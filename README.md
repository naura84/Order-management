# Order Management

Full-stack order management application: a **FastAPI** REST API backed by **PostgreSQL**, with a **React** front end to manage clients, orders and order lines.

Developed as part of a technical assessment, with a focus on business rules, code quality, database management, API design, testing and containerization.

**Dashboard interface**

![Dashboard interface](img/dashboard.png)

**Order details interface**

![Order details interface](img/order-details.png)

**Customer statistics interface**

![Customer statistics interface](img/Client-statistiques.png)

## Table of contents

- [Key features](#key-features)
- [Quick start](#quick-start)
- [Tech stack](#tech-stack)
- [Architecture](#architecture)
- [Data model](#data-model)
- [Business rules](#business-rules)
- [API](#api)
- [Authentication](#authentication)
- [Frontend](#frontend)
- [Technical choices](#technical-choices)
- [Database migrations and seed data](#database-migrations-and-seed-data)
- [Local installation](#local-installation)
- [Tests](#tests)
- [Docker](#docker)
- [Limitations and next steps](#limitations-and-next-steps)

---

## Key features

- Client, order and order line management
- Controlled order status transitions
- Automatic order total calculation
- Customer statistics: order count, total amount, average basket and most frequent status
- Order filtering by client, status and minimum/maximum amount, with pagination
- API key authentication
- React interface: dashboard, order and client lists, order creation, order details and client statistics
- PostgreSQL database with SQLAlchemy ORM and Alembic migrations
- Automated tests focused on business rules and edge cases
- Docker and Docker Compose support, with seed data for development

---

## Quick start

From the project root:

```bash
docker compose up --build
docker compose exec api alembic upgrade head
docker compose exec api python -m app.database.seed
```

| Service | Address |
| --- | --- |
| Frontend | `http://localhost:5173` |
| API | `http://localhost:8000` |
| Swagger (API docs) | `http://localhost:8000/docs` |
| PostgreSQL | `localhost:5432` |

The API requires the `X-API-Key` header. With the default Docker Compose configuration:

```http
X-API-Key: test-api-key
```

To stop the containers:

```bash
docker compose down
```

PostgreSQL data is persisted in a Docker volume named `postgres_data`.

---

## Tech stack

| Layer | Technologies |
| --- | --- |
| Backend | Python 3.14, FastAPI, Pydantic, SQLAlchemy, Alembic |
| Database | PostgreSQL 17 |
| Frontend | React, Vite |
| Tests | Pytest (SQLite test database) |
| Infrastructure | Docker, Docker Compose |

---

## Architecture

The project is organized into three main layers:

- **Frontend**: React application for viewing and managing clients, orders and order lines.
- **Backend**: REST API developed with FastAPI, responsible for business logic, validation and data access.
- **Database**: PostgreSQL, used to persist clients, orders and order lines.

### Project structure

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

### Backend layers

- **Routes**: receive HTTP requests, validate request parameters, call the appropriate service and return HTTP responses.
- **Services**: contain the business rules (client validation, order creation, status transition validation, order line restrictions, automatic total recalculation, statistics). Keeping business logic outside the routes makes the application easier to test, maintain and evolve.
- **Models**: SQLAlchemy models representing the database entities and their relationships.
- **Schemas**: Pydantic schemas validating API inputs and structuring API responses.

---

## Data model

The application is based on three main entities (the domain model uses French names: `Commande` = order, `LigneCommande` = order line):

```text
Client
  |
  +-- 1 --- N --- Commande
                    |
                    +-- 1 --- N --- LigneCommande
```

**Client**: `id`, `nom`, `email` (unique), `date_creation`

**Commande**: `id`, `client_id`, `statut`, `date_commande`, `montant_total`

**LigneCommande**: `id`, `commande_id`, `reference_article`, `libelle`, `quantite`, `prix_unitaire`

---

## Business rules

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

The order listing supports the following query parameters: `client_id`, `statut`, `montant_min`, `montant_max`, `page` and `page_size`.

Pagination is implemented on `GET /commandes`. The response provides the requested items, the total number of orders, the current page, the page size and the total number of pages, which prevents the API from returning an unnecessarily large number of records in a single request.

### Statistics

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/stats/clients/{id}` | Number of orders, total amount ordered, average basket and most frequent status |

Interactive Swagger documentation is available at `http://localhost:8000/docs` once the application is running.

---

## Authentication

The API uses a simple API key mechanism through the `X-API-Key` HTTP header. The key is configured through the `API_KEY` environment variable rather than being hard-coded.

The authentication dependency is applied at router level so that protected endpoints consistently require authentication.

This approach was chosen because the technical assessment requires a basic authentication mechanism and does not require a full user-management system or JWT-based authentication.

---

## Frontend

The frontend is developed with React and Vite. It allows users to:

- View the dashboard
- View the order list, search and filter orders by client, status and amount, and navigate between pages
- View order details and track order status transitions
- Create a new order and add lines to an order
- View registered clients, create a new client, and view client details and statistics

### Main pages

| Route | Page |
| --- | --- |
| `/` | Dashboard |
| `/commandes` | Order list |
| `/commandes/nouvelle` | Create an order |
| `/commandes/{id}` | Order details |
| `/commandes/{id}/lignes/nouvelle` | Add an order line |
| `/clients` | Client list and client creation |
| `/clients/{id}` | Client details and statistics |

---

## Technical choices

- **FastAPI**: lightweight architecture, automatic OpenAPI documentation, Pydantic integration and a dependency injection system. The interactive Swagger interface makes the API easy to test and explore during development.
- **PostgreSQL**: the application relies on a relational data model (clients, orders, order lines). PostgreSQL provides strong support for relational constraints, transactions, data integrity and structured queries.
- **SQLAlchemy**: ORM layer defining explicit relationships between clients, orders and order lines while keeping database operations separated from the HTTP layer.
- **Alembic**: versioned database schema migrations, applied consistently across environments.
- **Routes / services separation**: routes focus on HTTP concerns while services contain business rules, which improves readability, testability and maintainability.
- **API key authentication**: a simple key stored in an environment variable, sufficient for the assessment requirements.

---

## Database migrations and seed data

Alembic is used to create and update the database schema. Once the containers are running:

```bash
docker compose exec api alembic upgrade head
```

The project includes a seed script that creates sample clients, orders and order lines:

```bash
docker compose exec api python -m app.database.seed
```

The seed script does not insert duplicate initial data if clients already exist in the database.

---

## Local installation

### Backend

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

The API is available at `http://localhost:8000` and the Swagger documentation at `http://localhost:8000/docs`.

### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend is available at `http://localhost:5173`.

---

## Tests

The test suite uses a dedicated SQLite database so that tests remain isolated from the development PostgreSQL database.

From the `backend` directory:

```bash
pip install -r requirements.txt
pytest -v
```

The tests are organized by feature:

```text
tests/
|-- test_auth.py
|-- test_client.py
|-- test_commande.py
|-- test_ligne.py
`-- test_stats.py
```

They focus particularly on business rules and edge cases, rather than only testing successful HTTP requests. They cover:

- API authentication
- Client management and duplicate email handling
- Order creation and retrieval
- Order status transition rules, including invalid transitions
- Order line management, quantity and price validation
- Automatic order total recalculation
- Order filtering and pagination
- Customer statistics
- Restrictions on modifying non-draft orders

---

## Docker

The project can be run with Docker Compose. The Docker environment includes three services:

- **db**: PostgreSQL 17
- **api**: FastAPI application
- **frontend**: React/Vite application

See [Quick start](#quick-start) to launch the full project.

---

## Limitations and next steps

- Authentication relies on a single API key, as required by the assessment. A user-management system with JWT would be the natural evolution.
- Running the test suite automatically on every push (GitHub Actions) would complete the quality setup.
