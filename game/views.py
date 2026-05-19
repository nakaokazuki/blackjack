from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


def top(request):
    """トップ（仮）。第 6 章で本格実装。"""
    return render(request, "game/top.html")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


@login_required
def game(request):
    """ゲーム画面（仮）。未ログインは login へリダイレクト。"""
    return render(request, "game/game.html")
