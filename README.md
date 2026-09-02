# Order Management API

Backend API for managing clients, orders, order lines, order statuses, and customer statistics.

The project was developed as part of a backend technical assessment, with a focus on code quality, business rules, database management, API design, testing, and containerization.

---

## Features

- Client management
- Order management
- Order line management
- Controlled order status transitions
- Automatic order total calculation
- Customer statistics: order count, total amount, average basket, and most frequent status
- Order filters by client, status, and minimum/maximum amount
- Order pagination
- API key authentication
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Automated tests
- Docker and Docker Compose support
- Seed data for development

---

## Tech Stack

- **Python 3.14**
- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **PostgreSQL**
- **Alembic**
- **Pytest**
- **Docker / Docker Compose**
- **React / Vite**

---

## Data Model

The application is based on three main entities:

```text
Client
  |
  +-- 1 --- N --- Commande
                    |
                    +-- 1 --- N --- LigneCommande
```

### Client

- `id`
- `nom`
- `email` (unique)
- `date_creation`

### Commande

- `id`
- `client_id`
- `statut`
- `date_commande`
- `montant_total`

### LigneCommande

- `id`
- `commande_id`
- `reference_article`
- `libelle`
- `quantite`
- `prix_unitaire`

---

## Business Rules

The application implements the following business rules:

### Order status

Orders follow controlled status transitions:

```text
brouillon
    +---> confirmée
    |        +---> expédiée
    |        |        +---> livrée
    |        +---> annulée
    +---> annulée
```

Once an order is **livrée** or **annulée**, its status cannot be changed.

### Order lines

- Lines can only be added to an order in `brouillon`.
- `quantite` must be greater than `0`.
- `prix_unitaire` cannot be negative.
- The order total is automatically recalculated whenever its lines change.
- The total cannot be manually provided by the client.

### Clients

- Client email addresses must be unique.
- Creating a client with an existing email returns an appropriate HTTP error.

---

## API

### Clients

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/clients` | Create a client |
| `GET` | `/clients/{id}` | Retrieve a client and its orders |

### Orders

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/commandes` | Create an order |
| `POST` | `/commandes/{id}/lignes` | Add an order line |
| `PATCH` | `/commandes/{id}/statut` | Change order status |
| `GET` | `/commandes/{id}` | Retrieve an order with its lines |
| `GET` | `/commandes` | List paginated orders with optional filters |

### Statistics

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/stats/clients/{id}` | Retrieve the number of orders, total amount ordered, average basket, and most frequent status |

The order listing supports:

- `client_id`
- `statut`
- `montant_min`
- `montant_max`
- `page`
- `page_size`

---

## Authentication

The API uses a simple API key authentication mechanism through the `X-API-Key` HTTP header.

The key is configured through the `API_KEY` environment variable.

Example:

```http
X-API-Key: test-api-key
```

The authentication dependency is applied at router level so that protected endpoints consistently require authentication.

This approach was chosen because the technical assessment requires a basic authentication mechanism and does not require a full user-management system or JWT-based authentication.

---

## Architecture

The project is organized into three main layers:

- **Frontend**: React application for viewing and managing clients, orders, and order lines.
- **Backend**: REST API developed with FastAPI, responsible for business logic, validation, and data access.
- **Database**: PostgreSQL used to persist clients, orders, and order lines.

### Project Structure

```text
order-management/
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── main.py
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── Dockerfile
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Routes

The route layer is responsible for:

- Receiving HTTP requests
- Validating request parameters
- Calling the appropriate service
- Returning HTTP responses

### Services

Business rules are handled in dedicated service modules.

This includes:

- Client validation
- Order creation
- Status transition validation
- Order line restrictions
- Automatic total recalculation
- Statistics calculations

Keeping business logic outside the routes makes the application easier to test, maintain, and evolve.

### Models

SQLAlchemy models represent the database entities and their relationships.

### Schemas

Pydantic schemas validate API inputs and structure API responses.

## Frontend

The frontend is developed with React and Vite.

It allows users to:

- View the dashboard
- View the order list
- Search and filter orders by client, status, and amount
- Navigate between order pages
- View order details
- Add lines to an order
- Create a new order
- View registered clients
- Create a new client
- View client details and statistics
- Track order status transitions

### Main Pages

- `/` - Dashboard
- `/commandes` - Order list
- `/commandes/nouvelle` - Create an order
- `/commandes/{id}` - Order details
- `/commandes/{id}/lignes/nouvelle` - Add an order line
- `/clients` - Client list and client creation
- `/clients/{id}` - Client details and statistics

---

## Technical Choices

### FastAPI

FastAPI was chosen for its lightweight architecture, automatic OpenAPI documentation, Pydantic integration, and dependency injection system.

It also provides an interactive Swagger interface, which makes it easy to test and explore the API during development.

### PostgreSQL

PostgreSQL was selected as the main database because the application relies on a relational data model involving clients, orders, and order lines.

It provides strong support for relational constraints, transactions, data integrity, and structured queries.

### SQLAlchemy

SQLAlchemy provides the ORM layer used to interact with PostgreSQL.

It allows the application to define explicit relationships between clients, orders, and order lines while keeping database operations separated from the HTTP layer.

### Alembic

Alembic is used to manage database schema migrations.

This allows database changes to be versioned and applied consistently across environments.

### Routes / Services Separation

Routes focus on HTTP concerns while services contain business rules.

This separation improves readability, testability, and maintainability and avoids putting complex business logic directly inside API endpoints.

### API Key Authentication

A simple API key was chosen because the assessment requires basic authentication without requiring a complete authentication and user-management system.

The key is stored in an environment variable rather than being hard-coded into the application logic.

### Pagination

Pagination is implemented on `GET /commandes` using `page` and `page_size`.

The response provides:

- The requested items
- Total number of orders
- Current page
- Page size
- Total number of pages

Pagination prevents the API from returning an unnecessarily large number of records in a single request.

---

## Database Migrations

Alembic is used to create and update the database schema.

To apply the migrations:

```bash
docker compose exec api alembic upgrade head
```

---

## Seed Data

The project includes a seed script that creates sample clients, orders, and order lines.

Once the containers are running:

```bash
docker compose exec api python -m app.database.seed
```

The seed script does not insert duplicate initial data if clients already exist in the database.

---

## Installation

### Local Installation

#### Backend

From the project root:

```bash
cd backend
pip install -r requirements.txt
```

Configure the required environment variables, including:

```text
DATABASE_URL=postgresql+psycopg://order_admin:order_password@localhost:5432/order_management
API_KEY=test-api-key
```

Start the API:

```bash
uvicorn main:app --reload
```

The API is available at `http://localhost:8000`.

Swagger documentation is available at `http://localhost:8000/docs`.

#### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend is available at `http://localhost:5173`.

---

## API Documentation

Once the application is running, the interactive Swagger documentation is available at:

```text
http://localhost:8000/docs
```

The API requires the `X-API-Key` header.

With the default Docker Compose configuration:

```http
X-API-Key: test-api-key
```

---

## Tests

The test suite uses a dedicated SQLite database so that tests remain isolated from the development PostgreSQL database.

From the `backend` directory:

```bash
pip install -r requirements.txt
pytest -v
```

The tests cover:

- API authentication
- Client management and duplicate email handling
- Order creation and retrieval
- Order status transition rules
- Order line management
- Quantity and price validation
- Automatic order total recalculation
- Order filtering and pagination
- Customer statistics
- Invalid status transitions
- Restrictions on modifying non-draft orders

---

## Testing Strategy

The tests are organized by feature:

```text
tests/
|-- test_auth.py
|-- test_client.py
|-- test_commande.py
|-- test_ligne.py
`-- test_stats.py
```

The test suite focuses particularly on business rules and edge cases, rather than only testing successful HTTP requests.

---

## Docker

The project can be run with Docker Compose.

The Docker environment includes three services:

- **db**: PostgreSQL 17
- **api**: FastAPI application
- **frontend**: React/Vite application

### Start the Full Project

From the project root:

```bash
docker compose up --build
```

The services are available at:

| Service | Address |
| --- | --- |
| Frontend | `http://localhost:5173` |
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| PostgreSQL | `localhost:5432` |

To stop the containers:

```bash
docker compose down
```

PostgreSQL data is persisted in a Docker volume named `postgres_data`.