import socket
import pickle
import time

class Network:
    """Network class for managing client-side socket connections in a chess game.
    This class handles all network-related operations including establishing connections,
    sending/receiving data, and managing the game board state through socket communication.
    Attributes:
        client (socket): Socket object for client-side connection
        host (str): Server hostname, default is "localhost"
        port (int): Server port number, default is 5555
        addr (tuple): Tuple containing host and port for connection
        board (object): Game board state received from server after connection
    Raises:
        socket.error: If connection or data transmission fails
        Exception: If there are issues with data serialization/deserialization
    """
    
    def __init__(self):
        """
        Initializes the Network class with default host and port values.

        Args:
            None
        Returns:
            None
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.board = self.connect()
        self.board = pickle.loads(self.board)

    def connect(self):
        """
        Connects to the server and receives the initial game board state.

        Args:
            None
        Returns:
            str: Serialized game board state
        """
        self.client.connect(self.addr)
        return self.client.recv(4096*8)

    def disconnect(self):
        """
        Disconnects the client from the server.

        Args:
            None
        Returns:
            None
        """
        self.client.close()

    def send(self, data, pick=False):
        """ 
        Sends data to the server and receives a response.
        This function sends data to the server and waits for a response.
        
        Args:
            data (str): Data to send to the server
            pick (bool): Whether to pickle the data before sending
        Returns:
            str: Response data from the server
        """
        start_time = time.time()
        while time.time() - start_time < 5:
            try:
                if pick:
                    self.client.send(pickle.dumps(data))
                else:
                    self.client.send(str.encode(data))
                reply = self.client.recv(4096*8)
                try:
                    reply = pickle.loads(reply)
                    break
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)


        return reply


