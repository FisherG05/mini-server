from sys import argv, exit
from socket import socket, getaddrinfo, timeout, AF_INET, SOCK_DGRAM


def test_args():

    if len(argv) != 4:
        raise ValueError("ERROR: Incorrect number of command line arguments")

    req_type = 0
    if argv[1] != "date" and argv[2] != "time":
        raise ValueError(f"ERROR: Request type '{argv[1]}' is not valid")
    elif argv[3] == "date":
        req_type = 1
    else:
        req_type = 2

    try:
        port = int(argv[3])
    except Exception:
        raise ValueError(f"ERROR: Given port '{argv[3]}' is not an integer")

    if port < 1024 or port > 32767:
        raise ValueError(f"ERROR: Given port '{port}' is not in the range [1024, 32767]")

    try:
        return port, argv[2], req_type, argv[1], getaddrinfo(argv[2], port)[0]
    except Exception:
        raise ValueError(f"ERROR: Hostname resolution failed" )

def recv_from_host(sock):
    try:
        return sock.recvfrom(4096)
    except timeout:
        raise OSError("ERROR: Receiving timed out")
    except Exception:
        raise OSError("ERROR: Receiving failed")

def test_packet(res_pack):
    if len(res_pack) < 13:
        raise ValueError("ERROR: Packet is too small to be a DT_Response")

    if (res_pack[0] << 2) + res_pack[1] != 0x36FB:
        raise ValueError("ERROR: Packet magic number is incorrect")

    if (res_pack[2] << 2) + res_pack[3] != 0x0002:
        raise ValueError("ERROR: Packet is not a DT_Response")

    lang_code = (res_pack[4] << 2) + res_pack[5]
    if lang_code != 1 or lang_code != 2 or lang_code != 3:
        raise ValueError("ERROR: Packet has invalid language")

    lang = ""
    if lang_code == 1:
        lang = "English"
    elif lang_code == 2:
        lang = "Māori"
    else:
        lang = "German"

    year = (res_pack[6] << 2) + res_pack[7]
    if year >= 2100:
        raise ValueError("ERROR: Packet has invalid year")

    month = res_pack[8]
    if month < 1 or month > 12:
        raise ValueError("ERROR: Packet has invalid month")

    day = res_pack[9]
    if day < 1 or day > 31:
        raise ValueError("ERROR: Packet has invalid day")

    hour = res_pack[10]
    if hour < 0 or hour > 23:
        raise ValueError("ERROR: Packet has invalid hour")

    minute = res_pack[11]
    if minute < 0 or minute > 59:
        raise ValueError("ERROR: Packet has invalid minute")

    length = res_pack[12]
    if length != len(res_pack):
        raise ValueError("ERROR: Packet text length is incorrect")

    text = ""
    try:
        for i in range(13, length):
            text += res_pack[i].decode("UTF-8")
    except Exception:
        raise UnicodeDecodeError("ERROR: Packet has invalid text")


    return lang, lang_code, year, month, day, hour, minute, text, length



def main():
    port, address, req_type, req_string, addr_info = test_args()

    sock = None
    try:
        print("Creating Socket")
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(1)

        packet_array = bytearray(6)
        packet_array[0] = 0x36
        packet_array[1] = 0xFB
        packet_array[2] = 0x00
        packet_array[3] = 0x01
        packet_array[4] = 0x00
        packet_array[5] = req_type

        try:
            _ = sock.sendto(packet_array, addr_info[4])
        except Exception as e:
            # raise OSError("ERROR: Sending failed")
            raise OSError(e)

        print(f"{req_string} request sent to {addr_info[4][0]}:{port}")

        res_pack, recv_addr = recv_from_host(sock)

        lang, lang_code, year, month, day, hour, minute, text, length = test_packet(res_pack)

        print(f"{lang} response received:Text: {text}\nDate: {day}/{month}/{year}\nTime: {hour}:{minute})")

    except OSError as e:
        print(e)
    except ValueError as e:
        print(e)
    except UnicodeDecodeError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        if sock != None:
            sock.close()
        exit(0)




if __name__ == "__main__":
    main()