from application import create_app

app = create_app()

@app.route("/healthcheck")
def health():
    return {"status": "OK"}, 200

if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)