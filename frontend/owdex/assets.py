import flask as f

asset = f.Blueprint('asset', __name__, template_folder="templates")


@asset.route("/<path:asset>")
def serve_asset(asset):
    return f.send_from_directory("assets", asset)
