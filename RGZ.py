from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

contacts = {}
next_id = 1

@app.route('/contacts', methods=['POST'])
@swag_from({
    'tags': ['Contacts'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'phone': {'type': 'string'}
                },
                'required': ['name', 'phone']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Контакт создан',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'phone': {'type': 'string'}
                }
            }
        }
    }
})
def create_contact():
    global next_id
    data = request.json
    contact = {'id': next_id, 'name': data['name'], 'phone': data['phone']}
    contacts[next_id] = contact
    next_id += 1
    return jsonify(contact), 201

@app.route('/contacts/<int:contact_id>', methods=['GET'])
@swag_from({
    'tags': ['Contacts'],
    'parameters': [
        {
            'name': 'contact_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Идентификатор контакта'
        }
    ],
    'responses': {
        200: {
            'description': 'Информация о контакте',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'phone': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Контакт не найден'}
    }
})
def get_contact(contact_id):
    contact = contacts.get(contact_id)
    if contact:
        return jsonify(contact)
    return jsonify({'error': 'Контакт не найден'}), 404

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Contacts'],
    'parameters': [
        {
            'name': 'contact_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Идентификатор контакта'
        }
    ],
    'responses': {
        200: {
            'description': 'Контакт удалён'
        },
        404: {
            'description': 'Контакт не найден'
        }
    }
})
def delete_contact(contact_id):
    if contact_id in contacts:
        del contacts[contact_id]
        return jsonify({'message': 'Контакт удалён'})
    return jsonify({'error': 'Контакт не найден'}), 404

if __name__ == '__main__':
    app.run(debug=False)