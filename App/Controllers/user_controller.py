from flask import request
from ..Services import user_service

def register_user():
    user_info = request.json
    user_service.create_user(user_info)
    return {"message": "User created successfully"}, 201
