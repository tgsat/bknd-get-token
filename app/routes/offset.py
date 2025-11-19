from flask import Blueprint, request, jsonify
from app.utils.file_manager import file_manager

offset_bp = Blueprint('offset', __name__)

@offset_bp.route('/offset', methods=['GET'])
def get_offset():
    """Get current offset value"""
    offset_value = file_manager.get_offset()
    return jsonify({
        "success": True,
        "offset": offset_value
    })

@offset_bp.route('/offset', methods=['POST'])
def update_offset():
    """Update offset value"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "Data JSON diperlukan"
        }), 400
    
    offset_value = data.get('offset')
    
    if offset_value is None:
        return jsonify({
            "success": False,
            "error": "Offset value diperlukan"
        }), 400
    
    try:
        offset_value = int(offset_value)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Offset harus berupa angka"
        }), 400
    
    if file_manager.update_offset(offset_value):
        return jsonify({
            "success": True,
            "message": f"Offset berhasil diupdate ke {offset_value}",
            "offset": offset_value
        })
    else:
        return jsonify({
            "success": False,
            "error": "Gagal update offset"
        }), 500