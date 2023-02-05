from jsonpickle import dumps, loads
from application.request import Request
from application.response import Response

from application.templator import render


# behavioral pattern Observer | поведенчевский паттерн наблюдатель
class Observer:
    def update(self):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifire(Observer):

    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifire(Observer):

    def update(self, subject):
        print('EMAIL->', 'к нам присоединился', subject.students[-1].name)


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# behavioral pattern Template Method | поведенчевский паттерн шаблонный метод
class TemplateView:
    template_name = 'template.html'

    def __init__(self):
        self.request = None

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template = self.get_template()
        context = self.get_context_data()
        body = render(template_name=self.template_name, **context)
        return Response(body=body, request=self.request)

    # def __call__(self):
    #     self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context

    def get(self, request: Request):
        self.request = request
        return self.render_template_with_context()


class CreateView(TemplateView):
    template_name = 'create.html'

    def get_request_data(self):
        return self.request.POST

    def create_obj(self):
        pass

    def post(self, request: Request):
        self.request = request
        self.create_obj()
        return self.render_template_with_context()

    def get(self, request: Request):
        self.request = request
        return self.render_template_with_context()


# behavioral pattern Strategy | поведенчевский паттерн стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
