from flask import Flask
from flask_cors import CORS

from router import event, group, user

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(event)
app.register_blueprint(group)
app.register_blueprint(user)

# @app.post('/products')
# def createProduct():
#     product = request.get_json().get('product')
#     productId = db.products.insert_one(product).inserted_id
#     return str(productId)

# def addAttributeToUpdate(update, name: str, conversion = None):
#     attribute = request.form.get(name)
#     if attribute is None: return update
#     update[name] = conversion(attribute) if conversion else attribute
#     return update

# @app.patch('/products/<int:cname>')
# def updateProduct(cname):
#     update = {}
#     update = addAttributeToUpdate(update, 'name')
#     update = addAttributeToUpdate(update, 'ratings', float)
#     update = addAttributeToUpdate(update, 'no_of_ratings')
#     update = addAttributeToUpdate(update, 'actual_price')
#     update = addAttributeToUpdate(update, 'discount_price')

#     db.products.update_one({ 'code': cname }, { '$set': update })
#     return str(cname)

# @app.delete('/products/<int:cname>')
# def deleteProduct(cname):
#     db.products.delete_one({ 'code': cname })
#     return str(cname)

# @app.get('/products')
# def getAllProducts():
#     products = db.products.find()
#     if products is None: return "None Found"
#     return dumps(list(products))

# @app.get('/products/<int:cname>')
# def getProduct(cname):
#     product = db.products.find_one({ 'code': cname })
#     return dumps(product) if product is not None else "None Found"
