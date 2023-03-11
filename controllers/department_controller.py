from flask import Blueprint, jsonify, request
from main import db
from models.departments import Department
from schemas.department_schema import department_schema, departments_schema
from datetime import date

departments = Blueprint('departments', __name__ , url_prefix="/departments")

# Get all the departments
@departments.route("/", methods=["GET"])
def get_departments():
    # get all the departments from the database table
    departments_list = Department.query.all()
    # # Convert the departments from the database into a JSON format and store them in result
    result = departments_schema.dump(departments_list)
    # return the data in JSON format
    # return jsonify(result)
    return jsonify(result)

# Add a department
@departments.route("/", methods=["POST"])
def create_department():
    # #Create a new department
    department_fields = department_schema.load(request.json)

    new_department = Department()
    new_department.department_name = department_fields["department_name"]
    new_department.building_number = department_fields["building_number"]
    new_department.address = department_fields["address"]
    # not taken from the request, generated by the server
    new_department.date = date.today()
    # add to the database and commit
    db.session.add(new_department)
    db.session.commit()
    #return the department in the response
    return jsonify(department_schema.dump(new_department))


# Delete a department
@departments.route("/<int:id>/", methods=["DELETE"])
def delete_department(id):
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
    return "Department Deleted"