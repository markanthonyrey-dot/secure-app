# app/main.py
from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Security: Disable debug mode in production
app.config['DEBUG'] = False

# Security: Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security: Health check endpoint for container orchestration
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'secure-app'
    }), 200

# Security: Input validation and safe error handling
@app.route('/api/greet', methods=['POST'])
def greet():
    """Secure greeting endpoint with input validation"""
    try:
        data = request.get_json(silent=True) or {}
        
        # Security: Input validation - sanitize and validate
        name = data.get('name', 'World')
        if not isinstance(name, str):
            return jsonify({'error': 'Invalid input: name must be a string'}), 400
        
        # Security: Input sanitization - limit length and strip whitespace
        name = name.strip()[:100]
        
        if not name:
            name = 'World'
            
        logger.info(f'Greeting request processed for: {name}')
        
        return jsonify({
            'message': f'Hello, {name}!',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        # Security: Never expose internal error details to client
        logger.error(f'Error processing request: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

# Security: Safe math operation with validation
@app.route('/api/add', methods=['POST'])
def add_numbers():
    """Secure addition endpoint with type validation"""
    try:
        data = request.get_json(silent=True) or {}
        
        # Security: Strict type validation
        if not all(k in data for k in ('a', 'b')):
            return jsonify({'error': 'Missing required fields: a, b'}), 400
        
        try:
            a = float(data['a'])
            b = float(data['b'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid input: a and b must be numbers'}), 400
        
        # Security: Check for potential overflow
        result = a + b
        
        logger.info(f'Calculation performed: {a} + {b} = {result}')
        
        return jsonify({
            'result': result,
            'operation': 'addition'
        }), 200
        
    except Exception as e:
        logger.error(f'Error in calculation: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

# Security: 404 handler to prevent information leakage
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

# Security: 500 handler
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Security: Bind to localhost in development, configurable in production
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(host=host, port=port)
