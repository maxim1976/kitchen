# Hualien Kitchen — Full Workflow

## 1. Customer Flow

```
Customer enters cafe
        │
        ▼
Scans QR code at table / front desk
        │
        ▼
GET /                        ← landing page (front/index.html)
        │
        ▼
GET /menu                    ← menu page (menu/index.html)
   Alpine.js renders items from MENU_ITEMS (injected by Flask)
   Customer browses, adds items to cart (client-side state)
        │
        ▼
Fills in: Name │ Dine-in / Takeout │ Notes (optional)
        │
        ▼
Taps "Place Order"
        │
        ▼
POST /order  (JSON)          ← menu.py → place_order()
   Validates name + cart
   Saves Order + OrderItems to DB
   Returns { success: true, orderNumber: "4821" }
        │
        ▼
Confirmation screen (Alpine)
   Shows: order number, items, total, estimated wait (~15 min)
        │
        ▼
Receipt printed by kitchen printer  ← see section 3
        │
        ▼
Staff calls customer by name or number
        │
        ▼
Customer pays at counter → takes meal
```

---

## 2. Kitchen Staff Flow

```
Order saved to DB
        │
        ▼
GET /kitchen                 ← kitchen dashboard (PLANNED)
   Hands-free tablet display
   Shows pending orders in real-time (polling or WebSocket)
   Each card: order number │ customer name │ dine-in/takeout │ items │ notes
        │
        ▼
Staff prepares order
        │
        ▼
POST /kitchen/orders/<id>/ready   (PLANNED)
   Marks order as ready in DB
   Kitchen display removes card (or moves to "Done" column)
        │
        ▼
Staff calls customer by name / number
```

---

## 3. Receipt Printing

```
POST /order completes
        │
        ▼
Flask calls print_receipt(order)    ← app/printing.py  (PLANNED)
        │
        ▼
Sends ESC/POS commands to network thermal printer
   Library: python-escpos
   Printer: Epson TM-T88VI  or  Star TSP143IV
   Connection: LAN (IP address + port 9100)
        │
        ▼
Receipt printed at front desk / kitchen counter
   Contents:
   ─────────────────
   HUALIEN KITCHEN
   Order #4821
   ─────────────────
   Braised Pork Rice  × 1   NT$80
   Bubble Tea         × 2   NT$140
   ─────────────────
   TOTAL              NT$220
   [Dine-in]  Alex
   Notes: no sugar
   ─────────────────
   Est. wait: ~15 min
   ─────────────────
```

> **Printer note:** Use a **network** thermal printer, not portable/Bluetooth.
> Portable printers lose connection and run out of battery during service.
> Recommended: Epson TM-T88VI (~NT$8,000) connected via LAN to your router.

---

## 4. Owner / Admin Flow

```
GET /admin/login             ← admin/login.html
   Enter ADMIN_USERNAME + ADMIN_PASSWORD (set in Railway env vars)
        │
        ▼
GET /admin/                  ← admin/dashboard.html
        │
        ├── Toggle dish availability (one tap, no page reload)
        │        POST /admin/items/<id>/toggle  → returns JSON
        │        Alpine updates the button color instantly
        │        Green = Available │ Amber = Sold Out
        │
        ├── Edit dish  →  modal form  →  POST /admin/items/<id>/edit
        │
        ├── Add dish   →  modal form  →  POST /admin/items/add
        │
        └── Delete     →  confirm modal  →  POST /admin/items/<id>/delete
```

---

## 5. File Map

| Workflow step              | File                                  | Status   |
|----------------------------|---------------------------------------|----------|
| Landing page               | app/templates/front/index.html        | ✅ Built  |
| Customer menu              | app/templates/menu/index.html         | ✅ Built  |
| Place order (API)          | app/routes/menu.py → place_order()    | ✅ Built  |
| Kitchen display            | app/templates/kitchen/index.html      | ✅ Built  |
| Kitchen routes             | app/routes/kitchen.py                 | ✅ Built  |
| Receipt printing           | app/printing.py                       | PLANNED  |
| Admin login                | app/templates/admin/login.html        | ✅ Built  |
| Admin dashboard            | app/templates/admin/dashboard.html    | ✅ Built  |
| DB models                  | app/models.py (MenuItem, Order, OrderItem) | ✅ Built |

---

## 6. Routes Overview

```
GET  /                         Landing page
GET  /menu                     Customer menu
POST /order                    Place order → JSON

GET  /admin/login              Login form
POST /admin/login              Authenticate
GET  /admin/logout             Logout
GET  /admin/                   Dashboard
POST /admin/items/add          Add dish
POST /admin/items/<id>/edit    Edit dish
POST /admin/items/<id>/delete  Delete dish
POST /admin/items/<id>/toggle  Toggle availability (JSON)

GET  /kitchen/                 Kitchen display
GET  /kitchen/orders           Orders JSON (pending + ready)
POST /kitchen/orders/<id>/ready  Mark order ready
POST /kitchen/orders/<id>/done   Mark order served/done
```

---

## 7. What's Next

Priority order (highest impact first):

1. ~~**Kitchen display**~~ ✅ Done

2. ~~**Admin orders view**~~ ✅ Done

3. ~~**Table number support**~~ ✅ Done — QR URL `/menu?table=3`, stored in `Order.table_number`

4. **Receipt printing** — `app/printing.py` via `python-escpos`
   Requires physical network thermal printer (Epson TM-T88VI recommended).
   Implement when hardware is available.
