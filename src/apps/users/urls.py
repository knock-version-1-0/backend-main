from core.routers import Router

from django.urls import path, include
from . import views

from di.users_factory import (
    AuthFactory,
)

router = Router()

router.register(
    '', views.EmailSendViewSet, basename='auth-email-send', factory=AuthFactory()
)


urlpatterns = [
    path('auth/email-send/', include(router.urls)),
]
