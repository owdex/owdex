import os

from waitress import serve

from owdex import create_app

app = create_app()

port = int(os.environ.get("PORT", app.settings.runtime.port))

if app.settings.runtime.debug:
    app.run(host=app.settings.runtime.host, port=port)
else:
    serve(app, host=app.settings.runtime.host, port=port)
