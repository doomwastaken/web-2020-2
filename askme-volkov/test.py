def simplest_wsgi_app(environ, start_response):
     start_response('200 OK', [('Content-Type', 'text/plain')])
     yield b'Hello, world!'

def get_all_http(environ):
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items()) if key.startswith('HTTP_')
    ]
    return '\n'.join(response_body).encode('utf-8')

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    message = 'Hello world!\n'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    message += environ['QUERY_STRING']
    return [get_all_http(environ)]

    #return [b'Hello world!\n']