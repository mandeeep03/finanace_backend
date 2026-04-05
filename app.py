import os
from flask import Flask, jsonify
from config import Config
from extensions import db, cors
from routes import users_bp, records_bp, dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cors.init_app(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(dashboard_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "endpoint not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "method not allowed"}), 405

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "internal server error"}), 500

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
