from src import create_app
from flask_restful import Api
from src.views import VistaSignUp, VistaPong

application = create_app('default')
app_context = application.app_context()
app_context.push()

api = Api(application)
api.add_resource(VistaSignUp, '/api/signup')
api.add_resource(VistaPong, '/')

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 3000, debug = False)