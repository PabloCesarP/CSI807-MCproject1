from flask import Flask, render_template

from blueprints.matriz import bp as matriz_bp
from engine.repository import JsonRepository


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object("config.Config")
    if config:
        app.config.update(config)

    # A matriz é carregada uma vez e compartilhada pelos blueprints.
    app.extensions["matriz"] = JsonRepository(app.config["DATA_DIR"]).carregar_matriz()

    app.register_blueprint(matriz_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
