# -*- coding: utf-8 -*-
import os
from lms.envs.devstack import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "My Open edX - http://local.overhang.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="boto.plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="botocore.vendored.requests.packages.urllib3._collections")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs.opener")
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.overhang.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "Gbwxg6Ps9qvyNIqEIfuVNrkj"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "AitYVOnvJM2_Oz0V3pNyA4EmjRUEhpGKG24dqXCxNehmhgTvbZGhLIp4mXSsc0owYRM1FXuF8hzQYKmYR3jlA1kEJET8pNEhIK_ch5JnA2Z5HtAC7Ld7t_FE_pdEVVFdg41h52fczRPXPfDDqDDqiu0-YMkzBVB5SQgm3uI36vDQJB-MltfIgKRFmEMjVuYgZWDAvEqQb5tZjD3u0KpEzTxmnkPY_6VsNwBQ_uwhEWu37rWPN-r9OzH6NgFp3HaZ2HMyiT0R8OYq5_os_YdPKPvST7rKSZtWzkn8odbXeBhRxbJVDvlXLLWRnGAboc18KqZ4potCnP53BZtQrdIaMQ",
        "n": "kFwmXY_OdMW9Grn5PXi5JxPQOyegO82_LgZDNa77AB2SgALNZiEIUbP1wa9OiVRD6eJSPAf_CfIA_YX8NHeGwaosQ7SB65QyNTLgAn6-fI1e6PFU4x9ZfNAGM8vnt6hbC4pdWdYHnACaWVXObRCcRW-NHPXa9jUY9Lgv7N_CQwBExDgSYZkBLJ3cGcoLC0DnZ5MHSbpCxiGr_zVyFv5711IDpQ93WeAq2DXrDWRNfi98BdlaIFl93j0oUATAthaKm2F6MaJvtguCbPNeH-Jrdlq_saycdWchCeOTGb7Yq1iK4Cdo14PG4v8Vwu_EoVSjHvW53E2hqcvyywfYDqsyvQ",
        "p": "tt7BEB36_m0xVwMvKu-FqBeftGWUIs2O-LKah1ZBsZ8mBSYlIwuRN-bwDMaKvzUaxxBS_MqHY-IUCWqF7M0GwIbqQxSvAko5sa5cGEMYaGAb3uzwPebEPxxBnMpulIoNXZSuWQjGfDg-nWMzVQm8BAG5rny4jjy4R4hHca0GyAk",
        "q": "yhbvOGdOSrpez7nrFaWYr1ipxh7yrxF0B8G22JMjmxT70A2LxY5GUgO4gPBMwZFbZ_LBFkpJM_mByROaVGW2w_VC7VlyUb7MteOytIt6rjnn5NPfae9NTCsIcXsp-XTVXvCNcbntTI9wG6z4AQ2feYRwbmhQR70IOjXiKVik-hU",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "kFwmXY_OdMW9Grn5PXi5JxPQOyegO82_LgZDNa77AB2SgALNZiEIUbP1wa9OiVRD6eJSPAf_CfIA_YX8NHeGwaosQ7SB65QyNTLgAn6-fI1e6PFU4x9ZfNAGM8vnt6hbC4pdWdYHnACaWVXObRCcRW-NHPXa9jUY9Lgv7N_CQwBExDgSYZkBLJ3cGcoLC0DnZ5MHSbpCxiGr_zVyFv5711IDpQ93WeAq2DXrDWRNfi98BdlaIFl93j0oUATAthaKm2F6MaJvtguCbPNeH-Jrdlq_saycdWchCeOTGb7Yq1iK4Cdo14PG4v8Vwu_EoVSjHvW53E2hqcvyywfYDqsyvQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.overhang.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "Gbwxg6Ps9qvyNIqEIfuVNrkj"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
CORS_ALLOW_HEADERS = corsheaders_default_headers + ('use-jwt-cookie',)

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.local.overhang.io"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "hidden"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"
BULK_EMAIL_SEND_USING_EDX_ACE = True
FEATURES["ENABLE_FOOTER_MOBILE_APP_LINKS"] = False

# Branding
MOBILE_STORE_ACE_URLS = {}
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}

# Make it possible to hide courses by default from the studio
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False

# Caching
CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_lms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_lms",
}

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# MFE: enable API and set a low cache timeout for the settings. otherwise, weird
# configuration bugs occur. Also, the view is not costly at all, and it's also cached on
# the frontend. (5 minutes, hardcoded)
ENABLE_MFE_CONFIG_API = True
MFE_CONFIG_API_CACHE_TIMEOUT = 1

# MFE-specific settings


FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = True





FEATURES['ENABLE_NEW_BULK_EMAIL_EXPERIENCE'] = True














FEATURES['ALLOW_PUBLIC_ACCOUNT_CREATION'] = False

THIRD_PARTY_AUTH_BACKENDS = ['social_core.backends.google.GoogleOAuth2']

######## End of common LMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

LMS_BASE = "local.overhang.io:8000"
LMS_ROOT_URL = "http://{}".format(LMS_BASE)
LMS_INTERNAL_ROOT_URL = LMS_ROOT_URL
SITE_NAME = LMS_BASE
CMS_BASE = "studio.local.overhang.io:8001"
CMS_ROOT_URL = "http://{}".format(CMS_BASE)
LOGIN_REDIRECT_WHITELIST.append(CMS_BASE)

# Session cookie
SESSION_COOKIE_DOMAIN = "local.overhang.io"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

# CMS authentication
IDA_LOGOUT_URI_LIST.append("http://studio.local.overhang.io:8001/logout/")

FEATURES["ENABLE_COURSEWARE_MICROFRONTEND"] = False

# Disable enterprise integration
FEATURES["ENABLE_ENTERPRISE_INTEGRATION"] = False
SYSTEM_WIDE_ROLE_CLASSES.remove("enterprise.SystemWideEnterpriseUserRoleAssignment")

LOGGING["loggers"]["oauth2_provider"] = {
    "handlers": ["console"],
    "level": "DEBUG"
}


# Dynamic config API settings
# https://openedx.github.io/frontend-platform/module-Config.html
MFE_CONFIG = {
    "BASE_URL": "apps.local.overhang.io",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "CREDENTIALS_BASE_URL": "",
    "DISCOVERY_API_BASE_URL": "",
    "FAVICON_URL": "http://local.overhang.io/favicon.ico",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "http://local.overhang.io:8000",
    "LOGIN_URL": "http://local.overhang.io:8000/login",
    "LOGO_URL": "http://local.overhang.io:8000/theming/asset/images/logo.png",
    "LOGO_WHITE_URL": "http://local.overhang.io:8000/theming/asset/images/logo.png",
    "LOGO_TRADEMARK_URL": "http://local.overhang.io:8000/theming/asset/images/logo.png",
    "LOGOUT_URL": "http://local.overhang.io:8000/logout",
    "MARKETING_SITE_BASE_URL": "http://local.overhang.io:8000",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "http://local.overhang.io:8000/login_refresh",
    "SITE_NAME": "My Open edX",
    "STUDIO_BASE_URL": "http://studio.local.overhang.io:8001",
    "USER_INFO_COOKIE_NAME": "user-info",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
}

# MFE-specific settings


AUTHN_MICROFRONTEND_URL = "http://apps.local.overhang.io:1999/authn"
AUTHN_MICROFRONTEND_DOMAIN  = "apps.local.overhang.io/authn"
MFE_CONFIG["DISABLE_ENTERPRISE_LOGIN"] = True



ACCOUNT_MICROFRONTEND_URL = "http://apps.local.overhang.io:1997/account"
MFE_CONFIG["ACCOUNT_SETTINGS_URL"] = ACCOUNT_MICROFRONTEND_URL



COMMUNICATIONS_MICROFRONTEND_URL = "http://apps.local.overhang.io:1984/communications"
MFE_CONFIG["SCHEDULE_EMAIL_SECTION"] = True



MFE_CONFIG["ENABLE_NEW_EDITOR_PAGES"] = True
MFE_CONFIG["ENABLE_PROGRESS_GRAPH_SETTINGS"] = True



DISCUSSIONS_MICROFRONTEND_URL = "http://apps.local.overhang.io:2002/discussions"
DISCUSSIONS_MFE_FEEDBACK_URL = None



WRITABLE_GRADEBOOK_URL = "http://apps.local.overhang.io:1994/gradebook"



LEARNING_MICROFRONTEND_URL = "http://apps.local.overhang.io:2000/learning"
MFE_CONFIG["LEARNING_BASE_URL"] = "http://apps.local.overhang.io:2000"



ORA_GRADING_MICROFRONTEND_URL = "http://apps.local.overhang.io:1993/ora-grading"



PROFILE_MICROFRONTEND_URL = "http://apps.local.overhang.io:1995/profile/u/"
MFE_CONFIG["ACCOUNT_PROFILE_URL"] = "http://apps.local.overhang.io:1995"



# Cors configuration

# authn MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1999")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1999")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1999")

# account MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1997")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1997")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1997")

# communications MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1984")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1984")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1984")

# course-authoring MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:2001")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:2001")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:2001")

# discussions MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:2002")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:2002")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:2002")

# gradebook MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1994")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1994")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1994")

# learning MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:2000")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:2000")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:2000")

# ora-grading MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1993")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1993")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1993")

# profile MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1995")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1995")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1995")



