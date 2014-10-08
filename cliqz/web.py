from cliqz.action import unsplash
from cliqz.app import app, db
from flask import jsonify


def test():
    return jsonify({"status": "ok"})


def httpget_unsplash_img():
    background_image = unsplash.fetch()
    _unsplash_img_obj_to_url(background_image)
    return jsonify({
        "status": "ok",
        "url": _unsplash_img_obj_to_url(background_image),
    })


def _unsplash_img_obj_to_url(unsplash_img_obj):
    return "/media/unsplash_images/%s" % (unsplash_img_obj.filename)


app.add_url_rule('/unsplash/url/',
                 "httpget_unsplash_img", httpget_unsplash_img, methods=['GET'])

app.add_url_rule('/test/',
                 "test", test, methods=['GET'])

#teardown

@app.teardown_request
def shutdown_session(exception=None):
    if not app.config['TESTING']:
        try:
            db.remove()
        except:
            pass


@app.teardown_appcontext
def shutdown_appcontext(exception=None):
    if not app.config['TESTING']:
        try:
            db.remove
        except:
            pass