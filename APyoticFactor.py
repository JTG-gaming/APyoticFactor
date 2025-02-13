import typing
import socket

class AF_ServerInfo:
    """
    Allows requesting general or specific data from an Abiotic Factor server over its UDP Query Port

    Args:
        ip_address: IP or Domain Name for the server
        query_port: [Default: 27015] Query Port for the server

    Use get_info() for a dict of server rules
    Also includes a few miscellaneous get_[rule] functions for specific common info (server name, short code, player count, etc.)
    """

    def __init__(self, ip_address:str, query_port:int=27015) -> None:

        self.ip = ip_address
        self.port = query_port
        self.socket = None

    def _send_packet(self, packet:bytes) -> bytes | None:

        # Initialize Socket
        if not self.socket or self.socket.fileno() == -1:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(2)

        # Try to send packet
        try:
            self.socket.sendto(packet, (self.ip, self.port))
            data,addr = self.socket.recvfrom(1400)
        except socket.timeout:
            print("Socket Timed Out")
            return None
        except Exception as e:
            print(e)
            return None
        else:
            return data

    def _print_bytes(self, bytes_in:bytes, ret:bool=False) -> None | str:

        byte_str = ''
        for byte in bytes_in:
            byte_str += str(hex(byte)) + ' '

        if ret:
            return byte_str
        else:
            print(byte_str)

    def get_info(self,*,return_as_bytes:bool=False) -> dict[str, any] | bytes | None:
        """
        Returns server rules in dict format (key,value pairs)

        Args:
            return_as_bytes: [default: False] returns the raw packet without parsing into dict
        """

        # Send Packet with header data
        packet = b'\xFF\xFF\xFF\xFF\x56\xFF\xFF\xFF\xFF'
        data = self._send_packet(packet)

        # Respond with Challenge Number
        if data and data[4] == 65:
            packet = b'\xFF\xFF\xFF\xFF\x56' + data[5:]
            data = self._send_packet(packet)
        else:
            print("Challange Number Missing from server packet")
            return None

        # Return raw response packet
        if return_as_bytes:
            self.close()
            return data

        # Extract Strings from response data (minus header data)
        data = data.split(b'\x00')

        # Create key,value pair dict for strings in response data
        data_dict = {}
        for i in range(1, len(data)-1, 2):
            decoded_key = data[i].decode()
            data_type = decoded_key.split('_')

            # convert value to appropriate type
            match data_type[-1]:

                case 's':
                    decoded_key = data_type[0]
                    decoded_value = str(data[i+1].decode())

                case 'i':
                    decoded_key = data_type[0]
                    decoded_value = int(data[i+1].decode())

                case 'b':
                    decoded_key = data_type[0]
                    decoded_value = data[i+1].decode().lower() == 'true'

                case _:
                    decoded_value = data[i+1].decode()

            data_dict[decoded_key] = decoded_value
            #data_dict[data[i].decode()] = data[i+1].decode()

        #self.close()
        return data_dict

    def get_server_name(self) -> str | None:
        """
        Returns server name
        """

        data = self.get_info()
        if data:
            return data['ServerName']
        else:
            return None

    def get_short_code(self) -> str | None:
        """
        Returns server short code
        """

        data = self.get_info()
        if data:
            return data['ShortCode']
        else:
            return None

    def get_player_count(self) -> int | None:
        """
        Returns online player count
        """
        
        data = self.get_info()
        if data:
            return data['PlayerCount']
        else:
            return None

    def get_story_progress(self) -> str | None:
        """
        Returns game string indicating story progress
        """

        data = self.get_info()
        if data:
            return data['StoryProgress']
        else:
            return None

    def close(self):
        """
        Closes socket to server
        """

        self.socket.close()

if __name__ == "__main__":
    pass