from application import create_app

app = create_app()

@app.route("/healthcheck")
def health():
    return {"status": "OK"}, 200
