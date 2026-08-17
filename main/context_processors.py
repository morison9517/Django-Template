# =============================================================================
# context_processors.py = 全ページで自動的に使える情報を足す場所
#
# ▼ ★Djangoの便利な仕組み
#
#   ふつう、HTMLに渡す情報はビュー(views.py)で毎回書く必要がある。
#   でもサイト名のように「全ページで使うもの」を毎回書くのは無駄だし、
#   1か所でも書き忘れると、その画面だけ表示が欠ける。
#
#   ここに書いておけば、どのページのHTMLからでも使えるようになる。
#       {{ SITE_NAME }}
#       {{ AUTH_ENABLED }}
#
#   登録は config/settings.py の context_processors に済ませてある。
#
#   ※ {{ user }}(今アクセスしている人)と {{ messages }}(お知らせ)は
#     Djangoが最初から用意しているので、ここに書かなくても使える。
# =============================================================================

from django.conf import settings


def site_settings(request) -> dict:
    """全ページで使う共通の情報を返す。"""
    return {
        # ★プロダクト名が決まったらここを変える。
        #   全ページのタイトルとヘッダーに反映される。
        "SITE_NAME": "Django Template Demo",
        "AUTH_ENABLED": settings.AUTH_ENABLED,
    }
