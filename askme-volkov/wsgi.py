from cgi import parse_qs, escape

HELLO_WORLD = b"Hello world!\n"
GET = b"GET\n"
POST = b"POST\n"
def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    if(environ['REQUEST_METHOD'] == 'GET'):
        return[GET]
    if(environ['REQUEST_METHOD'] == 'POST'):
        return[GET]
    return [HELLO_WORLD]

class AppClass:

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD


html = """
<html>
  <body>
    <h1>Hello, world!</h1>
    <ul>
      <h3>GET parameters from request:</h3>
      %(get_params)s
    </ul>
    <ul>
      <h3>POST parameters from request:</h3>
      %(post_params)s
    </ul>
  </body>
</html>
"""
HELLO_WORLD = b"Hello world!\n"

def hello_world(environ, start_response):
    get_dict = parse_qs(environ["QUERY_STRING"])
    if get_dict:
        get_params = ("<p>" +
                      "<p></p>".join(escape(param)
                                     for param in get_dict.keys) +
                      "</p>")
    else:
        get_params = ""

    response_body = html % {
        'get_params': get_params,
        'post_params': '',
    }

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)

    print(response_body)

    return [response_body]