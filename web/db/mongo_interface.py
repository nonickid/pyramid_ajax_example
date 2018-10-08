import pymongo
from bson import ObjectId, json_util
import json


class MongoApi(object):

    def __init__(self, url='', user='', password=''):
        self.url = url
        self.user = user
        self.password = password
        self.db = ''
        self.products = ''

    def connect(self):
        conn = pymongo.MongoClient(self.url, username=self.user, password=self.password)
        if conn:
            return conn
        return None

    def get_products(self, conn):
        try:
            self.db = conn.shop
            self.products = self.db.products
            prod = self.products.find()
            return prod
        except pymongo.errors.ServerSelectionTimeoutError as e:
            return "MongoDB server connection timeout"

    def add_product(self, product):
        try:
            document_id = self.db.products.insert_one(product)
            inserted = self.products.find_one({'_id': ObjectId(document_id.inserted_id)})
            return json_util.dumps(inserted)
        except pymongo.errors.PyMongoError as e:
            return False

    def remove_product(self, objectId):
        try:
            self.db.products.delete_one({'_id': ObjectId(objectId['id'])})
            return True
        except pymongo.errors.PyMongoError as e:
            return False