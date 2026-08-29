# =============================================================================
# urls.py = このアプリが担当するURLの一覧
#
# ▼ ★画面を1枚増やすときの手順
#
#   1. templates/ にHTMLを1枚置く
#   2. views.py に関数を書く
#   3. ここに path(...) を1行足す
#
# ▼ ★トップページはまだ空いています
#
#   今 "/" を開くとデモページが出ますが、それは「ここにまだ "" が
#   無いから」です。下の見本のように path("", ...) を1行足せば、
#   Djangoは先に書いたほうを使うので、自分たちの画面に入れ替わります。
#   デモを消す作業は要りません(仕組みは demo/__init__.py)。
#
# ▼ name="..." について
#
#   URLに名前を付けておくと、HTML側から
#       <a href="{% url 'main:posts' %}">
#   と書ける。URLを直書きせず名前で呼ぶと、
#   後からURLを変えても呼び出し側を直さずに済む。
# =============================================================================

from django.urls import path

from main import views

# このアプリのURLにまとめて名札を付ける。
# HTMLからは "main:health" のように「アプリ名:URL名」で呼ぶ。
app_name = "main"

urlpatterns = [
    # --- 画面を返すURL ---
    #
    # ★ここから書きはじめる(コメントを外す)
    # path("", views.index, name="index"),
    path("health", views.health, name="health"),
    # --- JavaScript向けにデータを返すURL ---
    #
    # <int:post_id> = URLのこの部分を数字として受け取り、
    #                 ビューの引数 post_id に渡す、という指定。
    # path("api/posts", api.list_posts, name="api_list_posts"),
    #
    # ※ api を使うときは、上の import に足すこと:
    #     from main import api, views
]
