import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ WARNING: Ye Django ki key hai, ise change mat karna (Google wali niche hai)
SECRET_KEY = "django-insecure-y4z+pv#*#p9rg&(@*qaopp_4$s5^j02&_)pa(p-_ui+5&gl3&v"

DEBUG = True
ALLOWED_HOSTS = ["*", "www.gyansetu.shreejifintech.com"]

CSRF_TRUSTED_ORIGINS = [
    "https://www.gyansetu.shreejifintech.com",
    "https://gyansetu.shreejifintech.com"
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    "users",
    "courses",
    "smart_selects",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "courses.context_processors.extras",
                "courses.context_processors.unread_notifications",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'gyansetu_db',        # Jo aapke local PGAdmin mein dikh raha hai
#         'USER': 'postgres',
#         'PASSWORD': 'Shreeji@123',     # Aapka password
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gyansetu_db',
        'USER': 'gyansetu_user',
        'PASSWORD': 'Shreeji@123',
        'HOST': '72.60.223.238', # Agar database usi server par hai
        'PORT': '5432',
    }
}


# --- Localization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
DATETIME_FORMAT = "d M Y, P"
USE_L10N = False

# --- Static & Media ---
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR / "static")]
STATIC_ROOT = os.path.join(BASE_DIR / "staticfiles")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')

# --- Auth Settings ---
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'login_success'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = '/login/'

# --- Email Config ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'shreejiaffiliate@gmail.com'
EMAIL_HOST_PASSWORD = 'pxbqlsrnwpfjlgwp'
DEFAULT_FROM_EMAIL = 'GyanSetu <shreejiaffiliate@gmail.com>'

# --- Razorpay ---
RAZORPAY_KEY_ID = 'rzp_test_SOCWZ8L1q01O7W'
RAZORPAY_KEY_SECRET = '5TdpyMGMMCIlOPu69YoW61Zs'

# ================================================================
# ✅ ALLAUTH & GOOGLE LOGIN SETTINGS (Bypass Signup Form)
# ================================================================
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True

# 🚀 Ye dono lines signup form ko bypass karti hain
SOCIALACCOUNT_AUTO_SIGNUP = True 
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_ADAPTER = 'courses.adapters.MySocialAccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}

# --- Security ---
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ================================================================
# ✅ DJANGO REST FRAMEWORK AUTHENTICATION SETTINGS
# ================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

CORS_ALLOW_ALL_ORIGINS = True