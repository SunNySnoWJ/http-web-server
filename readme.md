# HTTP Web Server Project

This project shows the implementation of an HTTP web server that supports four key HTTP methods (`GET`, `POST`, `PUT`, and `HEAD`) via a simple HTML interface. It also includes a feature to view and manage uploaded files.

## Project Structure
<pre><code>
HTTP-Web-Server/
├── __pycache__/             # Cached bytecode files
├── uploads/                 # Directory for storing uploaded files
├── index.html               # Front-end interface for testing requests
├── main.py                  # Entry point: initializes socket server
├── response_utils.py        # Helper for building HTTP responses
├── server.py                # Main logic for handling request paths and methods
└── readme.md                # Project documentation
</code></pre>

## Supported HTTP Methods

| Method / Feature | Endpoint / Action                           | Expected Result                                                                |
|------------------|---------------------------------------------|--------------------------------------------------------------------------------|
| GET              | Open `/` in browser                         | Loads the main testing page (`index.html`)                                     |
| GET              | Submit query via `/get-data?query=...`      | Displays the value of the submitted query on a result page                     |
| POST             | Submit form to `/submit`                    | Displays submitted user info (name, email, age) on a new page                  |
| PUT              | Upload a file to `/upload/<filename>`       | Saves the uploaded file to the `uploads/` directory                            |
| HEAD             | Send HEAD request to `/` or `/index.html`   | Returns only HTTP headers (status, content-type, etc.) without body            |
| View Uploads     | Click "Show Uploads" on the main page        | Lists all uploaded files. Each file can be downloaded or deleted via a button.|


