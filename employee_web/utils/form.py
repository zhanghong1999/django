from django import forms
from employee_web.models import UserInfo, PrettyNum, Admin
from employee_web.utils.bootstrap import BootstrapModelForm
from employee_web.utils.encrypt import md5

from django.core.exceptions import ValidationError


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        # 输入密码时不显示
        widget=forms.PasswordInput
        # widget=forms.PasswordInput(render_value=True)
        # 输入不一致后不清空
    )

    class Meta:
        model = Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            # 输入密码时不显示
            "password": forms.PasswordInput
            # "password": forms.PasswordInput(render_value=True)
            # 输入不一致后不清空
        }

    # 密码加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        confirm = self.cleaned_data.get("confirm_password")
        # 加密
        confirm = md5(confirm)
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # return 返回什么，数据库中该字段保存什么
        # （此处的confirm_password不用保存到数据库）
        return confirm


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = Admin
        fields = ["username"]

    # 用户名不重复
    def clean_username(self):
        txt_username = self.cleaned_data.get("username")
        # self.instance.pk 主键 即id
        flag = Admin.objects.filter(username=txt_username).exclude(id=self.instance.pk).exists()
        if flag:
            raise ValidationError("用户名已存在")
        return txt_username


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        # self.cleaned_data 通过校验的字段的数据
        pwd = self.cleaned_data.get("password")
        pwd_md5 = md5(pwd)
        flag = Admin.objects.filter(password=pwd_md5, id=self.instance.pk).exists()
        if flag:
            raise ValidationError("不能为原密码")
        return pwd_md5

    def clean_confirm_password(self):
        confirm = self.cleaned_data.get("confirm_password")
        confirm = md5(confirm)
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


# 添加员工(ModelForm方法)
# 创建类
class UserModelForm(BootstrapModelForm):
    class Meta:
        model = UserInfo
        # 只用部分字段 如：只要姓名，密码和年龄
        # fields = ["name", "password", "age"]
        # 全部字段
        fields = "__all__"


class NumModelForm(BootstrapModelForm):
    # # 增加校验，方法1
    # mobile = forms.CharField(
    #     label="号码",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '格式错误')]
    #     # 正则表达式，^开头，$结尾
    # )

    class Meta:
        model = PrettyNum
        # fields = ["mobile", "price", "level"]  # 只要mobile, price, level字段
        fields = "__all__"  # 所有字段
        # exclude = ["level", "status"]  # 排除level和status字段

    # # 增加校验，方法2
    # def clean_mobile(self):
    #     # 获取用户传入的数据
    #     txt_mobile = self.cleaned_data["mobile"]
    #     # 验证号码位数为11
    #     if len(txt_mobile) != 11:
    #         # 显示错误
    #         raise ValidationError("格式错误")
    #     # 返回数据
    #     return txt_mobile

    # 号码不重复
    def clean_mobile(self):
        # 获取用户传入的数据
        txt_mobile = self.cleaned_data["mobile"]
        # 数据库中查询该字段是否存在该数据
        flag = PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if flag:
            raise ValidationError("号码已存在")
        return txt_mobile


class NumEditModelForm(forms.ModelForm):
    # # 1.显示手机号，但无法修改
    # mobile = forms.CharField(disabled=True, label="号码")

    class Meta:
        model = PrettyNum
        # 2.不显示手机号
        # fields = ["price", "level", "status"]  # 只要mobile, price, level字段
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加样式css：form-control
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    # 号码不重复
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # self.instance.pk 主键 即id
        # mobile相同&&id不相同
        flag = PrettyNum.objects.filter(mobile=txt_mobile).exclude(id=self.instance.pk).exists()
        if flag:
            raise ValidationError("号码已存在")
        return txt_mobile
