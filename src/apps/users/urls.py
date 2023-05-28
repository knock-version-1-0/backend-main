from core.routers import Router

from django.urls import path, include
from . import views

from di.users_factory import (
    AuthFactory,
    UserFactory
)

auth_email_router = Router()

auth_email_router.register(
    '', views.EmailSendViewSet, basename='auth-email', factory=AuthFactory()
)

user_router = Router()

user_router.register(
    '', views.UserListViewSet, basename='users', factory=UserFactory()
)


urlpatterns = [
    path('auth/email/', include(auth_email_router.urls)),
    path('users/', include(user_router.urls))
]
