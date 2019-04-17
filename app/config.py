import os

class Development(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///scraper.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///scraper.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app_config = {
    'development': Development,
    'production': Production,
}

site_rules = {
    # works even on sitemap
    "theguardian.com": {
        "title":"content__headline",
        "content":["content__standfirst","content__article-body",],

# TODO ## tagS - make plural
        "content_tag":"p",
#
        "image_wrap":"picture",
        "image_tag":"img",
        "must_have_alt":True,
        "update_existing":False,
        "ignore_list":["/live/","/gallery/","/video/",
                       "/picture/","/audio/","/lifeandstyle/",
                       "/football/","/artanddesign/","/info/"],
        "category_uri":"/0/",  # position in uri scheme
        "category_param":None, # a GET param dictates category
    },

    # new, only tested on example url, no images
    "crainscleveland.com": {
        "title":"article-title",
        "content":["field--name-field-paragraph-body",],
        "content_tag":"p",
        "image_wrap":None,
        "image_tag":None,
        "must_have_alt":False,
        "update_existing":False,
        "ignore_list":[],
        "category_uri":None,
        "category_param":None,
    },

    # A worst case, not configured, all we can really do is grab
    # meta title and body content...
    # TODO
}
