from django.urls import path, include
from ..v1.views.user_view import (
    CustomTokenObtainPairView, 
    UserRegisterView,
    VerifyUserAccount
)

app_name = "user"  

company_url_register_with_code = [
    # v1 registration
    path('register/', UserRegisterView.as_view(), name='registration-company-v1'),
    path('verify/', VerifyUserAccount.as_view(), name='company-verify-v1'),

]






urlpatterns = [
    # custom token refresh and access with email
    path('profile/token', CustomTokenObtainPairView.as_view(), name='custom-token'),
    path('profile/', include(company_url_register_with_code)),


]