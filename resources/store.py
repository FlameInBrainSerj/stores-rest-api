from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name '{name}' already exists"}

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"meassage": "An error occurred while creating the store"}, 500

        return store.json(), 202

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store was deleted"}


class StoreList(Resource):

    @jwt_required()
    def get(self):
        return {"stores": [store.json for store in StoreModel.query.all()]}
