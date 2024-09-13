import os

from .base import *

SECRET_KEY = os.urandom(32).hex()
