from sys import argv
from socket import socket


def main():
    # TODO: check args
    if len(argv) != 4:
        print("ERROR: Incorrect number of command line arguments")
    if argv[1] == argv[2] or argv[1] == argv[3] or argv[2] == argv[3]:
        print("ERROR: Duplicate ports given")
    ports = []
    for i in range(1, len(argv)):
        try:
            ports[i - 1] = int(argv[i])
        except ValueError:
            print(f"ERROR: Given port '{argv[i]}' is not an integer")
        if 1024 > ports[i - 1] > 32767:
            print(f"ERROR: Given port '{ports[i - 1]}' is not in the range [1024, 32767]")

    eng_sock, maori_sock,germ_sock = None, None, None

    try:
        print("Creating socket for English")
        eng_sock = socket()
        print("Creating socket for Maori")
        maori_sock = socket()
        print("Creating socket for German")
        germ_sock = socket()
    except OSError:
        print("ERROR: Socket creation failed")
    finally:
        eng_sock.close()
        maori_sock.close()
        germ_sock.close()

    # TODO: Bind sockets
    try:
        print("TODO")
    finally:
        print("ERROR: Socket creation failed")
        eng_sock.close()
        maori_sock.close()
        germ_sock.close()
    # TODO: Infinite loop, waiting for response



if __name__ == "__main__":
    main()