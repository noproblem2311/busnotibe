
from src.serializers.Driver.DriverSerializers import DriverSerializer
from src.serializers.Parent.ParentSerializer import ParentSerializer
from src.serializers.Admin.AdminSerializer import AdminSerializer



def create_new_user(id, username, type, email,phone_number,day_of_birth):
    data = {
        'id': id,
        'email': email,
        'user_name': username,
        'language': 'en',
    }
    data_admin = {
        'id': id,
        'email': email,
        'user_name': username,
    }
    if type == 'driver':
        data['phone_number'] = phone_number
        data['date_of_birth'] = day_of_birth
    serializer_class = ParentSerializer if type == 'parent' else (DriverSerializer if type == 'driver' else AdminSerializer)
    datareal= data if type != 'admin' else data_admin
    try:
        serializer = serializer_class(data=datareal)
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        print(f"Error creating {type}: {e}")

