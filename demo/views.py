# =============================================================================
# デモページの受付。
#
#   ここは「動いていることを確認するための画面」です。
#   自分たちの画面は main/views.py に書きます。
# =============================================================================

from django.db import connection
from django.shortcuts import render


def index(request):
    """デモページ。

    この関数は2つのURLから使われる(登録は demo/urls.py):
        /        … main/urls.py にまだトップページが無いとき
        /__demo  … いつでも
    """
    db_status, db_message = _check_db()

    return render(
        request,
        "demo/index.html",
        {
            "title": "セットアップ確認",
            "db_status": db_status,
            "db_message": db_message,
        },
    )


def _check_db() -> tuple[str, str]:
    """DBに繋がるか実際に試す。

    「SELECT 1」という最小の質問を投げ、返事が来るかで判定している。

    try/except で囲む理由:DBが起動しきっていないだけでこの画面が
    エラーになると原因が分かりにくい。画面は出しつつ「DBだけ未接続」と
    伝えたほうが切り分けが速い。
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return "ok", ""
    except Exception as exc:
        # DBのエラー文は数百文字になることがあるので先頭120文字だけ表示する。
        return "ng", str(exc)[:120]
