# 🍽️ Gastronomic ERP

A web-based ERP system designed for bars and restaurants. Manage employees, products, stock, payroll, and daily cash reconciliation (arqueos) from a single platform.

---

## Features

- 📊 **Dashboards** — Visual analytics powered by Chart.js (with heatmap and zoom plugins)
- 🗓️ **Weekly Schedule Panel** — Create and manage weekly shifts (Monday–Sunday) with PDF export
- 📦 **ABMs** — Full CRUD for products, raw materials, employees, and attendances; supports logical deletion
- 💰 **Payroll Management** — Daily salary tracking per employee with payment history
- 🧾 **Arqueos (Cash Reconciliation)** — End-of-day cash register closings with totals, card splits, differences, anulations, invitations, and expenses
- 🧂 **Stock & Recipes** — Track raw material stock levels and define product recipes with unit-of-measure support
- 🔐 **Session Management** — Stateless auth via JWT tokens stored in HTTPOnly cookies

---

## Tech Stack

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Backend    | Python / Flask                                  |
| Auth       | Flask-JWT-Extended                              |
| ORM        | SQLAlchemy                                      |
| Database   | SQLite                                          |
| Frontend   | Jinja2 templates + Vanilla JS                   |
| Charts     | Chart.js with heatmap and zoom plugins          |
| Alerts     | SweetAlert2                                     |
| PDF Export | WeasyPrint / ReportLab *(schedule export)*      |
| Security   | `werkzeug.security` for password hashing        |

---

## Sessions

Sessions are stored in **HTTPOnly cookies** containing a signed **JWT token**. The token payload includes the `user_id`, which is used to identify and authorize each request.

---

## ABMs & Logical Deletion

All entities that support deletion use a `record_status` boolean column:

- `True` → active record
- `False` → logically deleted (record is preserved to avoid data loss in related tables)

This applies to: **Users**, **Products**, **Raw Materials**.

Categories can be created for:
- **Products** → with a `sector` field (`kitchen` or `bar`)
- **Raw Materials** → simple name-based categorization

---

## Database Schema

Every table contains a primary key column named `id`.  
Tables marked with 🕐 include a `created_at` timestamp. Tables marked with 🗑️ include `record_status`.

### `bars` 🕐
| Column | Type   |
|--------|--------|
| id     | Integer PK |
| name   | String |

### `users` 🕐 🗑️
| Column     | Type    |
|------------|---------|
| id         | Integer PK |
| name       | String  |
| email      | String (unique) |
| password   | String (hashed) |
| created_at | DateTime |
| record_status | Boolean |

### `employees` 🕐
| Column       | Type    |
|--------------|---------|
| id           | Integer PK |
| user_id      | FK → users |
| address      | String  |
| rol          | Enum: `waiter`, `cashier`, `administrator`, `receptionist`, `chef`, `chef_assistant`, `dishes`, `manager` |
| leave_at     | DateTime (nullable) |
| daily_salary | Float   |
| bar_id       | FK → bars |
| created_at   | DateTime |

### `product_categories`
| Column | Type   |
|--------|--------|
| id     | Integer PK |
| name   | String |
| sector | Enum: `kitchen`, `bar` |

### `products` 🗑️
| Column      | Type   |
|-------------|--------|
| id          | Integer PK |
| name        | String |
| category_id | FK → product_categories |
| price       | Float  |
| bar_id      | FK → bars |
| record_status | Boolean |

### `sales` 🕐
| Column     | Type   |
|------------|--------|
| id         | Integer PK |
| product_id | FK → products |
| amount     | Integer |
| price      | Float  |
| bar_id     | FK → bars |
| created_at | DateTime |

### `payrolls` 🕐
| Column               | Type     |
|----------------------|----------|
| id                   | Integer PK |
| employee_id          | FK → employees |
| day                  | Date     |
| amount               | Float    |
| received_by_employee | DateTime |
| created_at           | DateTime |

### `expenses` 🕐
| Column       | Type   |
|--------------|--------|
| id           | Integer PK |
| payment_type | String |
| amount       | Float  |
| detail       | String |
| created_at   | DateTime |

### `arqueos` 🕐
| Column             | Type    |
|--------------------|---------|
| id                 | Integer PK |
| total              | Float   |
| card_total         | Float   |
| cash_total         | Float   |
| cash_difference    | Float   |
| total_anulations   | Float   |
| total_invitations  | Float   |
| total_expenses     | Float   |
| created_at         | DateTime |
| cashier_id         | FK → employees |
| manager_id         | FK → employees |
| bar_id             | FK → bars |
| detail             | Text    |
| arqueo_url         | String  |

### `raw_material_categories`
| Column | Type   |
|--------|--------|
| id     | Integer PK |
| name   | String |

### `raw_materials` 🗑️
| Column      | Type   |
|-------------|--------|
| id          | Integer PK |
| name        | String |
| category_id | FK → raw_material_categories |
| record_status | Boolean |

### `recipes`
| Column          | Type    |
|-----------------|---------|
| id              | Integer PK |
| product_id      | FK → products |
| raw_material_id | FK → raw_materials |
| amount          | Float   |
| uom             | String (default: `gr`) |

### `stock`
| Column          | Type    |
|-----------------|---------|
| id              | Integer PK |
| raw_material_id | FK → raw_materials (unique) |
| amount          | Float   |

### `stock_movements` 🕐
| Column          | Type    |
|-----------------|---------|
| id              | Integer PK |
| raw_material_id | FK → raw_materials |
| type            | Enum: `in`, `out` |
| amount          | Float   |
| created_at      | DateTime |

---

## Project Structure

```
gastronomic-erp/
├── app.py
├── config.py
├── database/
│   ├── __init__.py         # SQLAlchemy instance (db)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bar.py
│   │   ├── user.py
│   │   ├── employee.py
│   │   ├── product.py
│   │   ├── sale.py
│   │   ├── payroll.py
│   │   ├── expense.py
│   │   ├── arqueo.py
│   │   ├── raw_material.py
│   │   ├── recipe.py
│   │   └── stock.py
│   └── seed.py             # Optional: initial data seeding
├── routes/
├── templates/
├── static/
└── requirements.txt
```

---

## Getting Started

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app (creates SQLite DB automatically)
flask run
```

---

## Requirements

```
Flask
Flask-JWT-Extended
SQLAlchemy
Flask-SQLAlchemy
Werkzeug
```