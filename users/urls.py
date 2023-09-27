from django.urls import path
from .views import RegisterView, UpdateView, UserView, ListUserView, AssignUserToGroup, GroupList, GroupDetail, GroupCreate, GroupUpdate, GroupDelete
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    # -------- URL API -----------
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/user/update/<int:pk>/', UpdateView.as_view(), name='update'),
    path('api/user/delete/<int:pk>/', UserView.as_view(), name='delete'),
    path('api/user/list/', ListUserView.as_view(), name='list_user'),
    
    #url group
    path('api/groups/list_group/', GroupList.as_view(), name='group-list'),
    path('api/groups/detail_group/<int:pk>/', GroupDetail.as_view(), name='group-detail'),
    path('api/groups/create/', GroupCreate.as_view(), name='group-create'),
    path('api/groups/update/<int:pk>/', GroupUpdate.as_view(), name='group-update'),
    path('api/groups/delete/<int:pk>/', GroupDelete.as_view(), name='group-delete'),
    path('api/assign/<int:user_id>/<int:group_id>', AssignUserToGroup.as_view() , name='assign_user_to_group'),
]