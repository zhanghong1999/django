from django import forms


# 多继承
class Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有字段，添加样式css：form-control（保留原来的样式）
        for name, field in self.fields.items():
            if field.widget.attrs:
                # 原来有样式
                field.widget.attrs["class"] = "form-control"
            else:
                # 原来没有样式
                field.widget.attrs = {"class": "form-control"}


class BootstrapModelForm(Bootstrap, forms.ModelForm):
    pass


class BootstrapForm(Bootstrap, forms.Form):
    pass
