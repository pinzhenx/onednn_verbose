import http.server
import socketserver
import webbrowser


def render(content):
    class handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            # suppress log
            return

        def do_GET(s):
            s.send_response(200)
            s.send_header('Content-type', 'text/html')
            s.end_headers()
            s.wfile.write(bytes(content, 'utf-8'))
    return handler


def get_all_nic_ipv4():
    try:
        import netifaces as ni
        return [nic[ni.AF_INET][0]['addr'] for nic in
                (ni.ifaddresses(ifname) for ifname in ni.interfaces())
                if ni.AF_INET in nic]
    except ImportError:
        print('Warning: "pip install netifaces" to get all LAN IPs for remote access')
        import socket
        return [socket.gethostbyname(socket.gethostname())]


def serve_single_page(html):
    with socketserver.TCPServer(('', 0), render(html)) as serv:
        port = serv.server_address[1]
        for ip in get_all_nic_ipv4():
            url = f'http://{ip}:{port}'
            print('Serving at', url)
        webbrowser.open_new(url)
        serv.serve_forever()
