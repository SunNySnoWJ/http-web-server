import os
from response_utils import build_response
from urllib.parse import urlparse, parse_qs

def handle_request(method, path, headers=None, body=None):

    if method == "GET":
        parsed_url = urlparse(path)
        route = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Support /get-data?query=xxx
        if route == "/get-data":
            query_value = query_params.get("query", ["(empty)"])[0]
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>GET Result</title>
            </head>
            <body>
                <p>Received GET query: <b>{query_value}</b></p>
                <button onclick="window.location.href='/'">Main Page</button>
            </body>
            </html>
            """
            return build_response(200, html)
        # Support /upload-list: show files in uploads folder
        if route == "/delete":
            filename = query_params.get("filename", [None])[0]
            if filename:
                file_path = os.path.join("uploads", filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head><title>Delete Result</title></head>
                        <body>
                            <p>File <b>{filename}</b> deleted successfully.</p>
                            <button onclick="window.location.href='/upload-list'">Back to List</button>
                            <button onclick="window.location.href='/'">Main Page</button>
                        </body>
                        </html>
                        """
                        return build_response(200, html)
                    except Exception as e:
                        return build_response(500, f"<h1>500 Error</h1><p>Delete error: {e}</p>")
                else:
                    return build_response(404, f"<h1>404 Not Found</h1><p>File '{filename}' not found.</p>")
            else:
                return build_response(400, "<h1>400 Bad Request</h1><p>Missing filename parameter.</p>")
    
        if route == "/upload-list":
            try:
                files = os.listdir("uploads")
                file_list_html = "<ul>"
                for f in files:
                    file_list_html += f"<li>{f} - <a href='/delete?filename={f}'>Delete</a></li>"
                file_list_html += "</ul>"

                html = f"""
                <!DOCTYPE html>
                <html>
                <head><title>Uploaded Files</title></head>
                <body>
                    <h2>Uploaded Files</h2>
                    {file_list_html}
                    <button onclick="window.location.href='/'">Main Page</button>
                </body>
                </html>
                """
                return build_response(200, html)
            except Exception as e:
                return build_response(500, f"<h1>500 Error</h1><p>{e}</p>")
        
        # Serve static HTML pages (e.g., index.html)
        if route == "/":
            route = "/index.html"

        file_path = route.lstrip("/")
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return build_response(200, content)
            except Exception as e:
                return build_response(500, f"<h1>500 Error</h1><p>{e}</p>")
        else:
            return build_response(404, "<h1>404 Not Found</h1><p>Page not found!</p>")

        
    elif method == "POST":
        if path == "/submit":
            # handle form submission
            try:
                parsed_data = parse_qs(body)

                name = parsed_data.get("name", ["Anonymous"])[0]
                email = parsed_data.get("email", ["N/A"])[0]
                age = parsed_data.get("age", ["?"])[0]

                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>POST Result</title>
                </head>
                <body>
                    <h2>Submission Received!</h2>
                    <p><b>Name:</b> {name}</p>
                    <p><b>Email:</b> {email}</p>
                    <p><b>Age:</b> {age}</p>
                    <button onclick="window.location.href='/'">Main Page</button>
                </body>
                </html>
                """
                return build_response(200, html)

            except Exception as e:
                return build_response(500, f"<p>POST error: {e}</p>")
        else:
            return build_response(404, "<p>POST path not found.</p>")
        
    elif method == "HEAD":
        parsed_url = urlparse(path)
        route = parsed_url.path

        # Map "/" to "index.html" as the default homepage
        if route == "/":
            route = "/index.html"

        file_path = route.lstrip("/")

        # If the static file (e.g., index.html) exists, return it
        if os.path.isfile(file_path):
            return build_response(200, content_type="text/html", body=None)

        # Explicitly support known dynamic routes
        if route in ["/get-data", "/submit", "/upload-list", "/delete"]:
            return build_response(200, content_type="text/html", body=None)

        return build_response(404, body=None)



    elif method == "PUT":
        if path.startswith("/upload/"):
            filename = path[len("/upload/"):] 
            try:
                if not filename:
                    raise ValueError("Filename is missing in path.")

                file_path = os.path.join("uploads", filename)
                with open(file_path, "wb") as f:
                    f.write(body)
                print(f"[✅ PUT] Saved file '{filename}' ({len(body)} bytes)")
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>PUT Result</title>
                </head>
                <body>
                    <p>File '<b>{filename}</b>' uploaded successfully.</p>
                    <button onclick="window.location.href='/'">Main Page</button>
                </body>
                </html>
                """
                return build_response(200, html)
            except Exception as e:
                print(f"[❌ PUT ERROR] {e}")
                return build_response(500, f"<p>PUT file save error: {e}</p>")
        else:
            return build_response(404, "<p>PUT path not found.</p>")
