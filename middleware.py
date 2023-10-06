class UUIDValidateMiddleware(object):
    def authenticate_uuid(request):
        # One-time configuration and initialization.
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = request.headers

        print(response['x-api-key'])
        return response

