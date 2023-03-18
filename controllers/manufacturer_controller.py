from flask import Blueprint, jsonify, request, abort
from main import db
from models.manufacturer import Manufacturer
from models.users import User
from schemas.manufacturer_schema import manufacturer_schema, manufacturers_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest
from datetime import date

manufacturers = Blueprint('manufacturers', __name__, url_prefix="/manufacturers")

# error handler for validation error in marshmallow
@manufacturers.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify({'please check this field again': error.messages})
    response.status_code = 400
    return response

# The GET route endpoint - get all manufacturers
@manufacturers.route("/", methods=["GET"])
def get_manufacturers():
    # get all the manufacturers from the database table
    manufacturers_list = Manufacturer.query.all()
    # Convert the manufacturers from the database into a JSON format and store them in result
    result = manufacturers_schema.dump(manufacturers_list)
    # return the data in JSON format
    return jsonify(result)

# The GET manufacturer routes endpoint - get details on one manufacturer
@manufacturers.route("/<int:id>/", methods=["GET"])
def get_manufacturer(id):
    manufacturer = Manufacturer.query.get(id)
    #return an error if the manufacturer doesn't exist
    if not manufacturer:
        return jsonify({'error': 'Manufacturer not found'}), 400
    # Convert the manufacturers from the database into a JSON format and store them in result
    result = manufacturer_schema.dump(manufacturer)
    # return the data in JSON format
    return jsonify(result)

# The POST route endpoint - add a manufacturer
@manufacturers.route("/", methods=["POST"])
@jwt_required()
def create_manufacturers():
    # get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    # Find it in the db
    user = User.query.get(user_id)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    try:
        #add a new manufacturer
        manufacturer_fields = manufacturer_schema.load(request.json)
        new_manufacturer = Manufacturer()
        new_manufacturer.manufacturer_name = manufacturer_fields["manufacturer_name"]
        new_manufacturer.manufacturer_contact_number = manufacturer_fields["manufacturer_contact_number"]
        new_manufacturer.manufacturer_email = manufacturer_fields["manufacturer_email"]
        new_manufacturer.manufacturer_address = manufacturer_fields["manufacturer_address"]
        new_manufacturer.asset_id = manufacturer_fields ["asset_id"]
        # not taken from the request, generated by the server
        new_manufacturer.date = date.today()
        # add to the database and commit
        db.session.add(new_manufacturer)
        db.session.commit()
        #return the manufacturer in the response
        return jsonify("Manufacturer added", manufacturer_schema.dump(new_manufacturer))
    except BadRequest as e:
        # Handle the case where the request data is invalid
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle all other exceptions
        return jsonify({'error': 'New manufacturer could not be added, please check details again'}), 500

# The PUT route endpoint - update manufacturer details
@manufacturers.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_manufacturer(id):
    # Create a new manufacturer
    manufacturer_fields = manufacturer_schema.load(request.json)
    # get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    # Find it in the db
    user = User.query.get(user_id)
    # Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the manufacturer
    manufacturer = Manufacturer.query.filter_by(manufacturer_id=id).first()
    #return an error if the manufacturer doesn't exist
    if not manufacturer:
        return abort(400, description= "Manufacturer does not exist")
    # update the manufacturer details with the given values
    try:
        manufacturer.manufacturer_name = manufacturer_fields["manufacturer_name"]
        manufacturer.manufacturer_contact_number = manufacturer_fields["manufacturer_contact_number"]
        manufacturer.manufacturer_email = manufacturer_fields["manufacturer_email"]
        manufacturer.manufacturer_address = manufacturer_fields["manufacturer_address"]
        manufacturer.asset_id = manufacturer_fields["asset_id"]
        # not taken from the request, generated by the server
        manufacturer.date = date.today()
        # add to the database and commit
        db.session.commit()
        #return the manufacturer in the response
        return jsonify("Manufacturer updated", manufacturer_schema.dump(manufacturer))
    except BadRequest as e:
        # Handle the case where the request data is invalid
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle all other exceptions
        return jsonify({'error': 'Manufacturer details cannot be updated, please check details'}), 500


# The DELETE route endpoint - delete a manufacturer
@manufacturers.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_asset(id):
    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    user = User.query.get(user_id)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the manufacturer
    manufacturer = Manufacturer.query.filter_by(manufacturer_id=id).first()
    #return an error if the manufacturer doesn't exist
    if not manufacturer:
        return jsonify({'error': 'Manufacturer does not exist'}), 400
    #Delete the manufacturer from the database and commit
    db.session.delete(manufacturer)
    db.session.commit()
    #return the manufacturer in the response
    return jsonify("Manufacturer deleted", manufacturer_schema.dump(manufacturer))
