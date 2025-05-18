from flask import Blueprint, request, jsonify
from app import db
import uuid
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import FormSubmission, User

form_bp = Blueprint("form", __name__, url_prefix="/form")


@form_bp.route("", methods=["POST"])
@jwt_required()
def submit_form():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"message": "No form data submitted"}), 400

    submission = FormSubmission(
        id=str(uuid.uuid4()),
        user_id=user_id,
        form_data=data,
        submitted_at=datetime.utcnow()
    )

    db.session.add(submission)
    db.session.commit()

    return jsonify({"message": "Form submitted successfully", "submission_id": submission.id}), 201


@form_bp.route("/submissions", methods=["GET"])
@jwt_required()
def get_submissions():
    user_id = get_jwt_identity()
    submissions = FormSubmission.query.filter_by(user_id=user_id).all()

    submissions_list = []
    for s in submissions:
        submissions_list.append({
            "id": s.id,
            "form_data": s.form_data,
            "submitted_at": s.submitted_at.isoformat()
        })

    return jsonify({"submissions": submissions_list}), 200
