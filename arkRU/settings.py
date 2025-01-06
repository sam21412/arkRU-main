"""
Django settings for arkRU project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from oscar.defaults import *







# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'





# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b(-l&ymakw49x1v_$0%14!kz(%kaezre*ne7bdf)_0iad2e9)$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
  'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',

    'django.contrib.sites',
    'django.contrib.flatpages',
    'oscar.config.Shop',
    'apps.analytics.apps.AnalyticsConfig',
    'apps.checkout.apps.CheckoutConfig',
    'apps.address.apps.AddressConfig',
    'apps.shipping.apps.ShippingConfig',
    'apps.catalogue.apps.CatalogueConfig',
    'oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig',
    'apps.communication.apps.CommunicationConfig',
    'apps.partner.apps.PartnerConfig',
    'apps.basket.apps.BasketConfig',  # Убедитесь, что используется ваша конфигурация
    'apps.payment.apps.PaymentConfig',
    'apps.offer.apps.OfferConfig',
    'apps.order.apps.OrderConfig',
    'apps.customer.apps.CustomerConfig',
    'oscar.apps.search.apps.SearchConfig',
    'apps.voucher.apps.VoucherConfig',
    'apps.wishlists.apps.WishlistsConfig',
    'apps.dashboard.apps.DashboardConfig',


    'oscar.apps.dashboard.reports.apps.ReportsDashboardConfig',
    'oscar.apps.dashboard.users.apps.UsersDashboardConfig',
    'oscar.apps.dashboard.orders.apps.OrdersDashboardConfig',
    'apps.dashboard.catalogue.apps.CatalogueDashboardConfig',
    'oscar.apps.dashboard.offers.apps.OffersDashboardConfig',
    'oscar.apps.dashboard.partners.apps.PartnersDashboardConfig',
    'oscar.apps.dashboard.pages.apps.PagesDashboardConfig',
    'oscar.apps.dashboard.ranges.apps.RangesDashboardConfig',
    'oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig',
    'oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig',
    'oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig',
    'oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig',
    

    # 3rd-party apps that oscar depends on
    'sslserver',
    'widget_tweaks',
    'haystack',
    'treebeard',
    'sorl.thumbnail',   # Default thumbnail backend, can be replaced
    'django_tables2',
    'your_app',  # Добавьте ваше приложение сюда
]

# Удалите или закомментируйте OSCAR_SHOP_APPS, так как он не нужен:
# OSCAR_SHOP_APPS = [
#     'apps.basket.apps.BasketConfig',
#     # ...другие приложения Oscar...
# ]

MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        'social_django.middleware.SocialAuthExceptionMiddleware',
        

    
]



ROOT_URLCONF = 'arkRU.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'oscar.apps.search.context_processors.search_form',
'oscar.apps.checkout.context_processors.checkout',
'oscar.apps.communication.notifications.context_processors.notifications',
'oscar.core.context_processors.metadata',
    'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

            ],
        },
    },
]

WSGI_APPLICATION = 'arkRU.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }
}

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',

    'social_core.backends.steam.SteamOpenId',  # Используйте SteamOpenId для Steam
    'django.contrib.auth.backends.ModelBackend',

)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIAL_AUTH_STEAM_API_KEY = '7098BB74FD55AB718B95C18D50FABEDF'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'



HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = 'en-us'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
    # добавьте другие языки по необходимости
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


SITE_ID = 1

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'your_app.pipeline.save_steam_id',  # Добавьте эту строку
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

AUTH_USER_MODEL = 'your_app.User'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}