# =============================================================================
# デモ用のデータの形。
#
#   ★このアプリは DEBUG=True のときだけ読み込まれるので、
#     この表(demo_todo)は本番のDBには作られません。
#
#   自分たちの表は main/models.py に書きます。書き方の見本としてどうぞ。
# =============================================================================

from django.conf import settings
from django.db import models


class Todo(models.Model):
    """やることリスト1件分(デモ)。"""

    # ★ID(1,2,3…の通し番号)は書かなくても自動で作られる。

    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    # ForeignKey = 「この項目はユーザーの表の誰か」という紐付け。
    #
    #   on_delete=CASCADE … ユーザーが消えたら、その人のTodoも一緒に消す
    #   null=True         … 持ち主なしでも保存できる(ログイン機能をOFFにしても動く)
    #   related_name      … 逆に user.todos で、その人のTodo一覧が取れるようになる
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="todos",
    )

    # auto_now_add=True = 保存時に現在時刻を自動で入れる。入れ忘れる事故がなくなる。
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 取り出すときの並び順。"-" を付けると新しい順。
        # ★ここで決めておくと、取得のたびに並び替えを書かなくて済む。
        ordering = ["-id"]

    def __str__(self) -> str:
        """管理画面などで1件を表す文字。これが無いと「Todo object (1)」と出る。"""
        return self.title

    def to_dict(self) -> dict:
        """JavaScriptに渡せる形(JSONにできる辞書)に変換する。

        ★ここで返す形が、そのままJavaScript側で受け取る形になる。
          項目名を変えるときは demo/static/demo/todo.js も一緒に直す。
        """
        return {
            "id": self.id,
            "title": self.title,
            "is_done": self.is_done,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
        }
