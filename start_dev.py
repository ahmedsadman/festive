from application import create_app
from dotenv import load_dotenv
from config import Config

load_dotenv()
app = create_app(Config)

if __name__ == "__main__":
    app.run(debug=True)
