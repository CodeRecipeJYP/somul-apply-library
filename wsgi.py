from app import create_app
from app.config import Config


app = create_app(Config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
