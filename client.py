import socket
import pickle
import time

class Network:
    
    def __init__(self):
        """
        Initializes the Network class with default __host and __port values.

        Args:
            None
        Returns:
            None
        """
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = "local__host"
        self.__port = 5555
        self.__addr = (self.__host, self.__port)
        self.__board = self.connect()
        self.__board = pickle.loads(self.__board)

    def connect(self):
        """
        Connects to the server and receives the initial game __board state.

        Args:
            None
        Returns:
            str: Serialized game __board state
        """
        self.__client.connect(self.__addr)
        return self.__client.recv(4096*8)

    def disconnect(self):
        """
        Disconnects the __client from the server.

        Args:
            None
        Returns:
            None
        """
        self.__client.close()

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
                    self.__client.send(pickle.dumps(data))
                else:
                    self.__client.send(str.encode(data))
                reply = self.__client.recv(4096*8)
                try:
                    reply = pickle.loads(reply)
                    break
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)


        return reply


