from flask import Blueprint, jsonify, request
from main import db
from models.assets import Asset
from schemas.asset_schema import asset_schema, assets_schema
from datetime import date

assets = Blueprint('assets', __name__, url_prefix="/assets")

# get all the assets
@assets.route("/", methods=["GET"])
def get_asset():
    # get all the assets from the database table
    assets_list = Asset.query.all()
    # Convert the assets from the database into a JSON format and store them in result
    result = assets_schema.dump(assets_list)
    # return the data in JSON format
    return jsonify(result)

# add an asset
@assets.route("/", methods=["POST"])
def create_asset():
    #Create a new asset
    asset_fields = asset_schema.load(request.json)

    new_asset = Asset()
    new_asset.serial_number = asset_fields["serial_number"]
    new_asset.date_purchased = asset_fields["date_purchased"]
    new_asset.employee_id = asset_fields["employee_id"]
    new_asset.asset_type_id = asset_fields["asset_type_id"]
    # not taken from the request, generated by the server
    new_asset.date = date.today()
    # add to the database and commit
    db.session.add(new_asset)
    db.session.commit()
    #return the asset in the response
    return jsonify(asset_schema.dump(new_asset))

# delete a asset
@assets.route("/<int:id>/", methods=["DELETE"])
def delete_asset(id):
    # #get the user id invoking get_jwt_identity
    # user_id = get_jwt_identity()
    # #Find it in the db
    # user = User.query.get(user_id)
    # #Make sure it is in the database
    # if not user:
    #     return abort(401, description="Invalid user")
    # # Stop the request if the user is not an admin
    # if not user.admin:
    #     return abort(401, description="Unauthorised user")
    # # find the card
    # card = Card.query.filter_by(id=id).first()
    # #return an error if the card doesn't exist
    # if not Card:
    #     return abort(400, description= "Card doesn't exist")
    # #Delete the card from the database and commit
    # db.session.delete(card)
    # db.session.commit()
    # #return the card in the response
    # return jsonify(card_schema.dump(card))
    return "Asset Deleted"