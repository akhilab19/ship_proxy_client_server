Ship Proxy Client and Server

This project implements a simple proxy system designed for a networking assignment. The main goal is to route all HTTP requests from a ship through a single TCP connection to an offshore proxy server.

System Overview

- The client application (running on the ship) listens on port 8080 and accepts HTTP requests from browsers or tools like curl.
- It forwards each request through one persistent TCP connection to a remote server.
- The proxy server receives the request, fetches the actual web content, and returns it back to the client.
- The client then delivers the response to the original requester.

Requests are handled sequentially, one after another, even if multiple requests come in at the same time.

Included Files

- proxy_server.py – Code for the offshore proxy server.
- ship_proxy.py – Code for the ship-side proxy client.
- Dockerfile_server – Dockerfile for containerizing the server.
- Dockerfile_client – Dockerfile for containerizing the client.

Running the Project with Docker

1. Build Docker Images

docker build -f Dockerfile_server -t proxy-server .
docker build -f Dockerfile_client -t ship-proxy .

2. Start the Containers

 Terminal 1 - Run the server
docker run -p 9999:9999 proxy-server

 Terminal 2 - Run the client
docker run -p 8080:8080 ship-proxy

Testing

To verify the setup is working, use:

curl -x http://localhost:8080 http://httpforever.com/

This command sends a request through the ship proxy to the offshore server, which returns the result from the target website.

Important Notes

- Only one TCP connection is used between the client and server.
- The system processes HTTP requests one at a time in the order they arrive.
- Ensure port 8080 (client) and 9999 (server) are open and not in use.

About

This code was developed as part of a programming task given by Segments Cloud Computing LLC.
