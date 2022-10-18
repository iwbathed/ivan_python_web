from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from datetime import date


def application(env, start_response):
    html_response = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Task 2</title>
        </head>
        <body>
        <form method="post">
            <p>x: <input type="text" name="x"></p>
            <p>y: <input type="text" name="y"></p>
            <p><button type="submit">Submit</button></p>
        </form>
        </body>
        </html>
    """
    if env['REQUEST_METHOD'].upper() == 'GET':
        print(env['QUERY_STRING'])
        status = '200 OK'

        headers = [('Content-Type', 'text/html; charset=UTF-8'),
                               ('Content-Length', str(len(html_response)))]

        start_response(status, headers)
        return [html_response.encode('utf-8')]
    elif env['REQUEST_METHOD'].upper() == 'POST':
        today = date.today().strftime("%d/%m/%Y")

        try:
            the_size = int(env.get('CONTENT_LENGTH', 0))
        except (ValueError):
            the_size = 0
        request_body = env['wsgi.input'].read(the_size)
        data = parse_qs(request_body.decode('utf-8'))
        print(data)
        try:
            response = str(int(data['x'][0]) + int(data['y'][0]))
        except ValueError:
            response = "Incorrect data."
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=UTF-8'),
                               ('Content-Length', str(len(html_response)))]

        start_response(status, headers)
        print(response)
        return ["Result: ".encode('utf-8'), response.encode('utf-8'), f"<br>Date: {today}".encode('utf-8')]
    else:
        return False


with make_server('localhost', 8888, application) as server:
    print("Starting server on 127.0.0.1:8888")
    server.serve_forever()
