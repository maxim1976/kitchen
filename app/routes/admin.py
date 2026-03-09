from functools import wraps
from datetime import datetime, timedelta
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, jsonify, current_app,
)
from app import db
from app.models import MenuItem, Order

admin_bp = Blueprint('admin', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


# ── Auth ──────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if (username == current_app.config['ADMIN_USERNAME'] and
                password == current_app.config['ADMIN_PASSWORD']):
            session['admin_logged_in'] = True
            session.permanent = True
            return redirect(url_for('admin.dashboard'))
        error = 'Invalid username or password.'

    return render_template('admin/login.html', error=error)


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route('/')
@login_required
def dashboard():
    items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()
    return render_template(
        'admin/dashboard.html',
        items=[i.to_dict() for i in items],
    )


# ── CRUD ──────────────────────────────────────────────────────────────────────

@admin_bp.route('/items/add', methods=['POST'])
@login_required
def add_item():
    item = MenuItem(
        name=request.form['name'].strip(),
        name_zh=request.form.get('name_zh', '').strip(),
        category=request.form['category'],
        price=float(request.form['price']),
        desc=request.form.get('desc', '').strip(),
        desc_zh=request.form.get('desc_zh', '').strip(),
        available=request.form.get('available') == 'true',
    )
    db.session.add(item)
    db.session.commit()
    flash('Dish added successfully.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/items/<int:item_id>/edit', methods=['POST'])
@login_required
def edit_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.name      = request.form['name'].strip()
    item.name_zh   = request.form.get('name_zh', '').strip()
    item.category  = request.form['category']
    item.price     = float(request.form['price'])
    item.desc      = request.form.get('desc', '').strip()
    item.desc_zh   = request.form.get('desc_zh', '').strip()
    item.available = request.form.get('available') == 'true'
    db.session.commit()
    flash('Dish updated successfully.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/items/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Dish deleted.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/items/<int:item_id>/toggle', methods=['POST'])
@login_required
def toggle_item(item_id):
    """Called via fetch() from Alpine — returns JSON, no page reload."""
    item = MenuItem.query.get_or_404(item_id)
    item.available = not item.available
    db.session.commit()
    return jsonify({'success': True, 'available': item.available})


# ── Orders ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/orders')
@login_required
def orders():
    period = request.args.get('period', 'today')
    now = datetime.utcnow()

    if period == 'yesterday':
        d     = now - timedelta(days=1)
        start = d.replace(hour=0, minute=0, second=0, microsecond=0)
        end   = d.replace(hour=23, minute=59, second=59, microsecond=999999)
        label = 'Yesterday'
    elif period == 'week':
        start = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
        end   = now
        label = 'Last 7 Days'
    elif period == 'all':
        start = None
        end   = None
        label = 'All Time'
    else:  # today (default)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end   = now
        label = 'Today'

    q = Order.query
    if start:
        q = q.filter(Order.created_at >= start)
    if end:
        q = q.filter(Order.created_at <= end)
    all_orders = q.order_by(Order.created_at.desc()).all()

    total_revenue = sum(float(o.total) for o in all_orders)
    pending_count = sum(1 for o in all_orders if o.status == 'pending')
    done_count    = sum(1 for o in all_orders if o.status == 'done')

    def _dict(o):
        return {
            'id':           o.id,
            'orderNumber':  o.order_number,
            'customerName': o.customer_name,
            'orderType':    o.order_type,
            'notes':        o.notes or '',
            'total':        float(o.total),
            'status':       o.status,
            'tableNumber':  o.table_number or '',
            'time':         o.created_at.strftime('%H:%M'),
            'date':         o.created_at.strftime('%b %d'),
            'items': [
                {'name': i.name, 'qty': i.quantity, 'price': float(i.price)}
                for i in o.items
            ],
        }

    return render_template(
        'admin/orders.html',
        orders=[_dict(o) for o in all_orders],
        total_revenue=total_revenue,
        pending_count=pending_count,
        done_count=done_count,
        order_count=len(all_orders),
        period=period,
        period_label=label,
    )


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
def update_order_status(order_id):
    """Called via fetch() from Alpine — cycles order status, returns JSON."""
    order = Order.query.get_or_404(order_id)
    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if new_status in ('pending', 'ready', 'done'):
        order.status = new_status
        db.session.commit()
    return jsonify({'success': True, 'status': order.status})
