from urllib.parse import parse_qs


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.build_get_params_dict(environ['QUERY_STRING'])
        self.build_post_params_dict(environ['wsgi.input'].read())
        # self.build_get_params_dict(environ['QUERY_STRING'])
        self.settings = settings
        self.environ = environ
        self.extra = {}

    def __getattr__(self, item):
        return self.extra.get(item, None)

    def build_get_params_dict(self, raw_params: str):
        self.GET = parse_qs(raw_params)
        # print(self.GET)

    def build_post_params_dict(self, raw_bytes: bytes):
        raw_params = raw_bytes.decode('utf-8')
        self.POST = parse_qs(raw_params)
        # print(self.POST)