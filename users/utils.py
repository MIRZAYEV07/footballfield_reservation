import json
import random
import string
from django.conf import settings as s

from datetime import datetime, timedelta

def user_expire_time():
    time = datetime.now() + timedelta(minutes=1)
    return time.strftime('%H:%M:%S')