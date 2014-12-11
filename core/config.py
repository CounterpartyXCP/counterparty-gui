
class Config:
    def __init__(self, args=None):
        self.args = args

        self.TESTNET = True
        
        self.PLUGINS = ['send', 'test']

        self.BACKEND_RPC_USER = 'rpc'
        self.BACKEND_RPC_PASSWORD = 'pass'
        self.BACKEND_RPC_CONNECT = 'jahpowerbit.org'
        self.BACKEND_RPC_PORT = 14000
        self.BACKEND_RPC_SSL = False
        self.BACKEND_RPC_SSL_VERIFY = False

        self.BACKEND_RPC_PROTOCOL = 'https' if self.BACKEND_RPC_SSL else 'http'

        self.BACKEND_RPC = '{}://{}:{}@{}:{}'.format(self.BACKEND_RPC_PROTOCOL, self.BACKEND_RPC_USER, self.BACKEND_RPC_PASSWORD, self.BACKEND_RPC_CONNECT, self.BACKEND_RPC_PORT) 