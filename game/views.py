from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView

from .constants import ALLOW_NEGATIVE_POINTS, POINTS_DRAW, POINTS_LOSS, POINTS_WIN
from .domain.blackjack import hand_value, new_game_state, player_hit, player_stand
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

    def form_valid(self, form):
        messages.success(
            self.request,
            "登録が完了しました。ログインしてください。",
        )
        return super().form_valid(form)


@login_required
def game(request):
    """ブラックジャック本体。"""
    state = request.session.get("blackjack_state")
    if not state:
        state = new_game_state()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "new":
            state = new_game_state()
        elif action == "hit":
            state = player_hit(state)
        elif action == "stand":
            state = player_stand(state)

        if state.get("phase") == "finished" and not state.get("result_applied"):
            delta = _apply_points(request.user, state.get("result"))
            state["result_applied"] = True
            result_label = {"win": "勝ち", "lose": "負け", "draw": "引き分け"}[state["result"]]
            messages.info(request, f"結果: {result_label}（ポイント変動 {delta:+d}）")

    request.session["blackjack_state"] = state
    request.session.modified = True

    context = {
        "state": state,
        "player_total": hand_value(state["player"]),
        "dealer_total": hand_value(state["dealer"]),
    }
    return render(request, "game/game.html", context)


def _apply_points(user, result: str) -> int:
    if result == "win":
        delta = POINTS_WIN
    elif result == "lose":
        delta = POINTS_LOSS
    else:
        delta = POINTS_DRAW

    with transaction.atomic():
        user.points += delta
        if not ALLOW_NEGATIVE_POINTS:
            user.points = max(0, user.points)
        user.save(update_fields=["points"])
    return delta
