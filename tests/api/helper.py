import base64

def user_hash(email, password):
    string = '{}:{}'.format(email, password)
    user_hash = base64.b64encode(bytes(string, 'ascii')).decode('ascii')
    user_hash = 'Basic {}'.format(user_hash)
    return user_hash
