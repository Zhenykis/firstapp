from os import getenv

# ======= APP ==========
APP_HOST = getenv("APP_HOST", default="127.0.0.1")
APP_PORT = getenv("APP_PORT", default=8000)

# ======= BD ==========
BD_HOST = getenv("BD_HOST", default="127.0.0.1")
BD_PORT = getenv("BD_PORT", default=5432)
BD_USER = getenv("BD_USER", default="postgres")
BD_PASSWORD = getenv("BD_PASSWORD", default="postgres")
BD_NAME = getenv("BD_NAME", default="mydatabase")


# ======= AUTH
COOKIES_KEY = getenv("COOKIES_KEY", default="user_cookie")
