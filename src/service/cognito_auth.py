from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from src.helper.HashSecret import calculate_secret_hash

# from jose.backends.cryptography_backend import CryptographyBackend
from jose.constants import ALGORITHMS
import jose.jwt
from src.serializers.Parent.ParentSerializer import ParentSerializer
from src.serializers.Driver.DriverSerializers import DriverSerializer
import boto3
from src.models import Parent
User = get_user_model()
USER_POOL_ID = "ap-southeast-2_v5GOMajxt"
CLIENT_ID = "7trefn6t6c6o2at9cvtffeatit"

class CognitoAuthenticationBackend(BaseBackend):
    def create_user(self, email, password, username, type):
        client = boto3.client('cognito-idp')

        try:
            response = client.sign_up(
                ClientId= CLIENT_ID,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    # Các thuộc tính người dùng khác nếu cần
                ],
                ValidationData=[
                    {'Name': 'email', 'Value': email},
                    # Dữ liệu xác minh khác nếu cần
                ]
            )
            
            print(f"User created: {response}")

            
                
            response_data = {
                'status_code': 200,
                'id': response['UserSub']
            }
            return response_data


        except client.exceptions.UserNotFoundException:
            print("User pool not found")
            return {'error': 'User pool not found'}

        except client.exceptions.UsernameExistsException as e:
            error_message = e.response['Error']['Message']
            print(f"Username {username} already exists: {error_message}")
            return {'error':f"Username {username} already exists: {error_message}"}

        except Exception as e:
            print(f"Error creating user: {e}")
            return {'error': str(e)}
            
    def login(self, request, email, password):
    # Khởi tạo Cognito client
        client = boto3.client('cognito-idp')

        try:
            # Xác thực người dùng với Cognito
            response = client.admin_initiate_auth(
                UserPoolId=USER_POOL_ID,
                ClientId=CLIENT_ID,
                AuthFlow='ADMIN_USER_PASSWORD_AUTH',  # Thay đổi AuthFlow thành USER_SRP_AUTH
                AuthParameters={
                    'USERNAME': email,  
                    'PASSWORD': password,
                }
            )

            # Nếu xác thực thành công, giải mã và trả về thông tin người dùng
            if 'AuthenticationResult' in response:
                return response
            
            else:
                return response

        except client.exceptions.NotAuthorizedException as e:
            print("Not authorized:", e)
            return {"error": "Not authorized"}
        except client.exceptions.UserNotFoundException as e:
            print("User not found:", e)
            return {"error": "User not found"}
        except client.exceptions.UserNotConfirmedException as e:
            print("User not confirmed:", e)
            return {"error": "User not confirmed"}
        except Exception as e:
            print("Error logging in:", e)
            return { "error": "exception error" }

        return None
    def change_password(self, access_token, old_password, new_password):
        # Khởi tạo Cognito client
        client = boto3.client('cognito-idp')

        try:
            response = client.change_password(
                AccessToken=access_token,
                PreviousPassword=old_password,
                ProposedPassword=new_password
            )

            # In thông báo sau khi thay đổi mật khẩu
            print(f"Password changed successfully {response}")

            return response

        except client.exceptions.UserNotFoundException as e:
            print("User not found:", e)
            return ("User not found:")

        except client.exceptions.NotAuthorizedException as e:
            print("Not authorized:", e)
            return ("Not authorized:")

        except client.exceptions.LimitExceededException as e:
            print("Limit exceeded:", e)
            return ("Limit exceeded:")

        except client.exceptions.InternalErrorException as e:
            print("Internal error:", e)
            return ("Internal error:")

        except client.exceptions.InvalidParameterException as e:
            print("Invalid parameter:", e)
            return ("Invalid parameter:")

        except client.exceptions.InvalidPasswordException as e:
            print("Invalid password:", e)
            return ("Invalid password:")

        except client.exceptions.PasswordResetRequiredException as e:
            print("Password reset required:", e)
            return ("Password reset required:")

        except client.exceptions.ResourceNotFoundException as e:
            print("Resource not found:", e)
            return ("Resource not found:")

        except client.exceptions.TooManyRequestsException as e:
            print("Too many requests:", e)
            return ("Too many requests:")

        except Exception as e:
            print("Error changing password:", e)
            return ("Error changing password:")
    def confirm_otp(self, email, code):
        client = boto3.client('cognito-idp')
        try:
            response = client.confirm_sign_up(
                ClientId=CLIENT_ID,
                Username=email,
                ConfirmationCode=code,
                ForceAliasCreation=False  # Hoặc True nếu bạn muốn bắt buộc tạo alias
            )
            return response
        except client.exceptions.UserNotFoundException as e:
            print("User not found:", e)
            return "User not found"
        except client.exceptions.NotAuthorizedException as e:
            print("Not authorized:", e)
            return "Not authorized"
        except client.exceptions.LimitExceededException as e:
            print("Limit exceeded:", e)
            return "Limit exceeded"
        except client.exceptions.InternalErrorException as e:
            print("Internal error:", e)
            return "Internal error"
        except client.exceptions.InvalidParameterException as e:
            print("Invalid parameter:", e)
            return "Invalid parameter"
        except Exception as e:
            print("An unexpected error occurred:", e)
            return "An unexpected error occurred: " + str(e)
    def forgot_password(self, email):
        client = boto3.client('cognito-idp')
        try:
            response = client.forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
        )
            return response
        
        except client.exceptions.UserNotFoundException as e:
            print("User not found:", e)
            return "User not found"
        except client.exceptions.NotAuthorizedException as e:
            print("Not authorized:", e)
            return "Not authorized"
        except client.exceptions.LimitExceededException as e:
            print("Limit exceeded:", e)
            return "Limit exceeded"
        except client.exceptions.InternalErrorException as e:
            print("Internal error:", e)
            return "Internal error"
        except client.exceptions.InvalidParameterException as e:
            print("Invalid parameter:", e)
            return "Invalid parameter"
        except Exception as e:
            print("An unexpected error occurred:", e)
            return "An unexpected error occurred: " + str(e)
    def confirm_forgot_password(self, email, code, password):
        client = boto3.client('cognito-idp')
        try:
            response = client.confirm_forgot_password(
                ClientId=CLIENT_ID,
                Username=email,
                ConfirmationCode=code,
                Password=password
            )
            return response
        except client.exceptions.UserNotFoundException as e:
            print("User not found:", e)
            return "User not found"
        except client.exceptions.NotAuthorizedException as e:
            print("Not authorized:", e)
            return "Not authorized"
        except client.exceptions.LimitExceededException as e:
            print("Limit exceeded:", e)
            return "Limit exceeded"
        except client.exceptions.InternalErrorException as e:
            print("Internal error:", e)
            return "Internal error"
            
    def resend_confirmation_code(self, email):
        client = boto3.client('cognito-idp')
        try:
            response = client.resend_confirmation_code(
                ClientId=CLIENT_ID,
                Username=email
            )
            return response
        except client.exceptions.UserNotFoundException as e:
            print("User not found:", e)
            return "User not found"
        except client.exceptions.NotAuthorizedException as e:
            print("Not authorized:", e)
            return "Not authorized"
        except client.exceptions.LimitExceededException as e:
            print("Limit exceeded:", e)
            return "Limit exceeded"
        except client.exceptions.InternalErrorException as e:
            print("Internal error:", e)
            return "Internal error"
        