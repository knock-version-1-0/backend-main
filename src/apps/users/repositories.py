from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import (
    AuthSession,
    User
)
from domains.interfaces.users_repository import (
    AuthRepository as AuthRepositoryInterface,
    AuthRepositoryContext,
    UserRepository as UserRepositoryInterface,
    UserRepositoryContext
)
from core.exceptions import DatabaseError
from apps.users.exceptions import (
    AuthSessionDoesNotExist,
    EmailAddrValidationError
)

EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = settings.EMAIL_USE_TLS


class AuthRepository(AuthRepositoryInterface):
    queryset = AuthSession.objects.all()

    def __init__(self, context: AuthRepositoryContext):
        self.AuthSessionEntity = context['AuthSessionEntity']

    def send_email(self, email: str, code: int) -> int:
        if settings.TEST_MODE:
            return 1
        
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
            return email_message.send()
    
    def save(self, **kwargs) -> None:
        instance: AuthSession = self.get_model_instance()
        try:
            if bool(instance):
                instance.update(**kwargs)
            else:
                with transaction.atomic():
                    _qs = self.queryset.filter(email=kwargs['email']).delete()
                    instance = self.queryset.create(**kwargs)

        except ValidationError as e:
            if 'email' in e.error_dict:
                raise EmailAddrValidationError()
            else:
                raise e

        except Exception as e:
            raise DatabaseError(e)
        
        return self.AuthSessionEntity(
            id=instance.pk,
            email=instance.email,
            emailCode=instance.email_code,
            exp=instance.exp,
            at=instance.at,
            attempt=instance.attempt
        )
    
    def find_by_id(self, id: str, *args, **kwargs):
        try:
            auth_session = self.queryset.get(id=id)
            self.set_model_instance(auth_session)
            return self.AuthSessionEntity(
                id=auth_session.pk,
                email=auth_session.email,
                emailCode=auth_session.email_code,
                exp=auth_session.exp,
                at=auth_session.at,
                attempt=auth_session.attempt
            )
        except AuthSession.DoesNotExist:
            raise AuthSessionDoesNotExist()
        
        except Exception as e:
            raise DatabaseError(e)
    
    def delete(self) -> None:
        obj: AuthSession = self.get_model_instance()
        try:
            obj.delete()
            self.set_model_instance(None)

        except Exception as e:
            raise DatabaseError(e)


class UserRepository(UserRepositoryInterface):
    queryset = User.objects.filter(is_active=True)

    def __init__(self, context: UserRepositoryContext, **kwargs):
        self.UserEntity = context['UserEntity']

    def find_by_email(self, email: str):
        try:
            user: User = self.queryset.get(email=email)
            self.set_model_instance(user)
            return self.UserEntity(
                id=user.pk,
                username=user.username,
                email=user.email,
                isActive=user.is_active,
                isStaff=user.is_staff
            )
        except User.DoesNotExist:
            return None

    def save(self, **kwargs):
        user: User = User.objects.create_user(**kwargs)
        return self.UserEntity(
            id=user.pk,
            username=user.username,
            email=user.email,
            isActive=user.is_active,
            isStaff=user.is_staff
        )
