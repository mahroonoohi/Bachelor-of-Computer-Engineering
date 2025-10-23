import hashlib
import socket
import struct
from py3mschap import mschap

# Constants
RADIUS_PORT = 1812
SECRET = b'11041104'
MICROSOFT_VENDOR_ID = 311


def parse_radius_packet(packet):
    """
    Parse the RADIUS packet to extract relevant attributes.

    Args:
    - packet (bytes): The RADIUS packet in bytes format.

    Returns:
    - dict: Parsed attributes from the RADIUS packet.
    """

    # Extract packet header
    packet_type, packet_id, packet_length, authenticator = struct.unpack('!BBH16s', packet[0:20])

    attributes = {
        "packet_type": packet_type,
        "packet_id": packet_id,
        "packet_length": packet_length,
        "authenticator": authenticator.hex(),
    }

    # Parse AVPs
    avp_start = 20
    while avp_start < packet_length:
        avp_type, avp_length = struct.unpack('!BB', packet[avp_start:avp_start + 2])
        avp_value = packet[avp_start + 2:avp_start + avp_length]

        # Extract User-Name
        if avp_type == 1:
            attributes["User-Name"] = avp_value.decode('utf-8')

        # Extract Vendor-Specific attributes
        elif avp_type == 26:
            vendor_id = struct.unpack('!I', avp_value[0:4])[0]
            if vendor_id == MICROSOFT_VENDOR_ID:
                vendor_type, vendor_length = struct.unpack('!BB', avp_value[4:6])
                vendor_value = avp_value[6:6 + vendor_length - 2]

                # Extract MS-CHAP-Challenge and MS-CHAP2-Response
                if vendor_type == 11:
                    attributes["MS-CHAP-Challenge"] = vendor_value
                elif vendor_type == 25:
                    attributes["MS-CHAP2-Response"] = vendor_value

        avp_start += avp_length

    return attributes


def verify_mschapv2_response(parsed_packet, username, password):
    """
    Verify the MS-CHAPv2 response using the provided username and password.

    Args:
    - parsed_packet (dict): Parsed attributes from the RADIUS packet.
    - username (str): The username.
    - password (str): The password.

    Returns:
    - bool: True if the MS-CHAPv2 response is valid, False otherwise.
    """

    # Extract challenges
    peer_challenge = parsed_packet["MS-CHAP2-Response"][2:18]
    authenticator_challenge = parsed_packet["MS-CHAP-Challenge"]

    # Compute the expected MS-CHAPv2 response
    expected_response = mschap.generate_nt_response_mschap2(authenticator_challenge, peer_challenge, username, password)

    return expected_response.hex() == parsed_packet["MS-CHAP2-Response"][26:].hex()


def main():
    """
    Main function to start the RADIUS server and process incoming packets.
    """

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(('0.0.0.0', RADIUS_PORT))
        print("Listening for packets on port 1812...")

        try:
            while True:
                packet_data, _ = udp_socket.recvfrom(1024)
                parsed_packet = parse_radius_packet(packet_data)
                print(verify_mschapv2_response(parsed_packet, "amir", "1104"))
        except KeyboardInterrupt:
            print("Interrupted. Closing the socket.")


if __name__ == "__main__":
    main()
