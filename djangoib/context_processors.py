from datetime import datetime

from django.conf import settings


APP_NAME = getattr(settings, 'APP_NAME')
CURRENT_YEAR = datetime.now().year
GA_TRACKING_ID = getattr(settings, 'GA_TRACKING_ID')
COPYRIGHT_TEMPLATE = getattr(settings, 'COPYRIGHT_TEMPLATE')
COPYRIGHT_TEXT = COPYRIGHT_TEMPLATE.format(APP_NAME=APP_NAME, CURRENT_YEAR=CURRENT_YEAR)


def defauls(_):
    ctx = {
        'app_name': APP_NAME,
        'copyright_text': COPYRIGHT_TEXT,
        'ga_tracking_id': GA_TRACKING_ID,
    }
    return ctx
