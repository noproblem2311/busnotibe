import json
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from src.serializers.auth.ForgotPasswordSerializer import ForgotPasswordSerializer, ConfirmForgotPasswordSerializer
from src.helper.AddNewUserAfterSignUp import create_new_user
from src.service.cognito_auth import CognitoAuthenticationBackend
from src.serializers.auth.AuthSerializer import ResendConfirmationCodeSerializer, UserSerializer,LoginSerializer,ChangePasswordSerializer,RespondToNewPasswordChallengeSerializer
from src.models import Parent,Driver 
cognito_backend = CognitoAuthenticationBackend()
@api_view(['POST'])
def change_password_view(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            access_token = request.headers.get('Authorization')
            previous_password = serializer.validated_data.get('previous_password')
            proposed_password = serializer.validated_data.get('proposed_password')

            # Thực hiện thay đổi mật khẩu
            response = cognito_backend.change_password(access_token, previous_password, proposed_password)
            
            return Response(response)
        else:
            # Dữ liệu không hợp lệ, trả về phản hồi lỗi
            return Response(serializer.errors, status=400)
        
@api_view(['POST'])
def confirm_otp(request):
    if request.method == 'POST':
        serializer = RespondToNewPasswordChallengeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            email = serializer.validated_data.get('email')

            # Thực hiện phản hồi cho thách thức mật khẩu mới yêu cầu
            response = cognito_backend.confirm_otp(email, code)
            # if "User not found" in response:
            #     return Response({'error': 'User not found'}, status=401)
            # elif "Not authorized" in response:
            #     return Response({'error': 'Not authorized'}, status=401)
            # elif "Limit exceeded" in response:
            #     return Response({'error': 'Limit exceeded'}, status=401)
            # elif "Internal error" in response:
            #     return Response({'error': 'Internal error'}, status=401)
            # elif "An unexpected error occurred: " in response:
            #     return Response({'error': 'An unexpected error occurred'}, status=401)
            
            if isinstance(response, tuple):  # Nếu user là một tuple chứa thông điệp lỗi
                error_message = response[0]  # Lấy thông điệp lỗi từ tuple
                return Response({'error': error_message}, status=401)  # Trả về thông điệp lỗi với status code tương ứng
            
            return Response(response)
        else:
            # Dữ liệu không hợp lệ, trả về phản hồi lỗi
            return Response(serializer.errors, status=400)
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            type = serializer.validated_data.get('type')

            # Thực hiện xác thực người dùng
            user = cognito_backend.login(request, email, password)
            
            if 'AuthenticationResult' in user and 'AccessToken' in user['AuthenticationResult']:
                user['user'] = {
                    'error': 'User does not exist',
                }
                if type == 'parent':
                    parent = Parent.objects.filter(email=email).first()
                    if parent:
                        user['user'] = {
                            'id': parent.id,
                            'user_name': parent.user_name,
                            'email': parent.email,
                            'avatar': parent.avatar,
                            'date_of_birth': parent.date_of_birth,
                            'language': parent.language,
                        }
                elif type == 'driver':
                    driver = Driver.objects.filter(email=email).first()
                    if driver:
                        user['user'] = {
                            'id': driver.id,
                            'email': driver.email,
                            'avatar': driver.avatar,
                            'user_name': driver.user_name,
                            'date_of_birth': driver.date_of_birth,
                            'company': driver.company,
                            'license': driver.license,
                            'phone_number': driver.phone_number,
                            'bus_number': driver.bus_number,
                            'language': driver.language,
                        }

                return Response(user, status=200)
            
            if 'ChallengeName' in user and user['ChallengeName']:
                return Response(user)
            
            return Response(user['error'], status=401)


        else:
            # Dữ liệu không hợp lệ, trả về phản hồi lỗi
            return Response(serializer.errors, status=400)


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            username = serializer.validated_data.get('username')
            type = serializer.validated_data.get('type')
            phone_number = serializer.validated_data.get('phone_number')
            day_of_birth = serializer.validated_data.get('date_of_birth')

            # Tạo người dùng mới trong Cognito
            cognito_backend = CognitoAuthenticationBackend()
            response = cognito_backend.create_user(email, password, username, type)
            if 'status_code' in response and response['status_code'] == 200:
                create_new_user(response['id'], username, type, email, phone_number,day_of_birth)
                return Response(response)
            # Trả về phản hồi thành công sau khi đăng ký
            if 'error' in response:
                return Response(response['error'], status=400)
        else:
            # Dữ liệu không hợp lệ, trả về phản hồi lỗi
            return Response(serializer.errors, status=400)

@api_view(['POST'])
def forgot_password_view(request):
    if request.method == 'POST':
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            # Thực hiện thay đổi mật khẩu
            response = cognito_backend.forgot_password(email)
            return Response(response)
        else:
            # Dữ liệu không hợp lệ, trả về phân hồi lỗi
            return Response(serializer.errors, status=400)
@api_view(['POST'])
def confirm_forgot_password_view(request):
    if request.method == 'POST':
        serializer = ConfirmForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            code = serializer.validated_data.get('code')
            password = serializer.validated_data.get('password')

            # Thực hiện thay đổi mật không
            response = cognito_backend.confirm_forgot_password(email, code, password)
            return Response(response)
        else:
            # Dữ liệu không hợp lệ, trả về phân hồi lỗi
            return Response(serializer.errors, status=400)
        
@api_view(['POST'])
def resend_confirmation_code(request):
    if request.method == 'POST':
        serializer = ResendConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            # Thực hiện thay đổi mật không
            response = cognito_backend.resend_confirmation_code(email)
            return Response(response)
        else:
            # Dữ liệu không hợp lệ, trả về phân hồi lỗi
            return Response(serializer.errors, status=400)