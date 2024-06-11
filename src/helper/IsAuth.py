


import jwt


def isAuth(request):
    Authorization = request.headers.get('Authorization')
    if not Authorization:
        return False
    token = Authorization.split(" ")[1]
    # decode token
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    return True
    