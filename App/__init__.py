from .config import create_app, db
from .routes import bp as main_bp

app, db = create_app()
app.register_blueprint(main_bp)
