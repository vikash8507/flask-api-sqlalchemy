from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'error': "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'error': 'Store with this name already exists'}, 400
            
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'error': 'An error occurred during saving the store'}, 500
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        
        return {"message": "Stotre deleted"}, 200

class StoreList(Resource):
    def get(self):
        stores = [store.json() for store in StoreModel.query.all()]
        return {'stores': stores}, 200