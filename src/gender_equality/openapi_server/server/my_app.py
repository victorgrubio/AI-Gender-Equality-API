from openapi_server import encoder
from openapi_server.server.server import BaseServer


class MyApp(BaseServer):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(MyApp, self).__init__()

    def main(self, port=5000):
        self.add_api(encoder)
        self.run_server(port)
        self.kill()


app = MyApp()
app.init_server('../openapi/')
application = app.server.app

if __name__ == "__main__":
    app.main()
