"""Server runner instance."""

from sherlock import app

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
