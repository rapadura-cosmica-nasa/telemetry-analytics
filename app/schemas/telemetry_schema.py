from marshmallow import Schema, fields, validate, EXCLUDE

class TelemetrySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    astronautId = fields.String(
        required=True,
        validate=validate.Length(min=2),
        error_messages={"required": "O campo 'astronautId' é obrigatório."}
    )
    timestamp = fields.String(
        required=True,
        validate=validate.Length(min=2),
        error_messages={"required": "O campo 'timestamp' é obrigatório."}
    )
    heartRate = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=400, error="O campo 'heartRate' deve estar entre 1 e 400."),
        error_messages={"required": "O campo 'heartRate' é obrigatório."}
    )
    spo2 = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=100, error="O campo 'spo2' deve estar entre 0 e 100."),
        error_messages={"required": "O campo 'spo2' é obrigatório."}
    )
    radiationDoseMsv = fields.Float(
        required=True,
        validate=validate.Range(min=0, error="O campo 'radiationDoseMsv' não pode ser negativo."),
        error_messages={"required": "O campo 'radiationDoseMsv' é obrigatório."}
    )
    sleepHours = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=24, error="O campo 'sleepHours' deve estar entre 0 e 24."),
        error_messages={"required": "O campo 'sleepHours' é obrigatório."}
    )
    riskLevel = fields.String(dump_only=True)
    alertMessage = fields.String(dump_only=True)