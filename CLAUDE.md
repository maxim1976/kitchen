# Hualien Web Backend - CLAUDE.md

## Project Purpose
Flask backend for the Hualien restaurant menu system.
Jinja2 templates are ported from ../menu/ (the static prototype).

## Tech Stack
- Flask (app factory pattern)
- Flask-SQLAlchemy + Flask-Migrate (ORM + migrations)
- PostgreSQL on Railway / SQLite for local dev
- Gunicorn (WSGI server)
- Alpine.js CDN (cart UI, admin modals, kitchen display — same as prototype)

## File Structure
```
backend/
├── app/
│   ├── __init__.py        # Flask app factory — registers all 3 blueprints
│   ├── models.py          # MenuItem, Order (+ table_number), OrderItem
│   ├── routes/
│   │   ├── menu.py        # GET / GET /menu POST /order
│   │   ├── admin.py       # /admin/* with login_required
│   │   └── kitchen.py     # /kitchen/* — unauthenticated tablet display
│   ├── templates/
│   │   ├── front/index.html    # landing page (dark theme, scroll sections)
│   │   ├── menu/index.html     # customer menu + cart + order form
│   │   ├── kitchen/index.html  # kitchen display (polls every 8s)
│   │   └── admin/
│   │       ├── login.html
│   │       ├── dashboard.html  # menu item CRUD
│   │       └── orders.html     # order history + status management
│   └── static/css/        # style.css + admin.css (from ../menu/css/)
├── config.py
├── requirements.txt
├── Procfile
└── .env.example
```

## Environment Variables
| Variable | Description | Default |
|---|---|---|
| SECRET_KEY | Flask session secret | dev-secret (change!) |
| DATABASE_URL | PostgreSQL URL (Railway auto-injects) | sqlite:///menu.db |
| ADMIN_USERNAME | Admin login username | admin |
| ADMIN_PASSWORD | Admin login password | changeme |
| ESTIMATED_WAIT | Wait time shown on confirmation (minutes) | 15 |

## Local Development
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # fill in values
flask db init
flask db migrate -m "initial"
flask db upgrade
flask run
```

## Railway Deployment
1. Push to GitHub
2. Connect repo in Railway dashboard
3. Add PostgreSQL plugin (free on Hobby plan)
4. Set env vars: SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD
5. Run migrations: Railway → Deploy → open Shell → `flask db upgrade`
6. Railway auto-detects Procfile

## Routes
### Customer
- `GET  /`                          landing page (front/index.html)
- `GET  /menu?table=N`              customer menu — table number from QR code
- `POST /order`                     place order (JSON API)

### Kitchen
- `GET  /kitchen/`                  tablet display — polls every 8s, no auth
- `GET  /kitchen/orders`            orders JSON (pending + ready)
- `POST /kitchen/orders/<id>/ready` mark order ready
- `POST /kitchen/orders/<id>/done`  mark order served

### Admin (login_required)
- `GET  /admin/login`               login page
- `POST /admin/login`               authenticate
- `GET  /admin/logout`              logout
- `GET  /admin/`                    menu item dashboard
- `POST /admin/items/add`           add item
- `POST /admin/items/<id>/edit`     edit item
- `POST /admin/items/<id>/delete`   delete item
- `POST /admin/items/<id>/toggle`   toggle availability (JSON)
- `GET  /admin/orders?period=today|yesterday|week|all`  order history
- `POST /admin/orders/<id>/status`  update order status (JSON)

## Data Model Notes
- `Order.table_number` — nullable String(10), populated from `?table=N` URL param
- `Order.status` — `pending` | `ready` | `done`
- `OrderItem.name` — snapshot of dish name at order time (not a live FK lookup)
- `MenuItem.to_dict()` maps DB fields to camelCase for Alpine.js (nameZh, descZh)

## Conventions
- CSS class names are identical to ../menu/ — do not rename them
- Admin auth: session-based, credentials from env vars
- Kitchen display: no auth — internal network only
- No CSRF protection yet — add Flask-WTF when moving to production

## Pending
- `app/printing.py` — ESC/POS receipt printing via python-escpos (needs hardware)
