from flask import request
from flask_restful import Resource
from app.models import UrlIndex

class BaseAPI(Resource):
    def __init__(self):
        self.model = None
        self._set_model()

    def get(self):
        #print(request.args)
        results = []
        perpage = 0
        page = 0

        if "perpage" in request.args:
            perpage = int(request.args["perpage"])

        if "page" in request.args:
            page = int(request.args["page"])

        results = self._search_filter_order(request, perpage, page)
        return self.model.serialize_list(results)

    def _search_filter_order(self, request, perpage, page):
        if perpage > 0:
            return self.model.query.limit(perpage).offset(page*perpage)
        return self.model.query.all()

    def _set_model(self):
        raise NotImplementedError("API base class, derive and implement _set_model.")

class UrlsAPI(BaseAPI):
    def _set_model(self):
        self.model = UrlIndex


