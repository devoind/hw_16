import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from my_db_init import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    """
    Функция запроса всех пользователей

    :return: возвращает список всех пользователей
    """
    if request.method == 'GET':
        return jsonify([user.to_dict_user() for user in User.query.all()])

    if request.method == 'POST':
        try:
            user = json.loads(request.data)
            new_user_obj = User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            )
            db.session.add(new_user_obj)
            db.session.commit()
            db.session.close()
            return "Пользователь создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    """
    Функция запроса, изменения и удаления пользователя по id

    :param user_id: получает id
    :return: возвращает пользователя по указанному id
    """
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Пользователь не найден"
        else:
            return jsonify(user.to_dict_user())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь c id {user_id} успешно изменен", 200
    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь c id {user_id} успешно удален", 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    """
    Функция запроса всех заказов

    :return: возвращает список всех заказов
    """
    if request.method == 'GET':
        return jsonify([order.to_dict_order() for order in Order.query.all()])

    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = [int(i) for i in order['start_date'].split("/")]
            month_end, day_end, year_end = [int(i) for i in order['end_date'].split("/")]
            new_order_obj = Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=year_end, month=month_end, day=day_end),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            )
            db.session.add(new_order_obj)
            db.session.commit()
            db.session.close()
            return "Заказ создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    """
    Функция запроса, изменения и удаления заказа по id

    :param order_id: получает id
    :return: возвращает заказ по указанному id
    """
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Заказ не найден"
        else:
            return jsonify(order.to_dict_order())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден", 404
        month_start, day_start, year_start = [int(i) for i in order['start_date'].split("/")]
        month_end, day_end, year_end = [int(i) for i in order['end_date'].split("/")]
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.data(year=year_start, month=month_start, day=day_start)
        order.end_date = datetime.data(year=year_end, month=month_end, day=day_end)
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказ c id {order_id} успешно изменен", 200
    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден", 404
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f"Заказ c id {order_id} успешно удален", 200


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    """
    Функция запроса всех предложений

    :return: возвращает список всех предложений
    """
    if request.method == 'GET':
        return jsonify([offer.to_dict_offer() for offer in Offer.query.all()])

    if request.method == 'POST':
        offer = json.loads(request.data)
        new_offer_obj = Offer(id=offer['id'], order_id=offer['order_id'], executor_id=offer['executor_id'])
        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение создано в базе данных", 200


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offers(offer_id):
    """
    Функция запроса всех предложений

    :param offer_id: получает id
    :return: возвращает предложение по указанному id
    """
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Предложение не найдено"
        else:
            return jsonify(offer.to_dict_offer())
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Предложение не найдено", 404
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение c id {offer_id} успешно изменено", 200
    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Предложение не найдено", 404
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение c id {offer_id} успешно удалено", 200


if __name__ == '__main__':
    app.run()
