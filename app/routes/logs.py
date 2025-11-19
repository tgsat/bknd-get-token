from flask import Blueprint, request, jsonify, Response
import time
import json
from app.utils.file_manager import file_manager

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    """Get log contents"""
    max_lines = request.args.get('max_lines', 1000, type=int)
    logs = file_manager.get_logs(max_lines)
    
    return jsonify({
        "success": True,
        "logs": logs
    })

@logs_bp.route('/logs', methods=['DELETE'])
def clear_logs():
    """Clear log file"""
    if file_manager.clear_logs():
        return jsonify({
            "success": True,
            "message": "Logs berhasil dihapus"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Gagal menghapus logs"
        }), 500

@logs_bp.route('/logs/stream')
def stream_logs():
    """Stream log updates (Server-Sent Events)"""
    def generate():
        log_file_path = "download.log"
        last_position = 0
        
        while True:
            try:
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    f.seek(last_position)
                    new_content = f.read()
                    
                    if new_content:
                        # Format sebagai SSE
                        for line in new_content.split('\n'):
                            if line.strip():
                                yield f"data: {json.dumps({'message': line})}\n\n"
                        
                        last_position = f.tell()
                    
                    time.sleep(1)
            except (FileNotFoundError, IOError):
                yield f"data: {json.dumps({'error': 'Log file tidak ditemukan'})}\n\n"
                time.sleep(5)
            except Exception as e:
                yield f"data: {json.dumps({'error': f'Error: {str(e)}'})}\n\n"
                time.sleep(5)
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Cache-Control'
        }
    )

@logs_bp.route('/logs/write', methods=['POST'])
def write_log():
    """Tulis pesan ke log (untuk testing)"""
    data = request.get_json()
    message = data.get('message', '')
    
    if file_manager.write_log(message):
        return jsonify({
            "success": True,
            "message": "Log berhasil ditulis"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Gagal menulis log"
        }), 500