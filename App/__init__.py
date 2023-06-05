from .config import create_app, Config
from .routes import bp as main_bp

app = create_app(main_bp=main_bp)  # Pass main_bp as an argument
app.config.from_object(Config)
