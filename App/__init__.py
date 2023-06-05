from .config import create_app
from .routes import bp as main_bp

app = create_app()
app.register_blueprint(main_bp)
