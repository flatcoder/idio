from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

db = SQLAlchemy()

class ModelABC(object):
    # 1st int PK that's not a FK is autoincrement.
    id = db.Column(db.Integer, primary_key=True)

    date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def serialize(self):
        """ Basic, but enough for now """
        return {c: str(getattr(self, c)) for c in inspect(self).attrs.keys()}

    @classmethod
    def get(cls):
        """ Class method means read-only no instance, perfect... """
        try:
            return cls.query.all()
        except:
            raise NotImplementedError("Model base class, derive and implement 'get'.")

    @staticmethod
    def serialize_list(l):
        """ Static method, read-only, no instance, no class... """
        return [m.serialize() for m in l]

class UrlIndex(ModelABC, db.Model):
    __tablename__ = 'urls'

    url = db.Column(db.String(512), unique=True, nullable=False)
    canonical_rel = db.Column(db.String(512), nullable=True)
    title = db.Column(db.String(512), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    images_json = db.Column(db.Text(), nullable=True)
    category = db.Column(db.String(32), nullable=True)
    # site_rule = db.Column(db.String(32), nullable=True)

    @classmethod
    def find(cls, url):
        recs = cls.query.filter_by(url=url)
        if recs != None:
            return recs.first()
        return None

    @classmethod
    def create(cls, url, title, content, canonical_rel="",images="", category=""):

        if canonical_rel == "":
            canonical_rel = url

        newreg = UrlIndex(url=url,canonical_rel=canonical_rel,title=title,
                    content=content,images_json=images,category=category)
        try:
            db.session.add(newreg)
            db.session.commit()
            return newreg
        except:
            raise Exception("Failed creating URL INDEX for "+url+".")

    @classmethod
    def update(cls, url, title, content, canonical_rel="",images="", category=""):
        if canonical_rel == "":
            canonical_rel = url

        try:
            newreg = UrlIndex.query.filter_by(url=url).first()
            newreg.title = title
            newreg.content = content
            newreg.images = images
            newreg.canonical_rel = canonical_rel
            db.session.add(newreg)
            db.session.commit()
            return newreg
        except:
            raise Exception("Failed creating URL INDEX for "+url+".")
