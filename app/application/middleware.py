from application.request import Request
from application.response import Response
from uuid import uuid4
from urllib.parse import parse_qs
from http.cookies import SimpleCookie

class BaseMiddleware:

    def to_request(self, request: Request):
        return

    def to_response(self, response: Response):
        return


class Session(BaseMiddleware):

    def to_request(self, request: Request):
        raw_cookie = request.environ.get('HTTP_COOKIE', None)
        # print(raw_cookie)
        if raw_cookie:
            cookie = SimpleCookie()
            cookie.load(raw_cookie)
            cookie_dict = {key: value.value for key, value in cookie.items()}
        else:
            cookie_dict = {'sessionid': []}
            cookie = None
        # print(cookie_dict)
        if not cookie:
            return
        print(cookie_dict)
        session_id = cookie_dict['sessionid'][0]
        # session_id = parse_qs(cookie)['sessionid'][0]
        request.extra['session_id'] = session_id

    def to_response(self, response: Response):

        if not response.request.session_id:
            response.update_headers(
                {"Set-Cookie": f"session_id={uuid4()}"}
            )

middlewares = [
    Session
]