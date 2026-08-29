# =============================================================================
# models.py = データの形(DBの表)を決める場所
#
#   1つのクラス = DBの1つの表。1行 = 1件のデータ。
#       class Post  →  main_post 表
#
#   この設計図があるおかげで、SQLを書かずに
#       Post.objects.all()      → 全件取得
#       Post.objects.create()   → 1件追加
#   と書ける。
#
# ▼ ★ユーザーの表は自分で作らない
#
#   Djangoには最初からユーザーの表(User)が付いてくる。
#   パスワードを元に戻せない形で保存する処理も、ログインの判定も入っているので、
#   自分で作る必要がない。ここが Django が「全部入り」と言われる理由の1つ。
#
# ▼ ★モデルを変えたら必ず2つのコマンドを打つ
#
#       python manage.py makemigrations   … 変更内容の指示書を作る
#       python manage.py migrate          … 指示書どおりにDBを変更する
#
#   実行方法は docs/SETUP.md にある。これを忘れると
#   「コードは直したのにDBが古いまま」でエラーになる。
#
# ▼ 書き方の見本
#
#   demo/models.py にサンプル(Todo)があります。
#   ForeignKey(持ち主の紐付け)や Meta(並び順)の書き方はそちらを参照。
# =============================================================================

from django.db import models  # noqa: F401


# =============================================================================
# ★ここから書きはじめる
#
#   class Post(models.Model):
#       title = models.CharField(max_length=200)
#       body = models.TextField(blank=True)
#       created_at = models.DateTimeField(auto_now_add=True)
#
#       def __str__(self) -> str:
#           return self.title
# =============================================================================
