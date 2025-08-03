def build_response(status_code=200, body="", content_type="text/html"):
    reason = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error"
    }.get(status_code, "OK")

    status_line = f"HTTP/1.1 {status_code} {reason}\r\n"
    headers = f"Content-Type: {content_type}\r\n"

    if body is not None:
        body_bytes = body.encode("utf-8")
        headers += f"Content-Length: {len(body_bytes)}\r\n"
        return status_line + headers + "\r\n" + body
    else:
        headers += "Content-Length: 0\r\n"
        return status_line + headers + "\r\n"
