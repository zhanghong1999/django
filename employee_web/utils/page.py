"""
分页组件
view函数中
    data = {}
    data_list = 表名.objects.filter(**data)
    page_object = Pagination(request, data_list)
    page_data_list = page_object.page_data_list
    page_string = page_object.html()
    context = {
        "data_list": page_data_list,
        "page_string": page_string
    }
    return render(request, "admin_list.html", context)
html中
    {% for item in data_list %}
        <tr>
        <td>{{ item.id }}</td>
        <td>{{ item.username }}</td>
        <td>{{ item.password }}</td>
        </tr>
    {% endfor %}

    <ul class="pagination">
            {{ page_string }}
    </ul>
"""
from django.utils.safestring import mark_safe
from copy import deepcopy


class Pagination(object):
    def __init__(self, request, data_list, page_param="p", page_size=5, plus=5):
        """
        :param request:请求的对象
        :param data_list:待分页的数据
        :param page_param:在url中转递的获取分页的参数
        :param page_size:每页显示的数据条数
        :param plus:当前页码的前后几页
        """
        query_dict = deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        # 当前页
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            # 页码是否为十进制数字
            page = int(page)  # 整型
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_data_list = data_list[self.start:self.end]
        # 数据总条数
        total_count = data_list.count()
        total_page, div = divmod(total_count, page_size)
        if div:
            total_page += 1
        # 数据总页码
        self.total_page = total_page
        self.plus = plus
        self.page_param = page_param

    # 生成页码
    def html(self):

        if self.total_page <= 2 * self.plus + 1:
            # 数据库中的数据少，没有达到2*plus+1
            start_page = 1
            end_page = self.total_page + 1
        else:
            if self.page <= self.plus:
                # 当前页小于5（极小值）
                start_page = 1
                end_page = 2 * self.plus + 1 + 1
            else:
                # 当前页大于5
                if self.page + self.plus > self.total_page:
                    start_page = self.total_page - 2 * self.plus
                    end_page = self.total_page + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1 + 1
        # 页码
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])  # 当前url/1
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])  # 当前url/page - 1
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])  # 当前url/1
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                element = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                element = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(element)

        if self.page < self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            lat = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page])
            lat = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(lat)
        self.query_dict.setlist(self.page_param, [self.total_page])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        # 跳转功能
        search_string = """
        <li>
                <div style="padding-left:10px;float:left;width: 130px">
                    <form method="get">
                        <div class="input-group">
                            <input type="text" class="form-control" name="p">
                            <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">跳转</button>
                    </span>
                        </div>
                    </form>
                </div>
            </li>
        """
        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string
