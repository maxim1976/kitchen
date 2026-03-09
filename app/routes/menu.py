import random
from flask import Blueprint, render_template, request, jsonify, current_app
from app import db
from app.models import MenuItem, Order, OrderItem

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/')
def front():
    return render_template('front/index.html')


@menu_bp.route('/menu')
def index():
    items = (
        MenuItem.query
        .filter_by(available=True)
        .order_by(MenuItem.category, MenuItem.name)
        .all()
    )
    table_number = request.args.get('table', '').strip()
    return render_template(
        'menu/index.html',
        items=[i.to_dict() for i in items],
        estimated_wait=current_app.config['ESTIMATED_WAIT'],
        table_number=table_number,
    )


@menu_bp.route('/order', methods=['POST'])
def place_order():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400

    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'success': False, 'error': 'Name is required'}), 400

    order_type = data.get('type', 'dine-in')
    if order_type not in ('dine-in', 'takeout'):
        return jsonify({'success': False, 'error': 'Invalid order type'}), 400

    cart_items = data.get('items', [])
    if not cart_items:
        return jsonify({'success': False, 'error': 'Cart is empty'}), 400

    # Generate a unique 4-digit order number
    for _ in range(20):
        order_number = str(random.randint(1000, 9999))
        if not Order.query.filter_by(order_number=order_number).first():
            break

    table_number = (data.get('table') or '').strip() or None

    order = Order(
        order_number=order_number,
        customer_name=name,
        order_type=order_type,
        notes=(data.get('notes') or '').strip(),
        total=data.get('total', 0),
        table_number=table_number,
    )
    db.session.add(order)
    db.session.flush()  # get order.id before committing

    for item_data in cart_items:
        db.session.add(OrderItem(
            order_id=order.id,
            menu_item_id=item_data.get('id'),
            name=item_data.get('name', ''),
            price=item_data.get('price', 0),
            quantity=item_data.get('qty', 1),
        ))

    db.session.commit()
    return jsonify({'success': True, 'orderNumber': order_number})
