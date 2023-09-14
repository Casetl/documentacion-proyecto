from src import create_app
from flask_restful import Api
from .views import VistaSignUp

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaSignUp, '/api/signup')