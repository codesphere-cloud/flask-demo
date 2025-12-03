import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

# The service name used for the backend in the Codesphere ci.yml 
# and the resulting Kubernetes Service name
BACKEND_SERVICE_HOST = os.environ.get('BACKEND_HOST', 'backend')
BACKEND_SERVICE_PORT = os.environ.get('BACKEND_PORT', '3000')
BACKEND_URL = os.environ.get('BACKEND_URL', f"http://{BACKEND_SERVICE_HOST}:{BACKEND_SERVICE_PORT}/api")

# Simple HTML template for the frontend
HTML_TEMPLATE = """
<!doctype html>
<html>
<head><title>Codesphere Export Example</title></head>
<body>
    <h1>Codesphere Landscape Export Demo (Frontend)</h1>
    <p>Message from Backend: <strong>{{ backend_message }}</strong></p>
    <hr>
    <p>This is a Demo app consisting of a frontend and a backend service:</p>
    <ul>
        <li>The <strong>frontend</strong> service can be reached on at path <strong>/</strong></li>
        <li>The <strong>backend</strong> service can be reached on at path <strong>/api</strong></li>
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    backend_message = "Backend is currently unreachable (Service Discovery or Pod issue)."
    try:
        # Attempt to reach the backend service
        response = requests.get(BACKEND_URL, timeout=1)
        response.raise_for_status() # Raise exception for bad status codes
        backend_message = response.text
    except requests.exceptions.RequestException as e:
        # Fallback message if the backend is not available
        print(f"Error connecting to backend: {e}")
        
    return render_template_string(HTML_TEMPLATE, backend_message=backend_message)

if __name__ == '__main__':
    print(BACKEND_URL)
    app.run(host='0.0.0.0', port=3000)
