from core.routers import Router

from django.urls import path, include
from . import views

from di.users_factory import (
    AuthSessionFactory,
    UserFactory,
    AuthTokenFactory,
)

auth_email_router = Router()
auth_email_router.register(
    '', views.AuthEmailViewSet, basename='auth-email', factory=AuthSessionFactory()
)

auth_verification_router = Router()
auth_verification_router.register(
    '', views.AuthVerificationViewSet, basename='auth-verification', factory=AuthSessionFactory()
)

auth_token_router = Router()
auth_token_router.register(
    '', views.AuthTokenViewSet, basename='auth-token', factory=AuthTokenFactory()
)

user_router = Router()
user_router.register(
    '', views.UserListViewSet, basename='users', factory=UserFactory()
)

user_me_router = Router()
user_me_router.register(
    '', views.UserMeListViewSet, basename='users-me', factory=UserFactory()
)


urlpatterns = [
    path('auth/email/', include(auth_email_router.urls)),
    path('auth/verification/', include(auth_verification_router.urls)),
    path('auth/token/', include(auth_token_router.urls)),
    path('users/', include(user_router.urls)),
    path('users/me/', include(user_me_router.urls))
]
