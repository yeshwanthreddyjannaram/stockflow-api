# StockFlow API — Inventory & Order Management System

StockFlow is a RESTful API built using **Python, FastAPI, and PostgreSQL** to manage product inventory, categories, and customer orders.

The application supports product management, order processing, automatic stock updates, and order cancellation with stock restoration.

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Database Migrations:** Alembic
- **Server:** Uvicorn
- **Version Control:** Git & GitHub

## Features

### Category Management
- Create, retrieve, update, and delete categories.
- Prevent deletion of categories associated with products.

### Product Management
- Create, retrieve, update, and delete products.
- Search products by name.
- Filter products by category and maximum price.
- Pagination using `skip` and `limit`.
- Prevent deletion of products associated with existing orders.

### Order Management
- Create orders with multiple products.
- Validate product availability and stock quantity.
- Automatically calculate order totals.
- Automatically decrease stock when an order is placed.
- Retrieve all orders and individual order details.
- Update order status with transition validation.
- Cancel eligible orders and restore product stock.

## Project Structure

```text
STOCKFLOW/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── categories.py
│       ├── products.py
│       └── orders.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/yeshwanthreddyjannaram/stockflow-api.git
cd stockflow-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/stockflow_db
```

Replace the placeholders with your PostgreSQL credentials.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

## API Documentation

After starting the server, open:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/categories/` | Create category |
| GET | `/categories/` | Get all categories |
| GET | `/categories/{category_id}` | Get category by ID |
| PUT | `/categories/{category_id}` | Update category |
| DELETE | `/categories/{category_id}` | Delete category |
| POST | `/products/` | Create product |
| GET | `/products/` | Search and list products |
| GET | `/products/{product_id}` | Get product by ID |
| PUT | `/products/{product_id}` | Update product |
| DELETE | `/products/{product_id}` | Delete product |
| POST | `/orders/` | Create order |
| GET | `/orders/` | Get all orders |
| GET | `/orders/{order_id}` | Get order by ID |
| PUT | `/orders/{order_id}/status` | Update order status |
| PUT | `/orders/{order_id}/cancel` | Cancel order |

## Key Learning Outcomes

- Building REST APIs using FastAPI.
- Designing relational database models.
- Working with SQLAlchemy relationships.
- Request and response validation using Pydantic.
- Implementing inventory and order business logic.
- Handling database transactions and rollbacks.
- Managing API errors and HTTP status codes.
- Using Git and GitHub for version control.

## Author

**Yeshwanth Reddy Jannaram**

GitHub: https://github.com/yeshwanthreddyjannaram

---

*StockFlow — Inventory and Order Management API built as part of my backend development learning journey.*