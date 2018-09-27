from werkzeug.http import HTTP_STATUS_CODES as HTC

def error_handler(status_code, message=None):
	err = {'error' : HTC.get(status_code , 'Unknown error')}
	if message:
		err['message'] = message
	return err