from sys import argv
from socket import socket, SOCK_DGRAM, timeout
from select import select

def test_args(ports):
    if len(argv) != 4:
        raise ValueError("ERROR: Incorrect number of command line arguments")

    if argv[1] == argv[2] or argv[1] == argv[3] or argv[2] == argv[3]:
        raise ValueError("ERROR: Duplicate ports given")

    for i in range(1, len(argv)):
        try:
            ports[i - 1] = int(argv[i])
        except ValueError:
            raise TypeError(f"ERROR: Given port '{argv[i]}' is not an integer")
        if 1024 > ports[i - 1] or ports[i - 1] > 32767:
            raise ValueError(f"ERROR: Given port '{ports[i - 1]}' is not in the range [1024, 32767]")

    return ports

def create_socket(lang):
    print(f"Creating socket for {lang}")
    try:
        sock = socket(type=SOCK_DGRAM)
        sock.settimeout(1)
        return sock
    except:
        raise OSError('ERROR: Socket creation failed')

def bind_socket(sock, port):
    print(f"Binding to port {port}")
    try:
        sock.bind(("localhost", port))
    except:
        raise OSError('ERROR: Socket binding failed')

# TODO: format the ip address properly and return it
# def format_ip(address):

def test_data(data):
    if len(data) != 6:
        raise ValueError("ERROR: Packet length incorrect for a DT_Request, dropping packet")

    if data[0] << 2 + data[1] != 0x36FB:
        raise ValueError("ERROR: Packet magic number is incorrect, dropping packet")

    if data[2] << 2 + data[3] != 0x0001:
        raise ValueError("ERROR: Packet is not a DT_Request, dropping packet")

    request_type = data[4] << 2 + data[5]
    if request_type != 0x0001 or request_type != 0x0002:
        raise ValueError("ERROR: Packet has invalid type, dropping packet")
    return request_type

def main():
    """

    """

    # variables
    languages = ["English", "Maori", "German"]
    sockets = [None, None, None]
    ports = [0, 0, 0]

    try:
        test_args(ports)
    except ValueError as e:
        print(e)
        exit(1)
    except TypeError as e:
        print(e)
        exit(1)

    try:
        for i in range(len(ports)):

            sockets[i] = create_socket("english")
            bind_socket(sockets[i], ports[i])

        while True:
            print("Waiting for requests...")
            readable = select(sockets, [], [])[1]
            for sock in readable:
                # TODO: Create a method that returns a bunch of formatted stuff all in one go
                data, address = None, None

                try:
                    data, address = sock.recvfrom(4096)
                except timeout:
                    raise OSError("ERROR: Receiving timed out, dropping packet")
                except OSError:
                    raise OSError("ERROR: Receiving failed, dropping packet")

                # test and type
                request_type = test_data(data)

                # details
                index = sockets.index(sock)

                # proper packet
                print(f"{languages[index]} received {"date" if request_type == 0x0001 else "time"} request from {format_ip(address)}")

                # TODO: send response

    except ValueError as e:
        print(e)
    except OSError as e:
        print(e)
    finally:
        for s in sockets:
            s.close()



if __name__ == "__main__":
    main()