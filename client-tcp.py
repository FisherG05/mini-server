import socket
import time

def main():

    # YOU CAN NOW DO THIS WITH A WEB BROWERS!!!!!

    # sanity
    # print("Hello World")
    
    # details
    host = "127.0.0.1"
    port = 8080
    address = (host, port)

    with socket.socket() as c_sock:

        c_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # client socket setup
        c_sock.connect(address)    
        c_sock_info = c_sock.getsockname()
        print(f"c_sock info: {c_sock_info}")


        # send bytes

        # 1
        # num_of_bytes = c_sock.send(b"GET / HTTP/1.1\r\nHost:localhost:8080\r\n\r\n")

        # 2
        # get_request = str.encode("GET / HTTP/1.1\r\nHost:localhost:8080\r\n\r\n")
        # c_sock.send(get_request)

        num_of_bytes = c_sock.send(bytearray('GET / HTTP/1.1\r\nHost:localhost:8080\r\n\r\n', 'utf-8'))
        print(f"Num of bytes: {num_of_bytes}")

        # recieve and translate them
        recieved_bytes = c_sock.recv(1024)
        decoded_str = recieved_bytes.decode("UTF-8")
        print(f"Decoded string: \n{decoded_str}")

        
    


if __name__ == "__main__":
    main()