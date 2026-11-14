from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.telemetry_schema import TelemetrySchema
from app.services.biometrics_analyzer import analyze_telemetry, INDIVIDUAL_RULES, CROSS_RULES

analytics_bp = Blueprint('analytics', __name__, url_prefix="/api/v1")
telemetry_schema = TelemetrySchema()

@analytics_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "telemetry-analytics",
        "rules_loaded": len(INDIVIDUAL_RULES) + len(CROSS_RULES)
        }), 200

@analytics_bp.route('/analyze', methods=['POST'])
def analyze():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Corpo da requisição JSON ausente ou inválido."}), 400

    try:
        validated_data = telemetry_schema.load(payload)
    except ValidationError as err:
        return jsonify({"error": "Dados de telemetria inválidos", "details": err.messages}), 422

    analyzed_result = analyze_telemetry(validated_data)
    response_data = telemetry_schema.dump(analyzed_result)
    
    return jsonify(response_data), 200