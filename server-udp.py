from sys import argv, exit
from socket import socket, SOCK_DGRAM, AF_INET, timeout, getaddrinfo
from select import select
from datetime import datetime, tzinfo

_HEADER_SIZE = 13


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
        sock = socket(AF_INET, SOCK_DGRAM)
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

def format_data(sock, sockets):
    try:
        data, address = sock.recvfrom(4096)
    except timeout:
        raise OSError("ERROR: Receiving timed out, dropping packet")
    except OSError:
        raise OSError("ERROR: Receiving failed, dropping packet")

    # test and type
    request_type = test_data(data)

    # details
    lang_index = sockets.index(sock)

    # request type string
    request_type_str = "date" if request_type == 0x0001 else "time"

    ip_address = getaddrinfo(address[0], address[1])[0][3]
    print(ip_address)

    return data, address, request_type, request_type_str, lang_index, ip_address

def month_name(lang, month):
    eng_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    maori_months = ["Kohi-tātea", "Hui-tanguru", "Poutū-te-rangi", "Paenga-whāwhā", "Haratua", "Pipiri", "Hōngingoi", "Here-turi-kōkā", "Mahuru", "Whiringa-ā-nuku", "Whiringa-ā-rangi", "Hakihea"]
    germ_months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

    months = [eng_months, maori_months, germ_months]

    return months[lang][month - 1]

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
            try:
                print("Waiting for requests...")
                readable = select(sockets, [], [])[1]
                for sock in readable:
                    # get all the stuff
                    data, address, request_type, request_type_str, lang_index, ip_address = format_data(sock, sockets)

                    # proper packet
                    print(f"{languages[lang_index]} received {request_type_str} request from {ip_address}")

                    dt = datetime.now()
                    mm = dt.minute
                    hh = dt.hour
                    day = dt.day
                    month = dt.month
                    year = dt.year

                    text = ""
                    if lang_index == 0: # english
                        if request_type == 0x0001:  # current date
                            text = f"Today's date is {month_name(lang_index, month)} {day}, {year}"
                        else:  # current time
                            text = f"The current time is {hh}:{mm}"

                    elif lang_index == 1:
                        if request_type == 0x0001:  # current date
                            text = f"Ko te rā o tēnei rā ko {month_name(lang_index, month)} {day}, {year}"
                        else:  # current time
                            text = f"Ko te wā o tēnei wā {hh}:{mm}"

                    else:
                        if request_type == 0x0001:  # current date
                            text += f"Heute ist der {month_name(lang_index, month)} {day}, {year}"
                        else:  # current time
                            text += f"Die Uhrzeit ist {hh}:{mm}"

                    text_bytes = text.encode("utf-8")
                    text_length = len(text_bytes)
                    if text_length > 255:
                        raise ValueError("ERROR: Text too long, dropping packet")

                    packet_array = bytearray(text_length + _HEADER_SIZE)

                    # Header ------------------
                    # Magic Number
                    packet_array[0] = 0x36
                    packet_array[1] = 0xFB

                    # Packet Type
                    packet_array[2] = 0x00
                    packet_array[3] = 0x02

                    # Request Type
                    packet_array[4] = 0x00
                    packet_array[5] = lang_index + 1

                    # Date
                    packet_array[6] = (year & 0xFF00) >> 2
                    packet_array[7] =  (year & 0x00FF)
                    packet_array[8] = month
                    packet_array[9] = day
                    packet_array[10] = hh
                    packet_array[11] = mm

                    # text length
                    packet_array[12] = text_length

                    for i in range(text_length):
                        packet_array[i + 13] = text_bytes[i]

                    try:
                        sock.sendto(packet_array, address)
                        print("Response sent")
                    except OSError:
                        raise OSError("ERROR: Sending failed, dropping packet")


            except OSError as e:
                print(e)
            except ValueError as e:
                print(e)
            except Exception as e:
                print(e)

    except ValueError as e:
        print(e)
    except OSError as e:
        print(e)
    finally:
        for s in sockets:
            if s != None:
                s.close()
        exit(0)



if __name__ == "__main__":
    main()