import random
import string

from functools import lru_cache
from typing import List

import micawber
import requests

from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpRequest

DEFAULT_TIMEZONE = getattr(settings, 'TIME_ZONE', 'UTC')
IMGUR_CLIENT_ID = getattr(settings, 'IMGUR_CLIENT_ID', '')
PROVIDERS = micawber.bootstrap_basic()
RHEADERS = {'Authorization': 'Client-ID {}'.format(IMGUR_CLIENT_ID)}


def get_imgur_credit_status():
    r = requests.get('https://api.imgur.com/3/credits', headers=RHEADERS)
    print(r.json(), r.headers)


def upload_image(image_file):
    get_imgur_credit_status()
    files = {'image': image_file}
    payload = {'type': 'file'}
    r = requests.post('https://api.imgur.com/3/upload', data=payload, files=files, headers=RHEADERS)
    return r.json() if r.ok else None


def get_ip_from_request(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[-1].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    return ip_address


@lru_cache(maxsize=64)
def get_timezone_from_ip(ip_address: str, depth: int = 1):
    r = requests.get('http://ip-api.com/json/{}'.format(ip_address))
    max_depth = depth == 2
    if r.ok:
        r = r.json()
        succeeded = r.get('status') == 'success'
        if succeeded:
            return r.get('timezone', DEFAULT_TIMEZONE) or DEFAULT_TIMEZONE
        else:
            if max_depth:
                return DEFAULT_TIMEZONE
            else:
                return get_timezone_from_ip('', depth + 1)
    else:
        return DEFAULT_TIMEZONE


def get_random_string(char_count=32):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=char_count))


def parse_post_body(s: str, quotables: List[int], op: int) -> (str, List[int]):
    o = BeautifulSoup(s, 'lxml').text
    o = PROVIDERS.parse_text_full(o)
    lines = o.splitlines()
    quotable_lines = ['>>{}'.format(quotable) for quotable in quotables]
    quoted_post_ids = []
    for i in range(len(lines)):
        line = lines[i]
        try:
            qi = quotable_lines.index(line)
            current_quotable_post_id = quotables[qi]
            suffix = ''
            if current_quotable_post_id == op:
                suffix = '(OP)'
            line = '<a class="quoted-post-from-link" href="#p{}">&gt;&gt;{}{}</a>'.format(
                current_quotable_post_id, current_quotable_post_id, suffix)
            lines[i] = line
            quoted_post_ids.append(quotables[qi])
        except ValueError:
            pass
    o = '\n'.join(lines)
    return o, quoted_post_ids
