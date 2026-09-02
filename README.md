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
- Customer statistics
- Filtering and pagination
- API key authentication
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Automated tests
- Docker and Docker Compose support
- Seed data for development

---

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **PostgreSQL**
- **Alembic**
- **Pytest**
- **Docker / Docker Compose**

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

## API Endpoints

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
| `GET` | `/commandes` | List, filter, and paginate orders |

### Statistics

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/stats/clients/{id}` | Retrieve customer order statistics |

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

## Project Structure

```text
order-management/
|
+-- Dockerfile
+-- docker-compose.yml
|
+-- backend/
    |
    +-- main.py
    +-- requirements.txt
    +-- alembic.ini
    |
    +-- alembic/
    |   +-- versions/
    |
    +-- app/
    |   +-- routes/
    |   +-- services/
    |   +-- models/
    |   +-- schemas/
    |   +-- database/
    |   +-- core/
    |   +-- utils/
    |
    +-- tests/
        +-- conftest.py
        +-- test_auth.py
        +-- test_client.py
        +-- test_commande.py
        +-- test_ligne.py
        +-- test_stats.py
```

---

## Architecture

The project follows a layered architecture separating HTTP handling, business logic, database models, and validation schemas.

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

### Tests

The test suite uses a dedicated SQLite database and focuses particularly on business rules and edge cases, rather than only testing successful HTTP requests.

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

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Start the application

From the project root:

```bash
docker compose up --build
```

This starts:

- The FastAPI API
- The PostgreSQL database

The API is available at `http://localhost:8000`.

### Apply migrations

From a second terminal:

```bash
docker compose exec api alembic upgrade head
```

### Load seed data

```bash
docker compose exec api python -m app.database.seed
```

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

## Running Tests

The test suite uses a dedicated SQLite database so that tests remain isolated from the development PostgreSQL database.

From the `backend` directory:

```bash
pip install -r requirements.txt
pytest -v
```

The tests cover:

- API authentication
- Client creation
- Duplicate client emails
- Client retrieval
- Order creation
- Order status transitions
- Invalid status transitions
- Restrictions on modifying non-draft orders
- Order line creation
- Quantity and price validation
- Automatic order total recalculation
- Order filtering
- Pagination
- Customer statistics

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

A dedicated test database is used to avoid modifying the development database during test execution.

The test suite focuses particularly on business rules and edge cases, rather than only testing successful HTTP requests.

---

## Docker

The project includes a Docker configuration with two services:

```text
+---------------------+
|      FastAPI        |
|       API           |
|      :8000          |
+----------+----------+
           |
           |
+----------v----------+
|     PostgreSQL      |
|       :5432         |
+---------------------+
```

Docker Compose handles the application and database services together.

The PostgreSQL data is stored in a Docker volume so that database data persists when containers are restarted.

---

## Development

The application can also be run locally without Docker for development and testing.

The project uses environment variables for configuration, including:

```text
DATABASE_URL
API_KEY
```

---

## Key Technical Points

The project focuses on several backend engineering principles:

- Separation of concerns
- Explicit business rules
- Database integrity
- Input validation
- API authentication
- Pagination
- Automated testing
- Database migrations
- Containerization
- Clear API documentation

The main objective is to provide a maintainable backend rather than simply implementing the required endpoints.

---

## Author

Developed as part of a backend technical assessment.
