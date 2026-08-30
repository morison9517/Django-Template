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
# =============================================================================

from django.db import models  # noqa: F401


# =============================================================================
# ★ここから書きはじめる
#
#   from django.conf import settings
#
#   class Post(models.Model):
#       title = models.CharField(max_length=200)
#       body = models.TextField(blank=True)
#
#       # ▼ 他の表と紐付けたいとき(「この投稿は誰が書いたか」)
#       #
#       #   settings.AUTH_USER_MODEL … ユーザーの表を指す決まった書き方。
#       #                              User を直接書かない(後で差し替えられるように)
#       #   on_delete=CASCADE        … ユーザーが消えたら、その人の投稿も一緒に消す
#       #   null=True, blank=True    … 持ち主なしでも保存できる
#       #                              (ログイン機能をOFFにしても動く)
#       #   related_name             … 逆に user.posts で一覧が取れるようになる
#       user = models.ForeignKey(
#           settings.AUTH_USER_MODEL,
#           on_delete=models.CASCADE,
#           null=True,
#           blank=True,
#           related_name="posts",
#       )
#
#       created_at = models.DateTimeField(auto_now_add=True)
#
#       class Meta:
#           # 取り出すときの並び順。"-" を付けると新しい順。
#           # ★ここで決めておくと、取得のたびに並び替えを書かなくて済む。
#           ordering = ["-id"]
#
#       def __str__(self) -> str:
#           """管理画面などで1件を表す文字。これが無いと「Post object (1)」と出る。"""
#           return self.title
# =============================================================================
