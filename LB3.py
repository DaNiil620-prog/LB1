from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Ініціалізація Flask та бази даних SQLite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для товарів
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(50), nullable=True)

# Модель для користувачів
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Ініціалізація бази даних
with app.app_context():
    db.create_all()

# HTTP Basic Authentication
def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not verify_user(auth.username, auth.password):
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
        return func(*args, **kwargs)
    return decorated

def verify_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    return check_password_hash(user.password, password)

# Додати адміністратора
@app.route('/create_admin', methods=['POST'])
def create_admin():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Admin user created!"}), 201

# Endpoints
@app.route('/items', methods=['GET', 'POST'])
@authenticate
def manage_items():
    if request.method == 'GET':
        items = Item.query.all()
        output = []
        for item in items:
            item_data = {'id': item.id, 'name': item.name, 'price': item.price, 'size': item.size}
            output.append(item_data)
        return jsonify(output)

    if request.method == 'POST':
        data = request.json
        new_item = Item(name=data['name'], price=data['price'], size=data['size'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item created!"}), 201

@app.route('/items/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@authenticate
def handle_item(id):
    item = Item.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({'id': item.id, 'name': item.name, 'price': item.price, 'size': item.size})

    if request.method == 'PUT':
        data = request.json
        item.name = data['name']
        item.price = data['price']
        item.size = data['size']
        db.session.commit()
        return jsonify({"message": "Item updated!"})

    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted!"})

# Запуск серверу
if __name__ == '__main__':
    app.run(debug=True, port=8000)
