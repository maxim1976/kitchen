from datetime import datetime
from app import db


class MenuItem(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    name_zh     = db.Column(db.String(100), default='')
    category    = db.Column(db.String(50), nullable=False)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    desc        = db.Column(db.Text, default='')
    desc_zh     = db.Column(db.Text, default='')
    available   = db.Column(db.Boolean, default=True, nullable=False)
    image       = db.Column(db.String(200), default='')

    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)

    def to_dict(self):
        """Serialise for Alpine.js (camelCase keys match the static prototype)."""
        return {
            'id':        self.id,
            'name':      self.name,
            'nameZh':    self.name_zh or '',
            'category':  self.category,
            'price':     float(self.price),
            'desc':      self.desc or '',
            'descZh':    self.desc_zh or '',
            'available': self.available,
        }


class Order(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    order_number   = db.Column(db.String(10), nullable=False, unique=True)
    customer_name  = db.Column(db.String(100), nullable=False)
    order_type     = db.Column(db.String(20), nullable=False)  # 'dine-in' | 'takeout'
    notes          = db.Column(db.Text, default='')
    total          = db.Column(db.Numeric(10, 2), nullable=False)
    status         = db.Column(db.String(20), default='pending')  # pending | ready | done
    table_number   = db.Column(db.String(10), nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    order_id     = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=True)
    name         = db.Column(db.String(100), nullable=False)   # snapshot at order time
    price        = db.Column(db.Numeric(10, 2), nullable=False)
    quantity     = db.Column(db.Integer, default=1, nullable=False)
