from sys import argv
from socket import socket, SOCK_DGRAM
from select import select

def test_args():
    if len(argv) != 4:
        print("ERROR: Incorrect number of command line arguments")
        raise ValueError
    if argv[1] == argv[2] or argv[1] == argv[3] or argv[2] == argv[3]:
        print("ERROR: Duplicate ports given")
        raise ValueError
    ports = [0, 0, 0]
    for i in range(1, len(argv)):
        try:
            ports[i - 1] = int(argv[i])
        except ValueError:
            print(f"ERROR: Given port '{argv[i]}' is not an integer")
            raise TypeError
        if 1024 > ports[i - 1] or ports[i - 1] > 32767:
            print(f"ERROR: Given port '{ports[i - 1]}' is not in the range [1024, 32767]")
            raise ValueError
    return ports

def create_socket(lang):
    print(f"Creating socket for {lang}")
    return socket(type=SOCK_DGRAM)

def bind_socket(sock, port):
    print(f"Binding to port {port}")
    sock.bind(("localhost", port))

def main():

    try:
        ports = test_args()
    except ValueError as e:
        exit(1)
    except TypeError as e:
        exit(1)

    sockets = [None, None, None]

    try:
        for i in range(len(ports)):
            try:
                sockets[i] = create_socket("english")
            except:
                print('ERROR: Socket creation failed')
                raise OSError

            try:
                bind_socket(sockets[i], ports[i])
            except:
                print('ERROR: Socket binding failed')
                raise OSError

        while True:
            print("Waiting for requests...")
            readable = select(sockets, [], [])[0]
            # TODO: check packets

            # TODO: send response
    finally:
        for s in sockets:
            s.close()



if __name__ == "__main__":
    main()