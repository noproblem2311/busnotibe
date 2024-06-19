
import jwt

def getUserId(request):
    Authorization = request.headers.get('Authorization')
    if not Authorization:
        return False
    token = Authorization.split(" ")[1]
    if not token:
        return False
    # decode token
    try:
        payload = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})     
        return payload.get("username")
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    