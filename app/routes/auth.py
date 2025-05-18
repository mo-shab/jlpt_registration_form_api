from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
import uuid
from datetime import datetime, timedelta
from app.models import PasswordResetToken
from app.models import FormSubmission, User


auth_bp = Blueprint("auth_v2", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not all(k in data for k in ("full_name", "email", "password")):
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_pw = generate_password_hash(data["password"])

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        password_hash=hashed_pw
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"message": "Missing credentials"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=1)
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message" : "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }), 200


@auth_bp.route("/request-reset", methods=["POST"])
def request_password_reset():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "If the email is registered, a reset token will be sent."}), 200

    # Generate token
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)

    # Remove any existing tokens for this user
    PasswordResetToken.query.filter_by(user_id=user.id).delete()

    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    db.session.add(reset_token)
    db.session.commit()

    # In production: send email
    return jsonify({
        "message": "Password reset token generated.",
        "reset_token": token  # for testing only
    }), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    token = data.get("reset_token")
    new_password = data.get("new_password")

    if not all([email, token, new_password]):
        return jsonify({"message": "Email, token, and new password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid user or token"}), 400

    reset_token = PasswordResetToken.query.filter_by(
        user_id=user.id, token=token
    ).first()

    if not reset_token or reset_token.expires_at < datetime.utcnow():
        return jsonify({"message": "Invalid or expired token"}), 400

    # Hash new password and update user
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    # Delete token after use
    db.session.delete(reset_token)
    db.session.commit()

    return jsonify({"message": "Password has been reset successfully"}), 200


