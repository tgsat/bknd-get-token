from flask import Blueprint, request, jsonify
from app.utils.token_manager import token_manager

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/token', methods=['POST'])
def generate_token():
    """Generate token baru"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "Data JSON diperlukan"
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    referer = data.get('referer', 'https://www.arcgis.com')
    
    if not username or not password:
        return jsonify({
            "success": False,
            "error": "Username dan password diperlukan"
        }), 400
    
    result = token_manager.get_token(username, password, referer)
    
    if result["success"]:
        return jsonify({
            "success": True,
            "token": result["token"],
            "expires": result["expires"],
            "message": result["message"]
        })
    else:
        return jsonify({
            "success": False,
            "error": result["error"]
        }), 401

@auth_bp.route('/token/validate', methods=['POST'])
def validate_token():
    """Validasi token"""
    data = request.get_json()
    token = data.get('token')
    referer = data.get('referer', 'https://www.arcgis.com')
    
    if not token:
        return jsonify({
            "valid": False,
            "error": "Token diperlukan"
        }), 400
    
    is_valid = token_manager.validate_token(token, referer)
    
    return jsonify({
        "valid": is_valid
    })

@auth_bp.route('/token/status', methods=['GET'])
def token_status():
    """Status token saat ini (dari memory)"""
    if token_manager.current_token and time.time() < token_manager.token_expiry:
        return jsonify({
            "valid": True,
            "expires_in": token_manager.token_expiry - time.time()
        })
    return jsonify({"valid": False})