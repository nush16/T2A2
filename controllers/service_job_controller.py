from flask import Blueprint, jsonify, request, abort
from main import db
from models.service_job import ServiceJob
from models.users import User
from werkzeug.exceptions import BadRequest
from schemas.service_job_schema import service_job_schema, service_jobs_schema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

service_job = Blueprint('service_jobs', __name__, url_prefix="/service_job")

# The GET route endpoint - get all the service_jobs
@service_job.route("/", methods=["GET"])
def get_all_service_jobs():
    # Get all the service_job from the database table
    service_job_list = ServiceJob.query.all()
    # Convert the service_job from the database into a JSON format and store them in result
    result = service_jobs_schema.dump(service_job_list)
    # Return the data in JSON format
    return jsonify(result)

# The GET routes endpoint - get details on one service_job
@service_job.route("/<int:id>/", methods=["GET"])
def get_service_jobs(id):
    service_job = ServiceJob.query.get(id)
    # Return an error if the service_job doesn't exist
    if not service_job:
        return jsonify({'error': 'Service job not found'}), 400
    # Convert the service_job from the database into a JSON format and store them in result
    result = service_job_schema.dump(service_job)
    # Return the data in JSON format
    return jsonify(result)

# The POST route endpoint - add a service_job
@service_job.route("/", methods=["POST"])
@jwt_required ()
def create_service_job():
    # Get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    # Find it in the db
    user = User.query.get(user_id)
    # Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    try:
        # Create a new service job
        service_fields = service_job_schema.load(request.json)
        new_service_job = ServiceJob
        new_service_job.service_description = service_fields["service_description"]
        new_service_job.asset_id = service_fields["asset_id"]
        new_service_job.service_date = service_fields["service_date"]
        new_service_job.asset_id = service_fields ["asset_id"]
        # Not taken from the request, generated by the server
        new_service_job.date = date.today()
        # Add to the database and commit
        db.session.add(new_service_job)
        db.session.commit()
        # Return the service_job in the response
        return jsonify(service_job_schema.dump(new_service_job))
    except BadRequest as e:
        # Handle the case where the request data is invalid
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle all other exceptions
        return jsonify({'error': 'New service job could not be added, please check details again'}), 500
        
# The PUT route endpoint - update service job
@service_job.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_service_job(id):
        # Get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    # Find it in the db
    user = User.query.get(user_id)
    # Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # Find the asset_type
    service_job = ServiceJob.query.filter_by(service_job_id=id).first()
    # Return an error if the asset_type doesn't exist
    if not service_job:
        return abort(400, description= "Service job does not exist")
    try:
        # Create a new service_job
        service_fields = service_job_schema.load(request.json)
        # Update the service job details with the given values
        service_job.service_description = service_fields["service_description"]
        service_job.asset_id = service_fields["asset_id"]
        service_job.service_date = service_fields["service_date"]
        service_job.asset_id = service_fields ["asset_id"]
        service_job.date = date.today()
        # Add to the database and commit
        db.session.add(service_job)
        db.session.commit()
        # Return the asset_type in the response
        return jsonify(service_job_schema.dump(service_job))
    except BadRequest as e:
        # Handle the case where the request data is invalid
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle all other exceptions
        return jsonify({'error': 'Service job details cannot be updated, please check details'}), 500

# The DELETE route endpoint - delete a service job
@service_job.route("/<int:id>/", methods=["DELETE"])
@jwt_required ()
def delete_service_job(id):
    # Get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    # Find it in the db
    user = User.query.get(user_id)
    # Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # Find the card
    service_job = ServiceJob.query.filter_by(service_job_id=id).first()
    # Return an error if the service job doesn't exist
    if not service_job:
        return jsonify({'error': 'Service job does not exist'}), 400
    # Delete the service job from the database and commit
    db.session.delete(service_job)
    db.session.commit()
    # Return the service job in the response
    return jsonify(service_job_schema.dump(service_job))
   