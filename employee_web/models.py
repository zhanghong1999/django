from django.db import models


# 管理员表employee_web_admin
class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


# 部门表employee_web_department
class Department(models.Model):
    title = models.CharField(verbose_name="部门名称", max_length=32)

    # verbose_name="部门名称"相当于备注title是部门名称

    def __str__(self):
        # 输出这个类的对象，__str__可以定义输出内容
        return self.title
        # 输出Department类的对象，__str__可以定义输出为self.title


# 员工表employee_web_userinfo
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")

    choice_gender = (
        (1, "男"),
        (2, "女"),
    )  # 元组类型
    gender = models.SmallIntegerField(verbose_name="性别", choices=choice_gender)
    # choice 添加django的约束  给这个参数赋值时得用元组
    money = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # DecimalField(max_digits数字总长度（不包括正负号），decimal_places数字的小数点后几位)
    time = models.DateTimeField(verbose_name="入职时间")
    # 没有约束 没有和表employee_management_department关联
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 一般不提倡外键
    # 有约束 设置外键depart = models.ForeignKey(to="Department", to_field="id") --->属于数据库的约束
    # to=关联的表名，to_field=关联的字段名（列）
    # 生成表后，django会自动在此字段名后加上_id，所以实际表中的字段名是depart_id
    # 当其中部门删除时，可以有两种，外键字段必须设置on_delete
    # 1.级联删除 删除该部门的员工
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

    # 2.置空 该部门的员工的部门为空
    # depart = models.ForeignKey(to="Department", to_title="id", null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name


class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name="号码", max_length=11)
    price = models.IntegerField(verbose_name="价格", null=True, blank=True, default=0)

    choice_level = (
        (1, "Ⅰ级"),
        (2, "Ⅱ级"),
        (3, "Ⅲ级"),
    )  # 元组类型
    level = models.SmallIntegerField(verbose_name="级别", choices=choice_level, default=1)

    choice_status = (
        (1, "已占用"),
        (2, "未占用"),
    )  # 元组类型
    status = models.SmallIntegerField(verbose_name="状态", choices=choice_status, default=2)


# 消息表
class News(models.Model):
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详情")
    choice_level = (
        (1, "日常"),
        (2, "重要"),
        (3, "紧急"),
    )
    level = models.SmallIntegerField(verbose_name="类型", choices=choice_level, default=1)
    admin = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


# 订单表
class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=64)
    name = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    choice_status = (
        (1, "未支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=choice_status, default=1)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
