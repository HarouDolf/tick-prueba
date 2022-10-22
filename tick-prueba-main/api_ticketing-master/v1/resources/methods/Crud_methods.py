# pylint: disable=invalid-name
# pylint: disable=line-too-long
#imports python base
import json
import logging
#import terceros
from flask import session, jsonify
from flask_restful import Resource, reqparse
from mongoengine.context_managers import switch_db
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, User
from zenpy.lib.api_objects import Comment

#Import del sistema
from v1.resources.auth.authorization import Auth
from v1.resources.auth.dbDecorator import dbAccess
from v1.models.api_models import Model1, ModelZD

creds = {
    'email' : 'contacto@bnet.cl',
    'password' : 'lj37hcw2',
    'subdomain': 'bnet6753'
}

# Default
zenpy_client = Zenpy(**creds)

logger = logging.getLogger(__name__)

class Model1_GETALL(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):
        with switch_db(ModelZD, session["dbMongoEngine"]):
            my_model = ModelZD.objects()
            if my_model:
                return jsonify(my_model.to_json())
        return "Objeto no encontrado", 400

class zendesk_CRUD(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Subject", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Description", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args()
        with switch_db(ModelZD, session["dbMongoEngine"]):
            my_model = ModelZD.objects(Subject=data['Subject']).first()
            my_model.Description = data['Description']
            my_model.save()
        return jsonify(my_model.to_json())

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Sistema", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Requester", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Email", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Subject", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Description", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args()
        if data['Sistema'] == 'Zendesk':
            try:
                with switch_db(ModelZD, session["dbMongoEngine"]) as my_collection:
                    my_model = my_collection(Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description'])
                    ticket_audit = zenpy_client.tickets.create(Ticket(requester=User(name=my_model.Requester, email=my_model.Email),subject=my_model.Subject, description=my_model.Description))
                    my_model = my_collection(Id=ticket_audit.ticket.id,Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description'] )
                    my_model.save()
            except Exception as err:
                logger.error(err)
            return jsonify(my_model.to_json())
        else:
            logger.error(err)
#            try:
#                with switch_db(ModelOTRS, session["dbMongoEngine"]) as my_collection:
#                    my_model = my_collection(Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description'])
#                    my_model.save()
#                    zenpy_client.tickets.create(Ticket(requester=User(name=my_model.Requester, email=my_model.Email),subject=my_model.Subject, description=my_model.Description))
#            except Exception as err:
#                logger.error(err)
#            return jsonify(my_model.to_json())
        
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self): #Se ejecutara este metodo con el metodo post del endpoint
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("Id")
        parser.add_argument("Comment1", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #obtenemos los datos de la request

        with switch_db(ModelZD, session["dbMongoEngine"]):
            my_model = ModelZD.objects(Id=data['Id']).first()
            my_model.Comment1 = data['Comment1']
            ticket = zenpy_client.tickets(id=my_model.Id)
            ticket.comment = Comment(body=my_model.Comment1, public=False)
            zenpy_client.tickets.update(ticket)
            my_model.save()
        return jsonify(my_model.to_json())
       
class Model1_CRUD(Resource): #Clase para crear recursos REST
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("Requester", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #obtenemos los datos de la request

        with switch_db(ModelZD, session["dbMongoEngine"]):
            my_model = ModelZD.objects(Requester=data['Requester'])
            if my_model:
               return jsonify(my_model.to_json())
        return "Objeto no encontrado", 400

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self): #Se ejecutara este metodo con el metodo post del endpoint
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("Id", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Comment", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #obtenemos los datos de la request

        with switch_db(ModelZD, session["dbMongoEngine"]):
            my_model = ModelZD.objects(Id=data['Id']).first()
            my_model.Comment1 = data['Comment']
            ticket = zenpy_client.tickets(id='Id')
            ticket.comment = Comment(body=my_model.Comment1, public=False)
            zenpy_client.tickets.update(ticket)
            my_model.save()
        return jsonify(my_model.to_json())

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def put(self):
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("Requester", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Follower", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Asignee", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Share", type=bool, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Subject", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Description", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Status", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Type", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Priority", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #obtenemos los datos de la request

        try:
            with switch_db(Model1, session["dbMongoEngine"]) as my_collection:
                my_model = my_collection(Requester=data['Requester'], Follower=data['Follower'], Asignee=data['Asignee'], Share=data['Share'], Subject=data['Subject'], Description=data['Description'], Status=data['Status'], Type=data['Type'], Priority=data['Priority'])
                my_model.save()
        except Exception as err:
            logger.error(err)
        return jsonify(my_model.to_json())

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def delete(self):
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("Requester", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #obtenemos los datos de la request

        with switch_db(Model1, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(Requester=data['Requester']).first()
            if not my_obj:
                return jsonify({'error': 'data not found'})
            my_obj.delete()
        return "Ok", 200

    #documentacion sobre requestParser https://flask-restful.readthedocs.io/en/latest/reqparse.html
    #documentacion sobre decoradores https://github.com/alloxentric/KeycloakAuth
    #docuemntacion sobre flask https://flask.palletsprojects.com/en/2.0.x/
    #documentacion sobre flask restful https://flask-restful.readthedocs.io/en/latest/
