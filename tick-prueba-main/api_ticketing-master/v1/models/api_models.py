#from email.policy import default
#from msilib.schema import CheckBox
#from xmlrpc.client import boolean
from email.policy import default
from mongoengine import Document, DynamicDocument
from mongoengine import StringField, BooleanField, IntField


class Model1(Document):

    status = {
        'New':'New',
        'Open':'Open',
        'Pending':'Pending',
        'On-hold':'On-hold',
        'Solved':'Solved',
        'Closed':'Closed'
    }

    type = {
        'Question':'Question',
        'Incident':'Incident',
        'Problem':'Problem',
        'Link':'Link',
        'Task':'Task'
    }

    priority = {
        'Low':'Low',
        'Normal':'Normal',
        'High':'High',
        'Urgent':'Urgent'
    }

    Requester = StringField(max_length=128, required=True)
    Follower = StringField(max_length=128, required=False)
    Asignee = StringField(max_length=128, required=True)
    Share = BooleanField(default = True, required=True)
    Subject = StringField(max_length=150, required=True)
    Description = StringField(max_length=1000, required=True)
    Status = StringField(max_length=7, choices=status.keys(), Required=True)
    Type = StringField(max_length=8,choices=type.keys(), required=True)
    Priority = StringField(max_length=6, choices=priority.keys(), required=True)


class Model2(DynamicDocument):
    meta = {'collection': 'model2'}


class ModelZD(Document):

    sistema = {
        'Zendesk':'Zendesk',
        'OTRS':'OTRS'
    }
    Id = IntField(primary_key=True)
    Sistema = StringField(max_length=128, choices=sistema.keys(), required=True)
    Requester = StringField(max_length=128, required=True)
    Email = StringField(max_length=128, required=True)
    Subject = StringField(max_length=150, required=True)
    Description = StringField(max_length=1000, required=True)
    Comment1 = StringField(max_length=1000, required=False)