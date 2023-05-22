from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.db import transaction

from domains.entities.users_entity import AuthSessionEntity

from .models import (
    AuthSession,
)
from domains.interfaces.users_repository import (
    AuthRepository as AuthRepositoryInterface,
    AuthRepositoryContext,
)
from apps.users.exceptions import (
    EmailSendFailed,
)
from core.exceptions import DatabaseError

EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = settings.EMAIL_USE_TLS


class AuthRepository(AuthRepositoryInterface):
    queryset = AuthSession.objects.all()

    def __init__(self, context: AuthRepositoryContext):
        self.AuthSessionEntity = context['AuthSessionEntity']

    def send_email(self, email: str, code: int) -> None:
        template_path = 'email-code.html'
        context = {'code': code}
        html_message = render_to_string(template_path, context)

        with get_connection(
            host=EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL_HOST_USER,
            password=EMAIL_HOST_PASSWORD,
            use_tls=EMAIL_USE_TLS
        ) as connection:
            email_message = EmailMessage(
                subject="Knock account: Identify your code",
                body=html_message,
                from_email=EMAIL_HOST_USER,
                to=[email],
                connection=connection
            )
            email_message.content_subtype = 'html'
            status = email_message.send()
            if status != 1:
                raise EmailSendFailed()
    
    def save(self, **kwargs) -> None:
        instance: AuthSession = self.get_model_instance()

        if bool(instance):
            pass
        else:
            with transaction.atomic():
                instance = AuthSession.objects.create(**kwargs)
        
        return self.AuthSessionEntity(
            id=instance.pk,
            email=instance.email,
            emailCode=instance.email_code,
            exp=instance.exp,
            at=instance.at,
            attempt=instance.attempt
        )
    
    def find_by_email(self, email: str):
        try:
            instance = self.queryset.get(email=email)
            self.set_model_instance(instance)
            return self.AuthSessionEntity(
                id=instance.pk,
                email=instance.email,
                emailCode=instance.email_code,
                exp=instance.exp,
                at=instance.at,
                attempt=instance.attempt
            )
        except AuthSession.DoesNotExist:
            return None
    
    def delete(self) -> None:
        obj: AuthSession = self.get_model_instance()
        try:
            obj.delete()
            self.set_model_instance(None)

        except Exception as e:
            raise DatabaseError(e)
