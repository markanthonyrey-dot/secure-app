# tests/test_main.py
import pytest
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHealthEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_check_returns_200(self, client):
        """Test that health check returns 200 status"""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON response"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
    
    def test_health_check_has_timestamp(self, client):
        """Test that health check includes timestamp"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'timestamp' in data
        assert 'service' in data

class TestGreetEndpoint:
    """Tests for the greeting endpoint"""
    
    def test_greet_default(self, client):
        """Test greeting with default name"""
        response = client.post('/api/greet', 
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'Hello, World!' in data['message']
    
    def test_greet_with_name(self, client):
        """Test greeting with provided name"""
        response = client.post('/api/greet',
                              data=json.dumps({'name': 'Alice'}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'Hello, Alice!' in data['message']
    
    def test_greet_sanitizes_input(self, client):
        """Test that input is properly sanitized"""
        response = client.post('/api/greet',
                              data=json.dumps({'name': '  Bob  '}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'Hello, Bob!' in data['message']
    
    def test_greet_rejects_invalid_type(self, client):
        """Test that invalid input types are rejected"""
        response = client.post('/api/greet',
                              data=json.dumps({'name': 123}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_greet_limits_length(self, client):
        """Test that overly long names are truncated"""
        long_name = 'A' * 200
        response = client.post('/api/greet',
                              data=json.dumps({'name': long_name}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should be truncated to 100 chars
        assert len(data['message']) < 250

class TestAddEndpoint:
    """Tests for the addition endpoint"""
    
    def test_add_valid_numbers(self, client):
        """Test addition with valid numbers"""
        response = client.post('/api/add',
                              data=json.dumps({'a': 5, 'b': 3}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 8.0
    
    def test_add_floats(self, client):
        """Test addition with floating point numbers"""
        response = client.post('/api/add',
                              data=json.dumps({'a': 5.5, 'b': 3.3}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert abs(data['result'] - 8.8) < 0.001
    
    def test_add_missing_fields(self, client):
        """Test addition with missing fields"""
        response = client.post('/api/add',
                              data=json.dumps({'a': 5}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_invalid_types(self, client):
        """Test addition with invalid types"""
        response = client.post('/api/add',
                              data=json.dumps({'a': 'five', 'b': 3}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_negative_numbers(self, client):
        """Test addition with negative numbers"""
        response = client.post('/api/add',
                              data=json.dumps({'a': -5, 'b': 3}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == -2.0

class TestSecurityFeatures:
    """Tests for security-related features"""
    
    def test_404_handler(self, client):
        """Test that 404 errors don't leak information"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_content_type_json(self, client):
        """Test that responses are JSON"""
        response = client.get('/health')
        assert response.content_type == 'application/json'
    
    def test_method_not_allowed(self, client):
        """Test that wrong HTTP methods are handled"""
        response = client.get('/api/greet')  # POST expected
        assert response.status_code == 405

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
