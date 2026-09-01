# =============================================================================
# views.py = 画面(HTML)を返す受付
#
#   ブラウザ「/ をください」 → ここ → 「index.html をどうぞ」
#
# ▼ Djangoでの呼び方
#
#   この「受付の関数」を、Djangoではビュー(view)と呼ぶ。
#   FlaskやGinでいう「ルートの処理」と同じもの。
#
# ▼ 引数の request について
#
#   誰がどのページに何を送ってきたか、という情報が全部入っている。
#   ★書かないとエラーになるので、必ず1つ目に書く。
#       request.POST["username"] … 送信されたフォームの中身
#       request.user             … 今アクセスしている人
#
# ▼ ★書き方の見本
#
#   demo/views.py に、HTMLへ値を渡すサンプルがあります。
# =============================================================================

from django.http import JsonResponse
from django.shortcuts import render  # noqa: F401

# =============================================================================
# ★ここから書きはじめる(URLの登録は main/urls.py)
#
#   def index(request):
#       """トップページ。
#
#       render(request, "index.html", {...}) =
#           templates/index.html を読んで、完成したHTMLを返す。
#       3つ目の辞書がHTML側への差し込み情報で、HTML内の {{ title }} に入る。
#       """
#       return render(request, "index.html", {"title": "ホーム"})
# =============================================================================


def health(request):
    """動作確認用。

    AWSやNginxが「アプリが生きているか」を定期的に確認しに来る先。
    開発中も「画面が出ない…アプリ自体は動いてる?」の切り分けに使える。
    """
    return JsonResponse({"status": "ok"})
