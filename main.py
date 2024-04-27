import pymongo
from flask import Flask, request
from bson.json_util import dumps

try:
    mongo = pymongo.MongoClient(
        host = 'localhost',
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.local
    mongo.server_info() #trigger exception if cannot connect to db
except:
    print('Error -connect to db')

app = Flask(__name__)

@app.post('/products')
def createProduct():
    product = request.get_json().get('product')
    productId = db.products.insert_one(product).inserted_id
    return str(productId)

def addAttributeToUpdate(update, name: str, conversion = None):
    attribute = request.form.get(name)
    if attribute is None: return update
    update[name] = conversion(attribute) if conversion else attribute
    return update

@app.patch('/products/<int:cname>')
def updateProduct(cname):
    update = {}
    update = addAttributeToUpdate(update, 'name')
    update = addAttributeToUpdate(update, 'ratings', float)
    update = addAttributeToUpdate(update, 'no_of_ratings')
    update = addAttributeToUpdate(update, 'actual_price')
    update = addAttributeToUpdate(update, 'discount_price')

    db.products.update_one({ 'code': cname }, { '$set': update })
    return str(cname)

@app.delete('/products/<int:cname>')
def deleteProduct(cname):
    db.products.delete_one({ 'code': cname })
    return str(cname)

@app.get('/products')
def getAllProducts():
    products = db.products.find()
    if products is None: return "None Found"
    return dumps(list(products))

@app.get('/products/<int:cname>')
def getProduct(cname):
    product = db.products.find_one({ 'code': cname })
    return dumps(product) if product is not None else "None Found"
