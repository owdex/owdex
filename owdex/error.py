import flask as f

def error(status, explanation=None):
	return f.render_template("error.html", status=status, explanation=explanation), status

def page_not_found(e):
	return error(404, explanation="Page not found!")

def internal_server_error(e):
	return error(500, explanation="The server experienced an issue handling your request.")
