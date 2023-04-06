import flask as f
from http import HTTPStatus

def error(status, explanation=None):
	return f.render_template("error.html", status=status.value, phrase=status.phrase, explanation=explanation), status.value

def page_not_found(e):
	return error(HTTPStatus.NOT_FOUND, explanation="Page not found!")

def internal_server_error(e):
	return error(HTTPStatus.INTERNAL_SERVER_ERROR, explanation="The server experienced an issue handling your request.")
