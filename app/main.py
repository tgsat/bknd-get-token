from flask import Flask
from flask_cors import CORS
import os
import logging
from app.routes.auth import auth_bp
from app.routes.offset import offset_bp
from app.routes.logs import logs_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Konfigurasi
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(offset_bp, url_prefix='/api')
    app.register_blueprint(logs_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'service': 'ArcGIS REST API'}
    
    @app.route('/api/health')
    def api_health():
        return {
            'status': 'running',
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)