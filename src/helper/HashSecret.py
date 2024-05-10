import hashlib
import hmac
import base64

def calculate_secret_hash(client_id, client_secret, username):
    message = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'), msg=str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

