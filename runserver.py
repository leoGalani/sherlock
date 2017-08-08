"""Server runner instance."""

from sherlockapi import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
