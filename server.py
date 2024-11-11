# TCP Server for a simple terminal-based chat application,
# allowing communication with a client on the same device.

# Author: Mahshad Moshkelgosha
# Student Number: 400433145

import socket
import threading
import sys

# ANSI color codes for terminal output
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"

# Function to handle receiving messages from the client
def handle_client(conn, addr):
    print(GREEN + f"Client {addr} connected!" + RESET)
    try:
        while True:
            message = conn.recv(1024).decode('utf-8')
            if not message:
                print(YELLOW + "Client disconnected." + RESET)
                break
            print(MAGENTA + "Client: " + RESET + message)
    except Exception as e:
        print(YELLOW + "Client disconnected." + RESET)
    finally:
        conn.close()
        print(RED + "Shutting down server due to client disconnect." + RESET)
        sys.exit()

# Main function to initialize the server
def main():
    try:
        # Start the server on localhost at port 9000
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 9000))
        server_socket.listen(1)
        print(CYAN + "Server is running on port 9000..." + RESET)

        # Accept a single client connection
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

        # Capture and send messages to the client
        while True:
            try:
                message = input()
                conn.sendall((message + '\n').encode('utf-8'))
            except (BrokenPipeError, ConnectionResetError):
                print(RED + "Error writing to client. Disconnecting." + RESET)
                break
            except KeyboardInterrupt:
                print(RED + "\nShutting down server." + RESET)
                break

    except Exception as e:
        print(RED + "Error starting server:" + RESET, e)
    finally:
        server_socket.close()

if name == "__main__":
    main()
