from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users_management import settings
from .serializers import RegisterSerializer, UserListSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GroupSerializer
from users import serializers
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
BASE_URL=settings.BASE_URL


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UpdateView(generics.UpdateAPIView):
    queryset =User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'pk'
    def perform_update(self, serializer):
        serializer.validated_data.get('password')
        serializer.validated_data.get('email')
        serializer.validated_data.get('first_name')
        serializer.validated_data.get('last_name') 
        serializer.save()
    
class UserView(APIView):
      queryset = User.objects.all()
      def delete(self,pk):
        user=User.objects.filter(id=pk)
        if len(user)<=0:
            raise Exception("User does not exist")
        user[0].delete()
        return HttpResponse("user deleted")

class ListUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer

@api_view(['POST'])
def GroupCreate(request):
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    #list
class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupCreate(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#update group
class GroupUpdate(generics.UpdateAPIView):
    queryset = Group.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    lookup_field = 'pk'
    def perform_update(self, serializer):    
        serializer.validated_data.get('name_group')
        serializer.save()
#delete group
class GroupDelete(generics.DestroyAPIView):
    queryset = Group.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    def delete(self):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Group deleted successfully."}, status=204)
    

class GroupView(APIView):
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name_group']
            return Response({"message": "Group name is valid: " + name}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignUserToGroup(APIView):
    def post(self,request, user_id, group_id):
        try:
            user = User.objects.get(pk=user_id)
            groupe = Group.objects.get(pk=group_id)
            print(user)
            print(groupe)
        except User.DoesNotExist:
            return Response({"detail": "L'utilisateur n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist:
            return Response({"detail": "Le groupe n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)
        user.groups.add(groupe)
        user.save()
        return Response({"detail": f"L'utilisateur avec l'ID {user_id} a été assigné au groupe avec l'ID {group_id}."}, status=status.HTTP_200_OK)

class PasswordReset(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """
    serializer_class = serializers.EmailSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializers2 = serializers.EmailSerializer(data=request.data)
        if serializers2.is_valid():
            email = serializers2.data["email"]
            user = User.objects.filter(email=email).first()
            print(user)
            if user:
                encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
                token = PasswordResetTokenGenerator().make_token(user)
                reset_url = reverse(
                    "reset-password",
                    kwargs={"encoded_pk": encoded_pk, "token": token},
                )
                reset_link = f"{BASE_URL}/new_password/{encoded_pk}/{token}"
                #request.session['lien'] = reset_link

                # --------
                subject = 'MOT DE PASSE OUBLIE'
                recipient_list = [email]
                template_name = 'email_template.html'
                context = {'username': user, 'verification_link': reset_link}
                html_message = render_to_string(template_name, context) 
                # Strip the HTML tags to create a plain text version
                plain_message = strip_tags(html_message)

                # Send the email
                send_mail(subject, plain_message, None, recipient_list, html_message=html_message)
                #---------
                return Response( [ {
                        "lien": reset_link,
                        "code":  status.HTTP_200_OK,
                        "message": "Lien de confirmation bien envoyer",
                        "success":True
                }],status=status.HTTP_200_OK)
            else:
                return Response(
                    [
                        {
                        "code":  status.HTTP_400_BAD_REQUEST,
                        "message": "User doesn't exists",
                        "success":False
                        }
                    ], status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({"message":serializers2.errors,"status":404,"success":False})
class ResetPasswordAPI(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = serializers.ResetPasswordSerializer

    def put(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return Response([ 
            {
             "code": status.HTTP_200_OK,
             "message": "Password reset complete",
             "success": True
            }
        ]
        )    
    
class UserProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)