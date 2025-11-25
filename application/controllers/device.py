from flask import request, jsonify, current_app
from ..services.device_service import DeviceService
from . import device_bp


@device_bp.route("/report", methods=["POST"])
def report():
    data = request.get_json()
    if not data or not DeviceService.valid_data(data):
        return jsonify({"error": "Bad Request"}), 400

    device = DeviceService.registred_device(data["device_name"], data['mac_address'])
    if device is None:
        return jsonify({"error": "Device not found"}), 400
    
    report = DeviceService.store_report(device, data)
    if report is None:
        return jsonify({"error": "Database unavailable"}), 500
    # enqueue background processing task if celery is available
    try:
        celery = current_app.celery
    except Exception:
        celery = None

    if celery:
        # use fully qualified task name so we avoid importing task objects here
        celery.send_task('application.celery_worker.process_pothole_report', args=[report.id])

    return jsonify({"status": "OK"}), 201