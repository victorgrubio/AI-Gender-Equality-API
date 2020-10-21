import sys
import connexion
# Temporarily added CORS origing "*" to allow HTML/JS local client
from flask_cors import CORS
from openapi_server.server.app import BaseApp
# from openapi_server.server.models import db
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager

class BaseServer(BaseApp):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        JUST A SERVER OBJECT TO RUN
        '''
        super().__init__()
        self.server = None

    def init_server(self, specification_dir='..'):
        self.server = connexion.App(
            sys.modules[self.__class__.__module__].__name__,
            specification_dir=specification_dir)
        self.server.app.config.from_object('config.ProductionConfig')
#         self.init_db()
#         self.jwt = JWTManager(self.server.app)

    def add_api(self, encoder):
        self.server.app.json_encoder = encoder.JSONEncoder
        self.server.add_api('openapi.yaml',
                            arguments={
                                'title': 'Visiona Face Recognition REST API'})
        # No CORS requests on the type of server
        CORS(self.server.app, resources={r"/v1/*": {"origins": "*"}})

#     def init_db(self):
#         self.db = db
#         with self.server.app.app_context():
#             self.db.init_app(self.server.app)
#             self.db.create_all()
#             self.migrate = Migrate(self.server.app, self.db)

    def run_server(self, port):
        if self.server is None:
            raise RuntimeError("Server not initialised")
        self.server.run(port=port)
