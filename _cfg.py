import os


SQL_URI_WEBAPP = "postgresql://user:pass@localhost/cliqz"
CWD = os.path.dirname(os.path.realpath(__file__))
UNSPLASH_IMAGE_DIR = os.path.join(CWD, "resources/unsplash_images")
EXPIRE_UNSPLASH_DAYS = 1
MEDIA_PATH = os.path.join(CWD, "cliqz/media").idea
