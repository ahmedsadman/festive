from application import create_app
from dotenv import load_dotenv
from config_dev import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run(debug=True)
