
from src.serializers.Driver.DriverSerializers import DriverSerializer
from src.serializers.Parent.ParentSerializer import ParentSerializer


def create_new_user(id, username, type, email,phone_number,day_of_birth):
    data = {
        'id': id,
        'email': email,
        'user_name': username,
        'language': 'en',
    }
    if type == 'driver':
        data['phone_number'] = phone_number
        data['date_of_birth'] = day_of_birth
    serializer_class = ParentSerializer if type == 'parent' else DriverSerializer
    try:
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        print(f"Error creating {type}: {e}")

