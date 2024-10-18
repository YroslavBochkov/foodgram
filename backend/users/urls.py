from django.urls import path
from api.views import SignUpViewSet, TokenApiView

auth_urls = [
    path('signup/', SignUpViewSet.as_view(), name='signup'),
    path('token/', TokenApiView.as_view(), name='token'),
]
