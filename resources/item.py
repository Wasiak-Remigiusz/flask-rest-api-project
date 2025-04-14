# import uuid

# from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):

        ## ver1
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message= "Item not found.")

        # ver2
        item =ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self,item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        ## ver1
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted."}
        # except KeyError:
        #     abort(404, message= "Item not found.")

        # ver2
        item =ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
        # raise NotImplementedError("Deleting an item is not implemented.")


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):

        ## ver 1
        # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        #     )

        ## ver 2
        # try:
        #     item = items[item_id]
        #     # https://blog.teclado.com/python-dictionary-merge-update-operators/
        #     item |= item_data
        #     return item

        # except KeyError:
        #     abort(404, message="Item not found.")

        # ver3
        # item =ItemModel.query.get_or_404(item_id)
        # raise NotImplementedError("Updating an item is not implemented.")
    

        # ver4
        item =ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id = item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return items.values()
        # return {"items": list(items.values())}
        return ItemModel.query.all()
    

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        ## ver1
        # item_data = request.get_json()
        # if (
        #     "price" not in item_data
        #     or "store_id" not in item_data
        #     or "name" not in item_data
        # ):
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        #     )


        ## ver2
        # for item in items.values():
        #     if (
        #     item_data["name"] == item["name"]
        #         and item_data["store_id"] == item["store_id"]
        #     ):
        #         abort(400, message=f"Item already exists.")

        # item_id = uuid.uuid4().hex
        # item = { **item_data, "id": item_id}
        # items[item_id] = item

        # ver3
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
        # return item, 201