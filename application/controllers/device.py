from flask import request, jsonify
from flask import current_app
from marshmallow import ValidationError
from ..services.device_service import DeviceService
from ..schemas import DeviceReportSchema
from . import device_bp

report_schema = DeviceReportSchema()


@device_bp.route("/report", methods=["POST"])
def report():
    try:
        validated_data = report_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    print(validated_data)
    device = DeviceService.registred_device(validated_data["device_name"], validated_data['mac_address'])
    if device is None:
        return jsonify({"error": "Device registration failed"}), 500

    report = DeviceService.store_report(device, validated_data)
    if report is None:
        return jsonify({"error": "Database unavailable"}), 500

    current_app.celery.send_task('worker.predict_pothole_score', args=[report.id])
    return jsonify({"status": "accepted", "report_id": report.id, "message": "Report is being processed"}), 201
