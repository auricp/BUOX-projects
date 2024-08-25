from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer

from collections import namedtuple
from io import BytesIO
from socket import error as socket_error


# using exceptions to notify the connection-handling loop of any problems
class CommandError(Exception): pass
class Disconnect(Exception): pass

Error = namedtuple('Error', ('message',))


class ProtocolHandler(object):
    def handle_request(self, socket_file):
        '''
        Parse a request from the client to its component parts
        
        :param socket_file:
        '''
        pass
    
    def write_response(self, socket_file, data):
        '''
        Serialize the response data and send it to the client
        
        :param socket_file:
        :param data:
        '''
        pass
    
    
class Server(object):
    def __init__(self, host='127.0.0.1', port=31337, max_clients=64):
        self._pool = Pool(max_clients)
        self._server = StreamServer(
            (host, port),
            self.connection_handler,
            spawn=self._pool)
    
        self._protocol = ProtocolHandler()
        self._kv = {}
    
    def connection_handler(self, conn, address):
        # Conver conn (a socket object) into a file like object
        socket_file = conn.makefile('rwb')
    
        

