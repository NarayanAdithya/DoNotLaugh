import os


class Config():
    DEBUG = True
    HOST = os.environ.get('HOST', '127.0.0.1')
    APP_SETTINGS = "DevelopmentConfig"
    MONGODB_SETTINGS = {
        'DB': "donotlaugh",
        "host": os.environ.get('MONGO_URI', 'mongodb://localhost:27017/donotlaugh')
    }
    OAUTHLIB_INSECURE_TRANSPORT = 1
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
