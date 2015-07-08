from app import create_app
from config import Config

app = create_app(Config)
app.run()
