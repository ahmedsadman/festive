from flask import Blueprint

info_bp = Blueprint("info", __name__)


@info_bp.route("/", methods=["GET"])
def info():
    return {
        "title": "Fest Management API",
        "version": "1.0",
        "author": "Ahmed Sadman Muhib (Samyo), CSE 16, IUT",
    }
