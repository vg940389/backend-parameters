import os
from flask import Flask, jsonify

app = Flask(__name__)

# Define the file paths for ConfigMap and Secret
CONFIG_PATH = '/config/application.properties'
SECRET_CONFIG_PATH = '/secret-config/application.secret.properties'

# Read the content of the `application.properties` file from ConfigMap
def read_config_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

# Add `application.properties.from.configmap` and `application.secret.properties.from.secret` to environment variables
os.environ['application.properties.from.configmap'] = read_config_file(CONFIG_PATH)
os.environ['application.secret.properties.from.secret'] = read_config_file(SECRET_CONFIG_PATH)


@app.route('/api/hello')
def hello_world():
    """Returns Hello, EDP!"""
    return 'Hello, EDP!'


@app.route('/env')
def get_environment_variables():
    """
    Returns all application environment variables.
    Includes application.properties.from.configmap and
    application.secret.properties.from.secret.
    """
    return jsonify(dict(os.environ))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
