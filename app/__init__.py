from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    from app.routes.analytics_routes import analytics_bp
    app.register_blueprint(analytics_bp)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint não encontrado."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erro interno no motor de telemetria."}), 500

    return app