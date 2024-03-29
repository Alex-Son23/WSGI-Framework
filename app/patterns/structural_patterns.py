# структурный паттерн декратор
from time import time


class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    def __init__(self, name):
        self.name = name

    # def __call__(self, cls):
    #
    #     def timeit(method):
    #
    #         def timed(*args, **kwargs):
    #             ts = time()
    #             result = method(*args, **kwargs)
    #             te = time()
    #             delta = ts - te
    #
    #             print(f'DEBUG ----> {self.name} выполняется за {delta}')
    #             return result
    #
    #         return timed
    #     return timeit(cls)
    def __call__(self, cls):
        '''
        сам декоратор
        '''

        # это вспомогательная функция будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            # print(method)
            '''
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            '''
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)


