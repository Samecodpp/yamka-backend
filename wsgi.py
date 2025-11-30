from application import create_app, db
from application.models import User, Device, DeviceReport, Pothole

app = create_app()

@app.route("/healthcheck")
def health():
    return {"status": "OK"}, 200

if __name__ == "__main__":
    app.run()
