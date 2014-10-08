import datetime
import random
import os
import requests

from BeautifulSoup import BeautifulSoup
from cliqz.util import generate_uuid
from cliqz.app import db
from cliqz.model import UnsplashImage
from cfg import EXPIRE_UNSPLASH_DAYS, UNSPLASH_IMAGE_DIR
from sqlalchemy import asc, desc


def update():
    n = 1
    total_images = 0
    while total_images <= 20 and n < 10:
        url = "https://unsplash.com/?page=%d" % (n)
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text)
            all_photos = soup.findAll("div", {"class": "photo"})
            for p in all_photos:
                image_url = p.a.img["src"]

                if get(image_url) is not None:
                    total_images += 1
                    continue

                print "Downloading %d: %s" % (total_images + 1, image_url)
                file_name = download_url(image_url)
                unsplash_img = UnsplashImage()
                unsplash_img.id = image_url
                unsplash_img.utc_date_created = datetime.datetime.utcnow()
                unsplash_img.filename = file_name
                save(unsplash_img)
                total_images += 1

        n += 1


def save(o):
    db.add(o)
    db.commit()


def delete(o):
    db.delete(o)
    db.commit()


def _does_file_exists(file_path):
    return os.path.exists(file_path);


def random_image():
    unsplash_img_lis = (db.
                        query(UnsplashImage)
    ).all()
    return random.choice(unsplash_img_lis)


def fetch():
    #get unexpired image
    unsplash_img = (db.
                    query(UnsplashImage).
                    filter(UnsplashImage.utc_expiry != None).
                    filter(UnsplashImage.utc_expiry > datetime.datetime.utcnow())
    ).first()
    if unsplash_img is not None:
        return unsplash_img

    #get unused image
    unused_img = (db.
                  query(UnsplashImage).
                  filter(UnsplashImage.utc_expiry == None).
                  order_by(asc(UnsplashImage.utc_date_created))
    ).first()
    if unused_img is not None:
        unused_img.utc_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=EXPIRE_UNSPLASH_DAYS)
        save(unused_img)
        return unused_img

    #get latest expired image
    latest_img = (db.
                  query(UnsplashImage).
                  order_by(desc(UnsplashImage.utc_expiry))
    ).first()
    return latest_img


def download_url(url):
    file_name = "%s.jpg" % (generate_uuid())
    file_path = os.path.join(UNSPLASH_IMAGE_DIR, file_name)
    r = requests.get(url, allow_redirects=True)
    with open(file_path, 'wb') as f:
        f.write(r.content)
    return file_name


def get(id):
    return (db.
            query(UnsplashImage).
            filter(UnsplashImage.id == unicode(id))
    ).first() if id is not None else None