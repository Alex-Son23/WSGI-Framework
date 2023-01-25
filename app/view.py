from datetime import datetime

from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.structural_patterns import Debug
from patterns.creational_patterns import Engine, Logger, MapperRegistry
from patterns.behavioral_patterns import CreateView, ListView, EmailNotifire, SmsNotifire
from application.request import Request
from application.view import View
from application.response import Response
from application.template_engine import build_template
from application.templator import render

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifire()
sms_notifire = SmsNotifire()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


class Homepage(View):

    @Debug(name='Homepage')
    def get(self, request, *args, **kwargs):
        body = render(template_name='index.html')
        return Response(body=body, request=request)

    def post(self, request: Request, *args, **kwargs) -> Response:
        body = render(template_name='index.html')
        return Response(body=body, request=request)


class EpicMath(View):

    def get(self, request: Request, *args, **kwargs):
        first = request.GET.get('first')
        if not first or not first[0].isnumeric():
            return Response(body=f'first пустое либо не является числом', request=request)

        second = request.GET.get('second')
        if not second or not second[0].isnumeric():
            return Response(body=f'second пустое либо не является числом')

        return Response(body=f'Сумма {first[0]} и {second[0]} равна {int(first[0]) + int(second[0])}', request=request)


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
        body = render(template_name='contacts.html')
        return Response(body=body, request=request)


class About(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(template_name='about.html', **kwargs)
        return Response(body=body, request=request)

        # body = render(template_name='contacts.html', **kwargs)
        # return Response(body=body, request=request)

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass


class CategoryList(View):

    @Debug(name='Category List')
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.log('get category list')
        kwargs = {"objects_list": site.categories}
        body = render(template_name='category_list.html', **kwargs)
        return Response(body=body, request=request)


class CreateCategory(View):

    @Debug(name='Create category GET')
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.log('get create category')
        body = render(template_name="create_category.html")
        return Response(body=body, request=request)

    @Debug(name='Create category POST')
    def post(self, request: Request, *args, **kwargs) -> Response:
        logger.log('post create category')
        raw_name = request.POST.get('name')[0]
        site.create_category(raw_name)
        kwargs = {"objects_list": site.categories}
        body = render(template_name='category_list.html', **kwargs)
        return Response(body=body, request=request)


class CoursesList(View):

    @Debug(name='Courses List GET')
    def get(self, request: Request, *args, **kwargs) -> Response:
        # try:
        logger.log('get courses list')
        category = site.find_category_by_id(int(request.GET.get('id')[0]))
        body = render(template_name="course_list.html", objects_list=site.courses, name=category.name, id=category.id)
        return Response(body=body, request=request)
        # except KeyError:
        #     body = render(template_name="course_list.html")
        #     return Response(body=body, request=request)


class CreateCourse(View):

    @Debug(name='Create Courses GET')
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.log('get create course')
        category_id = int(request.GET.get('id')[0])
        category = site.find_category_by_id(category_id)
        body = render(template_name="create_course.html", name=category.name, id=category.id)
        return Response(body=body, request=request)

    @Debug(name='Create Courses POST')
    def post(self, request: Request, *args, **kwargs) -> Response:
        logger.log('post create course')
        category_id = int(request.GET.get('id')[0])
        category = site.find_category_by_id(category_id)
        name = request.POST.get('name')[0]
        type_ = request.POST.get('type')[0]
        course = site.create_course(type_, name, category)
        course.observers.append(email_notifier)
        course.observers.append(sms_notifire)
        site.courses.append(course)
        body = render(template_name="course_list.html", objects_list=category.courses, name=category.name,
                      id=category.id)
        return Response(body=body, request=request)


class CopyCourse(View):

    # def get(self, request: Request, *args, **kwargs) -> Response:
    #     kwargs = {"objects_list": site.categories}
    #     body = render(template_name='category_list.html', **kwargs)
    #     return Response(body=body, request=request)
    @Debug(name='Copy Courses GET')
    def get(self, request: Request, *args, **kwargs) -> Response:
        logger.log('copy course')
        name = request.GET.get('name')[0]

        old_course = site.get_course(name)
        if old_course:
            new_name = f'copy_{name}'
            new_course = old_course.clone()
            new_course.name = new_name
            site.courses.append(new_course)

            body = render(template_name="course_list.html", objects_list=new_course.category.courses,
                          name=new_course.category.name, )
            resp = Response(body=body, request=request)
            return resp


class StudentList(ListView):
    queryset = site.students
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


class CreateStudent(CreateView):
    template_name = 'create_student.html'

    def create_obj(self):
        data = self.get_request_data()
        new_obj = site.create_user('student', data['name'][0])
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_request_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self):
        data = self.get_context_data()
        course_name = site.decode_value(data['course_name'][0])
        course = site.get_course(course_name)
        student_name = site.decode_value(data['student_name'][0])
        student = site.get_student(student_name)
        course.add_student(student)
