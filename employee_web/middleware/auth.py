from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

"""
每个中间件类都有一个默认的方法列表，
包括 process_request()、process_view()、process_exception()、
process_response() 和 process_template_response() 等方法。
process_request(request):
在请求到达视图函数之前被调用，可用于处理请求头，进行身份验证等。
process_view(request, view_func, view_args, view_kwargs):
在视图函数被调用之前被调用，可以修改视图函数的参数列表，例如为视图函数添加额外的参数，检查请求是否符合权限要求等。
process_exception(request, exception):
在视图函数发生异常时被调用，可以对异常进行处理和转换，例如将特定的异常转换成特定的 HTTP 响应。
process_response(request, response):
在视图函数处理请求并生成响应后被调用，可以对响应进行修改和增强，例如添加额外的 header 信息，压缩响应内容等。
process_template_response(request, response):
只有当响应对象的 template_name 属性不为 None 时才会被调用，可以对模板响应对象进行进一步处理，例如添加额外的上下文或更改模板引擎。

以上方法的返回值可以是 None 或 HttpResponse 对象，
如果返回 None，则表示继续执行下一个中间件的对应方法；
如果返回 HttpResponse 对象，则表示直接中止并返回这个响应。

"""


class Start(MiddlewareMixin):
    def process_request(self, request):
        # 排除不需要登录的页面
        # request.path_info 获得当前用户请求的URL
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 读取当前访问的用户session信息
        info = request.session.get("info")
        if not info:
            return redirect("/login/")
        return
