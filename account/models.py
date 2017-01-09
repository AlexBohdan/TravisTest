from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import get_hasher
from django.core.exceptions import FieldDoesNotExist
from django.db import models, IntegrityError
from django.shortcuts import redirect
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social.exceptions import AuthCanceled, AuthTokenError, AuthMissingParameter
from django.contrib import auth


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if type(exception) == AuthCanceled:
            messages.error(request, 'Вы отменили аутентификацию.')
            return redirect('/')
        elif type(exception) == AuthTokenError:
            messages.error(request,
                           'Вы не дали доступ к email. Чтобы открыть доступ к вашему email зайдите в раздел "Настройки"->"Приложения" вашей соцсети и  удалите доступ приложения "IKnow". Повторно войдите через соцсеть на нашем сайте открыв доступ для email.')
            return redirect('/')
        elif type(exception) == AuthMissingParameter:
            messages.error(request, 'Пользователь с таким email уже зарегестрирован.')
            return redirect('/')
        else:
            raise exception


def save_profile(backend, strategy, uid, response={} or object(), details={}, *args, **kwargs):
    print('response: ' + str(response))
    print('details: ' + str(details))
    print('args: ' + str(args))
    print('kwargs: ' + str(kwargs))
    user = Account.objects.filter(auth_via=backend.name, social_id=uid).first()
    if user:
        login_user = auth.authenticate(username=details['email'], password='55')
        social = UserSocialAuth(login_user, uid, backend.name)
        strategy.session_set('email', details['email'])
    else:
        if details['email'] == '':
            raise AuthTokenError('error')

        avatar = '/media/default_avatar.png'

        if response['photo']:
            avatar = response['photo']

        # reg user
        hasher = get_hasher('default')

        if 'bdate' in response and len(response['bdate'].split('.')) != 3:
            date = response['bdate'].split('.')
            date = date[-1] + '.' + date[1] + '.' + date[0]
            try:
                Account.objects.create(password=hasher.encode('55', hasher.salt()), email=details['email'],
                                       first_name=details['first_name'],
                                       last_name=details['last_name'],
                                       auth_via=backend.name, access_token=response['access_token'],
                                       social_id=uid, avatar=avatar, sex=response['sex'], birthday=date)
            except IntegrityError:
                raise AuthMissingParameter
        else:
            try:
                Account.objects.create(password=hasher.encode('55', hasher.salt()), email=details['email'],
                                       first_name=details['first_name'],
                                       last_name=details['last_name'],
                                       auth_via=backend.name, access_token=response['access_token'],
                                       social_id=uid, avatar=avatar, sex=response['sex'])
            except IntegrityError:
                raise AuthMissingParameter

        # login user
        login_user = auth.authenticate(username=details['email'], password='55')
        social = UserSocialAuth(login_user, uid, backend.name)
        strategy.session_set('email', details['email'])

    return {'user': login_user,
            'social': social}


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(
            email=self.normalize_email(email),
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password):
        account = self.create_user(email, password)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    class Meta:
        verbose_name_plural = 'Пользователи'

    SEX = (('0', 'пол не указан'),
           ('1', 'женский'),
           ('2', 'мужской'),
           )

    email = models.EmailField('E-mail', unique=True)
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=100)

    city = models.CharField('Город', max_length=100, default='', blank=True)

    # for socials
    auth_via = models.CharField('Зарегистрировался через', max_length=20, default='native')
    social_id = models.CharField('Id из соцсети', max_length=100, default='')

    # дополнительные поля
    birthday = models.DateField('Дата рождения', null=True, blank=True)
    about_me = models.TextField('О себе', blank=True)

    # images
    avatar = models.ImageField(upload_to='avatars/', default='/media/default_avatar.png')

    # информационные поля
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последних изменений', auto_now=True)

    is_admin = models.BooleanField('Админ или нет', default=False, blank=True)

    sex = models.IntegerField('Пол', choices=SEX, default=0)

    access_token = models.CharField('Ключ доступа ВК', max_length=200)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
