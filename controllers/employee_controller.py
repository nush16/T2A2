from flask import Blueprint, jsonify, request, abort
from main import db
from models.employees import Employee
from models.assets import Asset
from models.admin import Admin
from schemas.employee_schema import employee_schema, employees_schema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

employees = Blueprint('employees', __name__, url_prefix="/employees")

# The GET route endpoint - get all the employees
@employees.route("/", methods=["GET"])
def get_employees():
    # get all the employees from the database table
    employees_list = Employee.query.all()
    # Convert the employees from the database into a JSON format and store them in result
    result = employees_schema.dump(employees_list)
    # return the data in JSON format
    return jsonify(result)

# The GET routes endpoint - get details on one employee
@employees.route("/<int:id>/", methods=["GET"])
def get_employee(id):
    employee = Employee.query.get(id)
    #return an error if the employee doesn't exist
    if not employee:
        return abort(400, description= "employee does not exist")
    # Convert the employee from the database into a JSON format and store them in result
    result = employee_schema.dump(employee)
    # return the data in JSON format
    return jsonify(result)

# The GET routes endpoint - get assets for one employee  
@employees.route('/assets/<int:employee_id>', methods=["GET"])
def employee_assets(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'})
    assets_dict_list = []
    for asset in employee.assets:
        asset_dict = {'asset_id': asset.asset_id, 'asset_name': asset.asset_name, 'serial_number':asset.serial_number}
        assets_dict_list.append(asset_dict)
    employee_dict = {'employee_id': employee.employee_id, 'first_name': employee.first_name, 'last_name': employee.last_name, 'assets': assets_dict_list}
    return jsonify(employee_dict)

# The GET routes endpoint - get mmnufacturer and assets for a employee  
@employees.route('/manufacturer/<int:employee_id>', methods=["GET"])
def employee_manufacturer(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'})
    assets_dict_list = []
    for asset in employee.assets:
        asset_dict = {'asset_id': asset.asset_id, 'asset_name': asset.asset_name, 'serial_number':asset.serial_number}
        assets_dict_list.append(asset_dict)
        for assettype in asset.asset_type_id:
            for manufacturer in assettype.manufacturer:
                manufacturer_dict = {'manufacturer_id': manufacturer.manufacturer_id, 'manufacturer_name': manufacturer.manufacturer_name, 'manufacturer_contact_number': manufacturer.manufacturer_contact_number,'manufacturer_email': manufacturer.manufacturer_email}
                assets_dict_list.append(manufacturer_dict)
    employee_dict = {'employee_id': employee.employee_id, 'first_name': employee.first_name, 'last_name': employee.last_name, 'asset_manufacturer': assets_dict_list}
    return jsonify(employee_dict)


# The POST route endpoint - add an employee
@employees.route("/", methods=["POST"])
def create_employees():
    # #Create a new employee
    employee_fields = employee_schema.load(request.json)

    new_employee = Employee()
    new_employee.first_name = employee_fields["first_name"]
    new_employee.last_name = employee_fields["last_name"]
    new_employee.email_address = employee_fields["email_address"]
    new_employee.contact_number = employee_fields["contact_number"]
    new_employee.room_number = employee_fields["room_number"]
    new_employee.position = employee_fields["position"]
    # not taken from the request, generated by the server
    new_employee.date = date.today()
    # add to the database and commit
    db.session.add(new_employee)
    db.session.commit()
    #return the employee in the response
    return jsonify(employee_schema.dump(new_employee))

# The PUT route endpoint - update employee details
@employees.route("/<int:id>/", methods=["PUT"])
# @jwt_required()
def update_employee(id):
    # Create a new employee
    employee_fields = employee_schema.load(request.json)

    #get the user id invoking get_jwt_identity
    # user_id = get_jwt_identity()
    #Find it in the db
    # user = User.query.get(user_id)
    # #Make sure it is in the database
    # if not user:
    #     return abort(401, description="Invalid user")
    # # Stop the request if the user is not an admin
    # if not user.admin:
    #     return abort(401, description="Unauthorised user")
    # # find the card
    employee = Employee.query.filter_by(id=id).first()
    # #return an error if the card doesn't exist
    # if not card:
    #     return abort(400, description= "Card does not exist")
    #update the car details with the given values
    employee.first_name = employee_fields["first_name"]
    employee.last_name = employee_fields["last_name"]
    employee.email_address = employee_fields["email_address"]
    employee.contact_number = employee_fields["contact_number"]
    employee.room_number = employee_fields["room_number"]
    employee.position = employee_fields["position"]
    # not taken from the request, generated by the server
    employee.date = date.today()
    # add to the database and commit
    db.session.commit()
    #return the card in the response
    return jsonify(employee_schema.dump(employee))


# The DELETE route endpoint - delete an employee
@employees.route("/<int:id>/", methods=["DELETE"])
def delete_employee(id):
    #get the user id invoking get_jwt_identity
    # admin_id = get_jwt_identity()
    # #Find it in the db
    # admin = Admin.query.get(admin_id)
    # #Make sure it is in the database
    # if not admin:
    #     return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    # if not user.admin:
    #     return abort(401, description="Unauthorised user")
    # find the card
    employee = Employee.query.filter_by(id=id).first()
    #return an error if the card doesn't exist
    if not employee:
        return abort(400, description= "employee doesn't exist")
    #Delete the card from the database and commit
    db.session.delete(employee)
    db.session.commit()
    #return the card in the response
    return jsonify(employee_schema.dump(employee))
  