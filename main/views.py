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
# =============================================================================

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """トップページ。

    render(request, "index.html", {...}) =
        templates/index.html を読んで、完成したHTMLを返す。
    3つ目の辞書がHTML側への差し込み情報で、HTML内の {{ title }} などに入る。
    """
    db_status, db_message = _check_db()

    return render(
        request,
        "index.html",
        {
            "title": "ホーム",
            "db_status": db_status,
            "db_message": db_message,
        },
    )


def _check_db() -> tuple[str, str]:
    """DBに繋がるか実際に試す。

    「SELECT 1」という最小の質問を投げ、返事が来るかで判定している。

    try/except で囲む理由:DBが起動しきっていないだけでトップページが
    エラー画面になると原因が分かりにくい。画面は出しつつ「DBだけ未接続」と
    伝えたほうが切り分けが速い。
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return "ok", ""
    except Exception as exc:
        # DBのエラー文は数百文字になることがあるので先頭120文字だけ表示する。
        return "ng", str(exc)[:120]


def health(request):
    """動作確認用。

    AWSやNginxが「アプリが生きているか」を定期的に確認しに来る先。
    開発中も「画面が出ない…アプリ自体は動いてる?」の切り分けに使える。
    """
    return JsonResponse({"status": "ok"})
