import os
from owdex import create_app

app = create_app(config_file="/owdex.toml")

if app.config["DEBUG"]:
    app.run(host="127.0.0.1", port="5000")
else:
    from waitress import serve
    port = int(os.environ.get("PORT", 80))
    serve(app, host="0.0.0.0", port=port)
