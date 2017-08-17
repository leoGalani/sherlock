"""Server runner instance."""
from flask_cors import CORS

from sherlockapi import app

if __name__ == '__main__':
    CORS(app, resources={r'/*': {"origins": '*', 'allow_headers': '*'}})
    app.run(host="0.0.0.0", port=8080)
