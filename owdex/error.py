import flask as f
from http import HTTPStatus

def error(status, explanation=None):
	# convert status to an HTTPStatus if it isn't already
	status = [status_obj for status_obj in HTTPStatus if status_obj.value == status][0] if isinstance(status, int) else status
	
	return f.render_template("error.html", status=status.value, phrase=status.phrase, explanation=explanation), status.value

def page_not_found(e):
	return error(404, explanation="Page not found!")

def internal_server_error(e):
	return error(500, explanation="The server experienced an issue handling your request.")
