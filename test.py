from rooter.database import Model, JsonDatabase

users_model = Model('users', {
    'id': {'type': 'int', 'auto_increment': True},
    'username': {'type': 'str'},
    'money': {'type': 'int', 'default': 10}
})
users_model.create()

db = JsonDatabase(table_name='users')