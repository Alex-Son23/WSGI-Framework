from application.urls import Url
from view import Homepage, EpicMath, Hello, Contacts, About, CategoryList, CreateCategory, CoursesList, CreateCourse, \
    CopyCourse, CreateStudent, StudentList, AddStudentByCourseCreateView

urlpatterns = [
    Url('^$', Homepage),
    Url('^/math$', EpicMath),
    Url('^/hello$', Hello),
    Url('^/contacts$', Contacts),
    Url('^/about$', About),
    Url('^/category-list$', CategoryList),
    Url('^/create-category$', CreateCategory),
    Url('^/courses-list$', CoursesList),
    Url('^/copy-course$', CopyCourse),
    Url('^/create-course$', CreateCourse),
    Url('^/create-student$', CreateStudent),
    Url('^/student-list$', StudentList),
    Url('^/add-student', AddStudentByCourseCreateView),
]