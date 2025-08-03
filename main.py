import socket
from server import handle_request
from response_utils import build_response

HOST = "localhost"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server is running at http://{HOST}:{PORT}/")

while True:
    client_socket, client_address = server_socket.accept()
    try:
        request_data = b""
        while True:
            chunk = client_socket.recv(1024)
            request_data += chunk
            if b"\r\n\r\n" in request_data:
                break

        # match request line and headers
        header_part, _, body_part = request_data.partition(b"\r\n\r\n")
        header_text = header_part.decode()
        lines = header_text.splitlines()
        method, path, _ = lines[0].split()

        # match headers
        headers = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

        # match Content-Length and continue receiving body (file or form)
        content_length = int(headers.get("Content-Length", 0))
        while len(body_part) < content_length:
            body_part += client_socket.recv(1024)

        # determine if body is bytes or str (depends on request type)
        if method in ("POST",): 
            body = body_part.decode("utf-8")
        else: 
            body = body_part

        # call handling logic
        response = handle_request(method, path, headers, body)

    except Exception as e:
        print("Error:", e)
        response = build_response(400, "<h1>400 Bad Request</h1>")
        print("==== Raw Request ====")
        print(request_data.decode("utf-8", errors="ignore"))
    finally:
        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()
