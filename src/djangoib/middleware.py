import pytz

from django.http import HttpRequest
from django.utils import timezone
from djangoib.utils import get_timezone_from_ip, get_ip_from_request


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        ip = get_ip_from_request(request)
        tz = get_timezone_from_ip(ip)
        timezone.activate(pytz.timezone(tz))
        return self.get_response(request)
