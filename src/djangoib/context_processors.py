from datetime import datetime

from django.conf import settings


APP_NAME = getattr(settings, 'APP_NAME')
CURRENT_YEAR = datetime.now().year
COPYRIGHT_TEMPLATE = getattr(settings, 'COPYRIGHT_TEMPLATE')
COPYRIGHT_TEXT = COPYRIGHT_TEMPLATE.format(APP_NAME=APP_NAME, CURRENT_YEAR=CURRENT_YEAR)
IS_PROD = getattr(settings, 'IS_PROD')


def defaults(_):
    ctx = {
        'app_name': APP_NAME,
        'copyright_text': COPYRIGHT_TEXT,
        'is_production': IS_PROD,
    }
    return ctx
