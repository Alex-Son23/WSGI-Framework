from pprint import pprint
from typing import List, Type

from application.exceptions import NotFound, NotAllow
from application.view import View

from application.request import Request

from application.response import Response

from application.middleware import BaseMiddleware
from urls import Url
import re


class Application:

    __slots__ = ('urls', 'settings', 'middlewares')

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[BaseMiddleware]]):
        self.urls = urls
        self.settings = settings
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        view = self._get_view(environ)
        request = self._get_request(environ)
        # response = self._get_response(environ, view, request)

        self._apply_middleware_to_request(request)
        response = self._get_response(environ, view, request)
        self._apply_middleware_to_response(response)
        # pprint(environ)
        # raw_url = environ['PATH_INFO']
        # view = self._find_view(raw_url)()
        # method = environ['REQUEST_METHOD'].lower()
        # if not hasattr(view, method):
        #     raise NotAllow
        # raw_response = getattr(view, method)(None)
        start_response(str(response.status_code), response.headers.items())
        # '200 OK', [('Content-Type', 'text/html')]
        return iter([response.body])

    def _apply_middleware_to_request(self, request: Request):
        for i in self.middlewares:
            i().to_request(request)

    def _apply_middleware_to_response(self, response: Response):
        for i in self.middlewares:
            i().to_response(response)

    def _prepare_url(self, url:str):
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url:str) -> Type[View]:
        url = self._prepare_url(raw_url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view
        raise NotFound

    def _get_view(self, environ) -> View:
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)()
        return view

    def _get_request(self, environ: dict):
        return Request(environ, self.settings)

    def _get_response(self, environ: dict, view: View, request: Request) -> Response:
        method = environ['REQUEST_METHOD'].lower()
        if not hasattr(view, method):
            raise NotAllow
        return getattr(view, method)(request)
