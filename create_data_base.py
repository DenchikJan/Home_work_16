# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from utils import read_file, get_model_all, get_model_one_element_for_id

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(10))

    orders = relationship('Order', back_populates='users')
    offers = relationship('Offer', back_populates='users')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer)

    users = relationship('User', back_populates='orders')
    offers = relationship('Offer', back_populates='orders')


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = relationship('User', back_populates='offers')
    orders = relationship('Order', back_populates='offers')


app.app_context().push()
with app.app_context():
    db.drop_all()
    db.create_all()


for user in read_file('users.json'):
    user_data = User(id=user['id'],
                     first_name=user['first_name'],
                     last_name=user['last_name'],
                     age=user['age'],
                     email=user['email'],
                     role=user['role'],
                     phone=user['phone']
                     )
    try:
        db.session.add(user_data)
        #print(User.query.all())
    except Exception as e:
        print(f'{e}')
db.session.commit()


for order in read_file('orders.json'):
    order_data = Order(id=order['id'],
                       name=order['name'],
                       description=order['description'],
                       start_date=order['start_date'],
                       end_date=order['end_date'],
                       price=order['price'],
                       customer_id=order['customer_id'],
                       executor_id=order['executor_id']
                       )
    try:
        db.session.add(order_data)
        #print(Order.query.all())
    except Exception as e:
        print(f'{e}')
db.session.commit()


for offer in read_file('offers.json'):
    offer_data = Offer(id=offer['id'],
                       order_id=offer['order_id'],
                       executor_id=offer['executor_id']
                       )
    try:
        db.session.add(offer_data)
        #print(Offer.query.all())
    except Exception as e:
        print(f'{e}')
db.session.commit()

##############################################--USER--############################################################
@app.route('/users')
def get_users():
    users = get_model_all(User)

    users_data = []

    for user in users:
        users_data.append(
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'email': user.email,
                'role': user.role,
                'phone': user.phone
            })

    return jsonify(users_data)


@app.route('/users/<int:id>')
def get_user_for_id(id: int):
    user = get_model_one_element_for_id(User, id)

    users_data = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'age': user.age,
                    'email': user.email,
                    'role': user.role,
                    'phone': user.phone
                }

    return jsonify(users_data)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        id=data.get('id'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        email=data.get('email'),
        role=data.get('role'),
        phone=data.get('phone')
    )
    db.session.add(user)
    db.session.commit()

    return f'User {user.id} add'


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id: int):
    user = User.query.get(id)
    data = request.json

    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.age = data.get('age')
    user.email = data.get('email')
    user.role = data.get('role')
    user.phone = data.get('phone')

    db.session.add(user)
    db.session.commit()

    return f'User: {user.id} update.'


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return f'Пользователь {user.id} удален'


##############################################--ORDER--############################################################
@app.route('/orders')
def get_orders():
    orders = get_model_all(Order)

    orders_data = []

    for order in orders:
        orders_data.append(
            {
                'id': order.id,
                'name': order.name,
                'description': order.description,
                'start_date': order.start_date,
                'end_date': order.end_date,
                'price': order.price,
                'customer_id': order.customer_id,
                'executor_id': order.executor_id
            })

    return jsonify(orders_data)


@app.route('/orders/<int:id>')
def get_order_for_id(id: int):
    order = get_model_one_element_for_id(Order, id)

    orders_data = {
                    'id': order.id,
                    'name': order.name,
                    'description': order.description,
                    'start_date': order.start_date,
                    'end_date': order.end_date,
                    'price': order.price,
                    'customer_id': order.customer_id,
                    'executor_id': order.executor_id
                }

    return jsonify(orders_data)


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = Order(
        id=data.get('id'),
        name=data.get('name'),
        description=data.get('description'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        price=data.get('price'),
        customer_id=data.get('customer_id'),
        executor_id=data.get('executor_id')
    )
    db.session.add(order)
    db.session.commit()

    return f'Order {order.id} add'


@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id: int):
    order = Order.query.get(id)
    data = request.json

    order.name = data.get('name')
    order.description = data.get('description')
    order.start_date = data.get('start_date')
    order.end_date = data.get('end_date')
    order.price = data.get('price')
    order.customer_id = data.get('customer_id')
    order.executor_id = data.get('executor_id')

    db.session.add(order)
    db.session.commit()

    return f'Order: {order.id} update.'


@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id: int):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return f'Order {order.id} delete'

##############################################--OFFER--############################################################
@app.route('/offers')
def get_offers():
    offers = get_model_all(Offer)

    offers_data = []

    for offer in offers:
        offers_data.append(
            {
                'id': offer.id,
                'order_id': offer.order_id,
                'executor_id': offer.executor_id
            })

    return jsonify(offers_data)


@app.route('/offers/<int:id>')
def get_offer_for_id(id: int):
    offer = get_model_one_element_for_id(Offer, id)

    offers_data = {
                    'id': offer.id,
                    'order_id': offer.order_id,
                    'executor_id': offer.executor_id
                }

    return jsonify(offers_data)


@app.route('/offers', methods=['POST'])
def create_offer():
    data = request.json
    offer = Order(
        id=data.get('id'),
        order_id=data.get('order_id'),
        executor_id=data.get('executor_id')
    )
    db.session.add(offer)
    db.session.commit()

    return f'Offer {offer.id} add'


@app.route('/offers/<int:id>', methods=['PUT'])
def update_offer(id: int):
    offer = Offer.query.get(id)
    data = request.json

    offer.order_id = data.get('order_id')
    offer.executor_id = data.get('executor_id')

    db.session.add(offer)
    db.session.commit()

    return f'Offer: {offer.id} update.'


@app.route('/offers/<int:id>', methods=['DELETE'])
def delete_offer(id: int):
    offer = Offer.query.get(id)
    db.session.delete(offer)
    db.session.commit()
    return f'Offer {offer.id} delete'


if __name__ == "__main__":
    app.run()
