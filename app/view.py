from datetime import datetime

from application.request import Request
from application.view import View
from application.response import Response
from application.template_engine import build_template
from application.templator import render


class Homepage(View):

    def get(self, request, *args, **kwargs):
        # body = build_template(request, {'time': str(datetime.now()), 'lst': [1, 2, 3]}, 'home.html')
        body = render(template_name='home.html')
        return Response(body=body, request=request)

    def post(self, request: Request, *args, **kwargs) -> Response:
        from pprint import pprint
        # pprint(request.environ)
        # print(f'Post запрос:{request.POST}')
        body = render(template_name='home.html')
        return Response(body=body, request=request)


class EpicMath(View):

    def get(self, request: Request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return Response(body=f'first пустое либо не является числом',request=request)

        second = request.GET.get('second')
        print(second)
        if not second or not second[0].isnumeric():
            return Response(body=f'second пустое либо не является числом')

        return Response(body=f'Сумма {first[0]} и {second[0]} равна {int(first[0])+int(second[0])}', request=request)

class Hello(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'name': 'Anonymous'}, 'hello.html')
        kwargs = {'name': 'Anonymous'}
        body = render(template_name='hello.html', **kwargs)
        return Response(body=body, request=request)

    def post(self, request: Request, *args, **kwargs) -> Response:
        raw_name = request.POST.get('name')
        name = raw_name[0] if raw_name else 'Anonymous'
        # body = build_template(request, {'name': name}, 'hello.html')
        kwargs = {'name': name}
        body = render(template_name='hello.html', **kwargs)
        return Response(body=body, request=request)


class Contacts(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(template_name='contacts.html', **kwargs)
        return Response(body=body, request=request)

    def post(self, request: Request, *args, **kwargs) -> Response:
        from pprint import pprint
        # pprint(request.environ)
        # print(f'Post запрос:{request.POST}')
        body = render(template_name='contacts.html')
        return Response(body=body, request=request)
