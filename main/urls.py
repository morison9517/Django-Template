# =============================================================================
# urls.py = このアプリが担当するURLの一覧
#
# ▼ ★画面を1枚増やすときの手順
#
#   1. templates/ にHTMLを1枚置く
#   2. views.py に関数を書く
#   3. ここに path(...) を1行足す
#
# ▼ name="..." について
#
#   URLに名前を付けておくと、HTML側から
#       <a href="{% url 'main:index' %}">
#   と書ける。URLを直書きせず名前で呼ぶと、
#   後からURLを変えても呼び出し側を直さずに済む。
# =============================================================================

from django.urls import path

from main import api, views

# このアプリのURLにまとめて名札を付ける。
# HTMLからは "main:index" のように「アプリ名:URL名」で呼ぶ。
app_name = "main"

urlpatterns = [
    # --- 画面を返すURL ---
    path("", views.index, name="index"),
    path("health", views.health, name="health"),
    # --- JavaScript向けにデータを返すURL ---
    #
    # <int:todo_id> = URLのこの部分を数字として受け取り、
    #                 ビューの引数 todo_id に渡す、という指定。
    path("api/todos", api.list_todos, name="api_list_todos"),
    path("api/todos/create", api.create_todo, name="api_create_todo"),
    path("api/todos/<int:todo_id>", api.toggle_todo, name="api_toggle_todo"),
    path("api/todos/<int:todo_id>/delete", api.delete_todo, name="api_delete_todo"),
]
