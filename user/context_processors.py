from .forms import LoginForm

# 此方法创建以后需要在sett设置路径，以后可以直接调用
def login_modal_form(request):
    return {'login_modal_form': LoginForm()}