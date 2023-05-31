from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.cache import cache
from typing import Optional

from .models import (
    AuthSession,
    User
)
from domains.interfaces.users_repository import (
    AuthSessionRepository as AuthSessionRepositoryInterface,
    AuthSessionRepositoryContext,
    AuthTokenCachePolicy,
    UserRepository as UserRepositoryInterface,
    UserRepositoryContext,
    AuthTokenRepositoryContext,
    AuthTokenRepository as AuthTokenRepositoryInterface
)
from core.exceptions import DatabaseError
from apps.users.exceptions import (
    AuthSessionDoesNotExist,
    EmailAddrValidationError,
    UserInvalidError
)

EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = settings.EMAIL_USE_TLS


class AuthSessionRepository(AuthSessionRepositoryInterface):
    queryset = AuthSession.objects.all()

    def __init__(self, context: AuthSessionRepositoryContext):
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


class AuthTokenRepository(AuthTokenRepositoryInterface):

    def __init__(self, context: AuthTokenRepositoryContext):
        self.AuthTokenEntity = context['AuthTokenEntity']
        self.UserEntity = context['UserEntity']

    def find_access_token_by_user_id(self, user_id: int, policy: AuthTokenCachePolicy):
        key = 'auth/token'
        obj_key = f'{user_id}'

        payload = cache.get(key)
        if payload:
            token: Optional[str] = payload.get(obj_key)
            if isinstance(token, str):
                return self.AuthTokenEntity(
                    type='access',
                    value=token
                )

        try:
            user: User = User.objects.filter(is_active=True).get(pk=user_id)
            user_entity = self.UserEntity(
                id=user.pk,
                username=user.username,
                email=user.email,
                isActive=user.is_active,
                isStaff=user.is_staff
            )
            token = user_entity.accessToken.value

            auth_token_cache = payload if payload else {}
            auth_token_cache[obj_key] = token

            cache.set(key, auth_token_cache, timeout=policy['max_age'])
            return self.AuthTokenEntity(
                type='access',
                value=token
            )
        except User.DoesNotExist:
            raise UserInvalidError()


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
        user = User.objects.create_user(**kwargs)
        return self.UserEntity(
            id=user.pk,
            username=user.username,
            email=user.email,
            isActive=user.is_active,
            isStaff=user.is_staff
        )
    
    def find_by_id(self, id: int):
        try:
            user: User = self.queryset.get(pk=id)
            self.set_model_instance(user)
            return self.UserEntity(
                id=user.pk,
                username=user.username,
                email=user.email,
                isActive=user.is_active,
                isStaff=user.is_staff
            )
        except User.DoesNotExist:
            raise UserInvalidError()
    
    def delete(self) -> None:
        obj: User = self.get_model_instance()
        try:
            obj.delete()
            self.set_model_instance(None)

        except Exception as e:
            raise DatabaseError(e)
