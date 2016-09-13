import requests
import json

host = 'http://oep.iks.cs.ovgu.de'
name = "MartinGlauer"

def create_table():
    data = { 'schema': 'workshop', 
        'table': 'workshop_'+name.lower(),
        'fields':[
            {'name': 'id', 'type':'BIGSERIAL', 'pk':True},
            {'name': 'name', 'type': 'VARCHAR(100)'},
            {'name': 'affiliation', 'type': 'VARCHAR(100)'},
            {'name': 'source', 'type': 'BIGINT'},
        ], 
        'constraints':{
            'fk':[
                {
                    'names':['source'],
                    'schema': 'reference',
                    'table': 'entries',
                    'fields': ['entries_id']
                }
            ]
        }
    }

    res= requests.post(host+'/api/create', data={'query':json.dumps(data)})
    print(res)
    
def search_data():
    data = { 
        'from':[{
            'type': 'table',
            'schema': 'workshop', 
            'table': 'workshop_'+name.lower()
        }],
        'fields':[
            _get_column_query('id'),
            _get_column_query('name'),
            _get_column_query('affiliation'),
            _get_column_query('source'),
        ],
        'order_by':[
        {
            'type': 'column',
            'column': 'id',
            'ordering': 'desc'
        }]
    }
    
    res = requests.post(host+'/api/search', data={'query':json.dumps(data)})
    for row in res:
        print(row)

def insert_data():
    rows = [
        {'name':'Max Mustermann', 'affiliation':'OvGU', 'source':'1'},
        {'name':'John Doe', 'affiliation':'RLI', 'source':'2'},
        {'name':'Petra Mustermann', 'affiliation':'ZNES', 'source':'3'}]


    data = { 'schema': 'workshop', 
        'table': 'workshop_'+name.lower(),
        'values': rows,
    }
    
    res = requests.post(host+'/api/insert', data={'query':json.dumps(data)})
    print(res)
    
    
def _get_column_query(name):
    return {
        'type': 'column',
        'column': name,
    }
    
#create_table()    
#insert_data()
search_data()
