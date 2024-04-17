"""
自定义分页组件
使用步骤：

在试图函数中
from app01.utils.pagination import Pagination

    def pnumber_list(request):
        #Step1:根据情况获取数据
        queryset = PrettyNum.objects.all()

        #Step2:实例化Pagination对象
        page_object = Pagination(request, queryset)

        #Step3:返回值
        content = {
            "models": page_object.page_queryset,  # 分页完的数据
            "page_str": page_object.html(),  # 生成页码 替换html占位符中内容
        }
        return render(request, "pnumber_list.html", content)

在html中
        # 数据  上方return中的content中的models是重点 具体如何循环取什么具体分息
        {% for item in models %}
            <tr>
                <td>{{ item.id }}</td>
                <td>{{ item.mobile }}</td>
                <td>{{ item.price }}</td>
                <td>{{ item.get_level_display }}</td>
                <td>{{ item.get_state_display }}</td>
                <td>
                    <a class="btn btn-primary btn-xs" href="/pnumber/{{ item.id }}/edit/">编辑</a>
                    <a class="btn btn-danger btn-xs" href="/pnumber/{{ item.id }}/delete/">删除</a>
                </td>
            </tr>
        {% endfor %}



        # 分页 照搬
        <ul class="pagination">
            {{ page_str }}
        </ul>

"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", distance=5):
        """
        :param request:  请求对象
        :param queryset: 查询的符合条件的数据，以此进行分页处理
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中get请求获取的页码参数
        :param distance: 显示当前页的前后distance页
        """

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        # 至此取到get请求的页码数 默认1
        self.page = page
        # 每页展示的数据量 默认10
        self.page_size = page_size
        # 每一页的起始数据项
        self.start = (page - 1) * page_size
        # 每一页的截止数据项
        self.end = page * page_size
        # 将查询到的数据按当前页码截取一个page_size大小的数据量
        self.page_queryset = queryset[self.start:self.end]

        # .count()计数 得总数据数
        total_count = queryset.count()
        # divmod(a,b) 除法 得商和余数
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        # 此时total_page_count为总页码数
        self.total_page_count = total_page_count
        self.distance = distance

    def html(self):

        # 当前页码的前五页和后五页

        # 数据较少
        if self.total_page_count <= 2 * self.distance + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据较多

            # 当前页小于distance 避免start_page = (distance - 5)<=0
            if self.page <= self.distance:
                start_page = 1
                end_page = 2 * self.distance + 1
            else:
                # 当前页大于total_page_count-disatance 避免end_page = （page + distance）超过实际页码数
                if self.page > self.total_page_count - self.distance:
                    start_page = self.total_page_count - 2 * self.distance - 1
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.distance
                    end_page = self.page + self.distance

        """ 生成页码传回前端"""

        self.query_dict.setlist(self.page_param, [1])

        # 首页
        page_str_list = ['<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())]
        # 前一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)

        # range() 前取后不取 所以要+1
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                element = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            # <li><a href="?page=i">i</a></li>
            else:
                element = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(element)

        # 后一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nextt = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nextt = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(nextt)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        # 跳转页
        search_str = """
            <li>
                <form method="get" style="float: right;margin-left:-1px">
                    <input type="text"
                           style="position: relative;float: left;display: inline-block;width: 100px;border-radius: 0"
                           class="form-control" placeholder="输入页码..." name="page">
                    <button style="border-radius: 0" class="btn btn-default" type="button">点击跳转!</button>
                </form>
            </li>"""
        page_str_list.append(search_str)

        # .join()用str将item的每个成员连接起来
        # mark_safe() 认为字符串安全 可以当作html源码渲染
        page_str = mark_safe("".join(page_str_list))
        return page_str
