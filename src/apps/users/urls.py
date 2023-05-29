from core.routers import Router

from django.urls import path, include
from . import views

from di.users_factory import (
    AuthFactory,
    UserFactory
)

auth_email_router = Router()
auth_email_router.register(
    '', views.AuthEmailViewSet, basename='auth-email', factory=AuthFactory()
)

auth_verification_router = Router()
auth_verification_router.register(
    '', views.AuthVerificationViewSet, basename='auth-verification', factory=AuthFactory()
)

user_router = Router()
user_router.register(
    '', views.UserListViewSet, basename='users', factory=UserFactory()
)


urlpatterns = [
    path('auth/email/', include(auth_email_router.urls)),
    path('auth/verification', include(auth_verification_router.urls)),
    path('users/', include(user_router.urls))
]
