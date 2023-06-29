"""
Django settings for experimenter.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import json
import os
from importlib import resources
from urllib.parse import urljoin

import sentry_sdk
from decouple import config
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from django.db.models import DecimalField, ForeignKey, JSONField, ManyToManyField
from sentry_sdk.integrations.django import DjangoIntegration

for cls in [
    DecimalField,
    ForeignKey,
    JSONField,
    ManyToManyField,
    ModelAdmin,
    StackedInline,
    TabularInline,
]:
    cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


APP_VERSION_JSON_PATH = os.path.join(BASE_DIR, "version.json")
APP_VERSION = config("APP_VERSION", default=None)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

DEV_USER_EMAIL = "dev@example.com"

NORMANDY_DEFAULT_CHANGELOG_USER = "unknown-user@normandy.mozilla.com"

KINTO_DEFAULT_CHANGELOG_USER = "experimenter@experimenter.services.mozilla.com"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

HOSTNAME = config("HOSTNAME")

IS_STAGING = "stage." in HOSTNAME

ALLOWED_HOSTS = [HOSTNAME]

if DEBUG:
    ALLOWED_HOSTS += ["localhost", "nginx"]  # pragma: no cover

USE_YARN_DEV = config("USE_YARN_DEV", default=DEBUG, cast=bool)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.forms",
    "import_export",
    # Graphene
    "graphene_django",
    # Libraries
    "corsheaders",
    "django_markdown2",
    "rangefilter",
    "rest_framework",
    "widget_tweaks",
    # Experimenter
    "experimenter.base",
    "experimenter.changelog",
    "experimenter.experiments",
    "experimenter.features",
    "experimenter.jetstream",
    "experimenter.kinto",
    "experimenter.legacy.legacy_experiments",
    "experimenter.legacy.normandy",
    "experimenter.legacy.notifications",
    "experimenter.openidc",
    "experimenter.outcomes",
    "experimenter.projects",
    "experimenter.reporting",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dockerflow.django.middleware.DockerflowMiddleware",
    "experimenter.openidc.middleware.OpenIDCAuthMiddleware",
]

ROOT_URLCONF = "experimenter.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "legacy", "legacy-ui", "templates"),
            os.path.join(BASE_DIR, "nimbus-ui", "templates"),
            os.path.join(BASE_DIR, "docs"),
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "experimenter.base.context_processors.google_analytics",
                "experimenter.base.context_processors.features",
                "experimenter.base.context_processors.debug",
            ],
            "debug": DEBUG,
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "experimenter.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": "5432",
    }
}

# Graphene Schema
GRAPHENE = {"SCHEMA": "experimenter.experiments.api.v5.schema"}

if DEBUG:  # pragma: no cover
    GRAPHENE["MIDDLEWARE"] = [
        "experimenter.base.graphene.GrapheneExceptionMiddleware",
    ]


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

OPENIDC_EMAIL_HEADER = config("OPENIDC_HEADER")
OPENIDC_AUTH_WHITELIST = (
    "experiments-api-list",
    "experiments-api-recipe",
    "experiments-api-detail",
    "nimbus-experiment-rest-list",
    "nimbus-experiment-rest-detail",
    "nimbus-experiment-rest-first-run-list",
    "nimbus-experiment-draft-rest-list",
    "nimbus-experiment-draft-rest-detail",
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(os.path.join(BASE_DIR, "served"), "static")

STATICFILES_DIRS = [
    ("assets", os.path.join(BASE_DIR, "legacy", "legacy-ui", "assets")),
    ("scripts", os.path.join(BASE_DIR, "legacy", "legacy-ui", "scripts")),
    ("imgs", os.path.join(BASE_DIR, "legacy", "legacy-ui", "imgs")),
    ("nimbus", os.path.join(BASE_DIR, "nimbus-ui", "build")),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


LOGGING_CONSOLE_LEVEL = config("LOGGING_CONSOLE_LEVEL", default="DEBUG")

# Logging

LOGGING_USE_JSON = config("LOGGING_USE_JSON", cast=bool, default=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "mozlog": {
            "()": "dockerflow.logging.JsonLogFormatter",
            "logger_name": "experimenter",
        },
        "verbose": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": LOGGING_CONSOLE_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "mozlog" if LOGGING_USE_JSON else "verbose",
        }
    },
    "loggers": {
        "django.db": {
            "handlers": ["console"] if DEBUG else [],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
}


# Sentry configuration
SENTRY_DSN = config("SENTRY_DSN", default=None)
SENTRY_DSN_NIMBUS_UI = SENTRY_DSN
if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=False,
    )


# Django Rest Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "experimenter.openidc.middleware.OpenIDCRestFrameworkAuthenticator",
    ),
}

# CORS Security Header Config
CORS_ORIGIN_ALLOW_ALL = True

# Experiments list pagination
EXPERIMENTS_PAGINATE_BY = config("EXPERIMENTS_PAGINATE_BY", default=10, cast=int)

USE_GOOGLE_ANALYTICS = config("USE_GOOGLE_ANALYTICS", default=True, cast=bool)

# Automated email destinations

# Email configuration
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_SENDER = config("EMAIL_SENDER")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = not DEBUG
EMAIL_USE_SSL = False

# Email to send to when an experiment is ready for review
EMAIL_REVIEW = config("EMAIL_REVIEW")

# Email to send to when an experiment is ready to ship
EMAIL_SHIP = config("EMAIL_SHIP")

# Email to send to when an experiment is being signed-off
EMAIL_RELEASE_DRIVERS = config("EMAIL_RELEASE_DRIVERS")

# Bugzilla API Integration
BUGZILLA_HOST = config("BUGZILLA_HOST")
BUGZILLA_API_KEY = config("BUGZILLA_API_KEY")
BUGZILLA_CC_LIST = config("BUGZILLA_CC_LIST", default="")
BUGZILLA_CREATE_PATH = "/rest/bug"
BUGZILLA_CREATE_URL = "{path}?api_key={api_key}".format(
    path=urljoin(BUGZILLA_HOST, BUGZILLA_CREATE_PATH), api_key=BUGZILLA_API_KEY
)
BUGZILLA_DETAIL_URL = urljoin(BUGZILLA_HOST, "/show_bug.cgi?id={id}")
BUGZILLA_UPDATE_URL = "{path}?api_key={api_key}".format(
    path=urljoin(BUGZILLA_HOST, "/rest/bug/{id}"), api_key=BUGZILLA_API_KEY
)

BUGZILLA_USER_URL = "{path}?api_key={api_key}".format(
    path=urljoin(BUGZILLA_HOST, "/rest/user/{email}"), api_key=BUGZILLA_API_KEY
)

BUGZILLA_BUG_URL = "{path}?api_key={api_key}".format(
    path=urljoin(BUGZILLA_HOST, "/rest/bug?id={bug_id}"), api_key=BUGZILLA_API_KEY
)
BUGZILLA_COMMENT_URL = "{path}?api_key={api_key}".format(
    path=urljoin(BUGZILLA_HOST, "/rest/bug/{id}/comment"), api_key=BUGZILLA_API_KEY
)

# DS Issue URL
DS_ISSUE_HOST = "https://mozilla-hub.atlassian.net/browse/"

REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_DB = config("REDIS_DB")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "TIMEOUT": None,
    },
}
SIZING_DATA_KEY = "population_sizing"

# Celery
CELERY_BROKER_URL = "redis://{host}:{port}/{db}".format(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB
)
CELERY_BEAT_SCHEDULE = {
    "experiment_status_ready_to_ship_task": {
        "task": "experimenter.legacy.normandy.tasks.update_recipe_ids_to_experiments",
        "schedule": config("CELERY_SCHEDULE_INTERVAL", default=300, cast=int),
    },
    "experiment_status_launched_task": {
        "task": "experimenter.legacy.normandy.tasks.update_launched_experiments",
        "schedule": config("CELERY_SCHEDULE_INTERVAL", default=300, cast=int),
    },
    "nimbus_check_kinto_push_queue_task": {
        "task": "experimenter.kinto.tasks.nimbus_check_kinto_push_queue",
        "schedule": config("CELERY_SCHEDULE_INTERVAL", default=300, cast=int),
    },
    "nimbus_synchronize_preview_experiments_in_kinto": {
        "task": (
            "experimenter.kinto.tasks.nimbus_synchronize_preview_experiments_in_kinto"
        ),
        "schedule": config("CELERY_SCHEDULE_INTERVAL", default=300, cast=int),
    },
    "nimbus_send_emails": {
        "task": "experimenter.kinto.tasks.nimbus_send_emails",
        "schedule": config("CELERY_SCHEDULE_INTERVAL", default=300, cast=int),
    },
    "fetch_jetstream_data": {
        "task": "experimenter.jetstream.tasks.fetch_jetstream_data",
        "schedule": 28800,
    },
    "fetch_population_sizing_data": {
        "task": "experimenter.jetstream.tasks.fetch_population_sizing_data",
        "schedule": 86400,
    },
}

# Recipe Configuration
RECIPE_SLUG_MAX_LEN = 80

# Monitoring
MONITORING_URL = (
    # from_date and to_date format is YYYY-mm-dd
    "https://mozilla.cloud.looker.com/dashboards-next/216?"
    "Experiment={slug}&Time+Range={from_date}+to+{to_date}"
)
ROLLOUT_MONITORING_URL = (
    "https://mozilla.cloud.looker.com/dashboards/operational_monitoring::{slug}"
)

# Statsd via Markus
STATSD_BACKEND = config(
    "STATSD_BACKEND", default="markus.backends.datadog.DatadogMetrics"
)
STATSD_HOST = config("STATSD_HOST")
STATSD_PORT = config("STATSD_PORT")
STATSD_PREFIX = config("STATSD_PREFIX")

MARKUS_BACKEND = [
    {
        "class": STATSD_BACKEND,
        "options": {
            "statsd_host": STATSD_HOST,
            "statsd_port": STATSD_PORT,
            "statsd_namespace": STATSD_PREFIX,
        },
    }
]

# Normandy URLs
NORMANDY_API_HOST = config("NORMANDY_API_HOST")
NORMANDY_API_RECIPE_URL = urljoin(NORMANDY_API_HOST, "/api/v3/recipe/{id}/")
NORMANDY_API_RECIPES_LIST_URL = urljoin(NORMANDY_API_HOST, "/api/v3/recipe/")
NORMANDY_API_HISTORY_URL = urljoin(NORMANDY_API_HOST, "/api/v3/recipe/{id}/history")

NORMANDY_DEVTOOLS_HOST = config("NORMANDY_DEVTOOLS_HOST")
NORMANDY_DEVTOOLS_RECIPE_URL = "{root}{recipe_url}".format(
    root=NORMANDY_DEVTOOLS_HOST, recipe_url="/recipes/{id}"
)
NORMANDY_DEVTOOLS_RECIPE_IMPORT_URL = "{root}{import_url}".format(
    root=NORMANDY_DEVTOOLS_HOST, import_url="/recipes/import/{slug}"
)


# Jira URL
JIRA_URL = config(
    "JIRA_URL",
    default="https://moz-pi-test.atlassian.net/servicedesk/customer/portal/9",
)


SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
SECURE_REFERRER_POLICY = config("SECURE_REFERRER_POLICY", default="origin")

# Silenced ssl_redirect, sts, django primary key checks
SILENCED_SYSTEM_CHECKS = ["security.W008", "security.W004", "models.W042"]

# Feature Flags
FEATURE_MESSAGE_TYPE = config("FEATURE_MESSAGE_TYPE", default=False, cast=bool)
FEATURE_ANALYSIS = config("FEATURE_ANALYSIS", default=False, cast=bool)

# Kinto settings
KINTO_HOST = config("KINTO_HOST")
KINTO_USER = config("KINTO_USER")
KINTO_PASS = config("KINTO_PASS")
KINTO_BUCKET_WORKSPACE = "main-workspace"
KINTO_BUCKET_MAIN = "main"
KINTO_COLLECTION_NIMBUS_DESKTOP = "nimbus-desktop-experiments"
KINTO_COLLECTION_NIMBUS_MOBILE = "nimbus-mobile-experiments"
KINTO_COLLECTION_NIMBUS_PREVIEW = "nimbus-preview"
KINTO_ADMIN_URL = config("KINTO_ADMIN_URL", default=urljoin(KINTO_HOST, "/admin/"))
KINTO_REVIEW_TIMEOUT = config("KINTO_REVIEW_TIMEOUT", cast=int)

# Jetstream GCS Bucket data
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_PROJECT_ID = "experiments-analysis"
GS_BUCKET_NAME = "mozanalysis"

# GCS bucket for user uploads, e.g. branch screenshots
UPLOADS_GS_BUCKET_NAME = config("UPLOADS_GS_BUCKET_NAME", default=None)

# Custom file storage override for user uploads (e.g. for testing)
UPLOADS_FILE_STORAGE = config("UPLOADS_FILE_STORAGE", default=None)

NIMBUS_SCHEMA_VERSION = (
    # TODO: #8492
    "1.12.0"  # pkg_resources.get_distribution("mozilla-nimbus-shared").version
)


# Jetstream config paths
JETSTREAM_CONFIG_OUTCOMES_PATH = os.path.join(
    BASE_DIR, "outcomes", "metric-hub-main", "jetstream", "outcomes"
)

# Feature Manifest path
FEATURE_MANIFESTS_PATH = os.path.join(BASE_DIR, "features", "manifests")
FEATURE_SCHEMAS_PATH = os.path.join(FEATURE_MANIFESTS_PATH, "schemas")

SKIP_REVIEW_ACCESS_CONTROL_FOR_DEV_USER = config(
    "SKIP_REVIEW_ACCESS_CONTROL_FOR_DEV_USER", default=False, cast=bool
)

# Required to save large experiments in the admin
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20mb
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000


EXPERIMENT_SCHEMA_PATH = (
    resources.files("mozilla_nimbus_shared")
    / "schemas"
    / "experiments"
    / "NimbusExperiment.json"
)

EXPERIMENT_SCHEMA = json.loads(EXPERIMENT_SCHEMA_PATH.read_text())
