import json

import firebase_admin
from firebase_admin import credentials

from src.settings import settings

firbase_admin = None


def initialize_firebase():
    global firbase_admin
    if firbase_admin is None:
        admin_sdk = json.loads(settings.FIREBASE_SETTINGS, strict=False)
        cred = credentials.Certificate(admin_sdk)
        firbase_admin = firebase_admin.initialize_app(cred)
