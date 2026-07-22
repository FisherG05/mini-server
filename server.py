import socket
import time
from pathlib import Path

def main():
    
    # sanity
    # print("Hello World")
    
    # details
    host = "0.0.0.0"
    port = 8080
    address = (host, port)
    
    with socket.socket() as s_sock:

        s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # server socket setup
        s_sock.bind(address)
        s_sock.listen(2)
        
        # wait for connection
        conn, addr = s_sock.accept()
        print(f"Connected sock info: addr - {addr} : conn - {conn}")

        

        # recieve and translate them
        recieved_bytes = conn.recv(4096)
        decoded_str = recieved_bytes.decode()

        print(f"Decoded string: \n{decoded_str}")

        with Path('./about.html').open() as file:
            
            
            headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Thu, 23 Jul 2026 14:08:30 GMT\r\nContent-Length: 229\r\n\r\n"
            html = file.read()

            # send response
            num_of_bytes = conn.send(bytearray(headers + html, 'utf-8'))
            # num_of_bytes = conn.send(bytearray(html, 'utf-8'))
            print(f"Num of bytes: {num_of_bytes}")




if __name__ == "__main__":
    main()
