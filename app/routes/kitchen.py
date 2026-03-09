from flask import Blueprint, render_template, jsonify
from app import db
from app.models import Order

kitchen_bp = Blueprint('kitchen', __name__)


def _order_dict(order):
    return {
        'id':           order.id,
        'orderNumber':  order.order_number,
        'customerName': order.customer_name,
        'orderType':    order.order_type,
        'notes':        order.notes or '',
        'total':        float(order.total),
        'status':       order.status,
        'tableNumber':  order.table_number or '',
        'createdAt':    order.created_at.isoformat() + 'Z',
        'items': [
            {
                'name':     item.name,
                'quantity': item.quantity,
                'price':    float(item.price),
            }
            for item in order.items
        ],
    }


@kitchen_bp.route('/')
def index():
    return render_template('kitchen/index.html')


@kitchen_bp.route('/orders')
def orders_json():
    orders = (
        Order.query
        .filter(Order.status.in_(['pending', 'ready']))
        .order_by(Order.created_at)
        .all()
    )
    return jsonify([_order_dict(o) for o in orders])


@kitchen_bp.route('/orders/<int:order_id>/ready', methods=['POST'])
def mark_ready(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'ready'
    db.session.commit()
    return jsonify({'success': True})


@kitchen_bp.route('/orders/<int:order_id>/done', methods=['POST'])
def mark_done(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'done'
    db.session.commit()
    return jsonify({'success': True})
