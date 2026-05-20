from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


def top(request):
    """トップ（仕様 6.1）。"""
    return render(request, "game/top.html")


def user_page(request):
    """ユーザー画面（仕様 6.3）。未ログインは登録・ログインへ誘導。"""
    return render(request, "game/user.html")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


@login_required
def game(request):
    """ゲーム画面（仮）。未ログインは login へリダイレクト。"""
    return render(request, "game/game.html")
