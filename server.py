# TCP Client for a simple terminal-based chat application,
# connecting to a server on the same device.

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
YELLOW = "\033[33m"

# Function to handle receiving messages from the server
def receive_messages(sock):
    while True:
        try:
            # Receive message from the server
            message = sock.recv(1024).decode('utf-8')
            if not message:
                print(YELLOW + "Server disconnected." + RESET)
                sock.close()
                sys.exit()
            print(CYAN + "Server: " + RESET + message)
        except Exception as e:
            print(YELLOW + "Server disconnected." + RESET)
            sock.close()
            sys.exit()

# Main function to connect to the server and handle user input
def main():
    # Connect to the server at localhost on port 9000
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 9000))
        print(GREEN + "Connected to the server!" + RESET)
    except Exception as e:
        print(RED + "Error connecting to server:" + RESET, e)
        return

    # Start a thread to handle incoming messages
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # Capture and send messages to the server until disconnect
    try:
        while True:
            message = input()
            if message:
                sock.sendall((message + '\n').encode('utf-8'))
    except KeyboardInterrupt:
        print(RED + "\nExiting client." + RESET)
    finally:
        sock.close()

if name == "__main__":
    main()
