# obtenemos la clase del recurso que tenemos en el archivo example.py para utilizarlo en un endpoint
#from v1.resources.example.example import Role
from v1.resources.methods.pymongo import EndPoint1, EndPoint2, EndPoint3
from v1.resources.methods.Crud_methods import Model1_CRUD, Model1_GETALL, zendesk_CRUD

def initialize_routes(api):
    '''
    En el endpoint le indicamos el recurso keycloak a utilizar
    con el formato "auth:nombrerecurso:explicacion_corta"
    '''
    #api.add_resource(Role, '/role', endpoint='auth:flask_base:dev', methods=['GET','POST',])
    api.add_resource(EndPoint1, '/endpoint1', endpoint='auth:recurso1', methods=['GET',])
    api.add_resource(EndPoint2, '/endpoint2', endpoint='auth:recurso2', methods=['GET',])
    api.add_resource(EndPoint3, '/endpoint3', endpoint='auth:recurso3', methods=['GET',])
    api.add_resource(Model1_CRUD, '/model1', endpoint='auth:recurso6', methods=['GET', 'POST'])
    api.add_resource(Model1_GETALL, '/modelgetall', endpoint='auth:recurso5', methods=['GET','POST'])
    api.add_resource(zendesk_CRUD, '/modelZD', endpoint='auth:recurso4', methods=['GET', 'POST', 'PUT', 'DELETE'])
