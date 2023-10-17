from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=40, default='', unique=True, error_messages={
            "unique": "Пользователь с таким номером телефона уже есть.",
        }, verbose_name='Телефон')

    # creator = models.ForeignKey(
    #     'api.baseuser', on_delete=models.SET_NULL, null=True, verbose_name='Создатель',
    #     help_text='Поле нужно для управления тем, каких пользователей видят продавцы')

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    createdAt = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    class Meta(AbstractBaseUser.Meta):
        verbose_name = 'Базовый пользователь'
        verbose_name_plural = 'Базовые пользователи'

    def __str__(self):
        return self.username
