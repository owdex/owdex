import os

from owdex import create_app

app = create_app()

if app.config["DEBUG"]:
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
else:
    from waitress import serve

    port = int(os.environ.get("PORT", 80))
    serve(app, host="0.0.0.0", port=port)
