# =============================================================================
# urls.py = URLの受付(親)
#
#   ブラウザ「/ をください」 → ここ → 担当のアプリへ振り分け
#
# ▼ ★2段構えになっている
#
#   ここは「どのアプリに任せるか」だけを決める案内所。
#   実際のURLは、各アプリの urls.py に書く。
#
#       config/urls.py    … /auth/ で始まるものは accounts に任せる  ← このファイル
#       main/urls.py      … / や /api/○○ など、自分たちで作るURL
#       accounts/urls.py  … /auth/login など
#
#   全URLを1ファイルに書くと巨大になり、6人で編集したとき必ず衝突する。
#   アプリごとに分けておけば別ファイルを触るので衝突しない。
#
# ▼ このファイルは基本的に触らない
#
#   URLを増やすときに触るのは main/urls.py や accounts/urls.py。
#   ここを触るのは「新しいアプリを作ったとき」だけ。
# =============================================================================

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # ★管理画面。Djangoが最初から用意してくれている、データの編集画面。
    #   http://localhost:8000/admin/ で開ける(使い方は docs/SETUP.md)。
    path("admin/", admin.site.urls),
    # include(...) = 「この先は main アプリの urls.py に任せる」という指定。
    path("", include("main.urls")),
]

# ★AUTH_ENABLED が False なら、ログイン関連のURLを登録しない。
#   コードを消さずに機能をOFFにできる。
if settings.AUTH_ENABLED:
    urlpatterns += [
        # "auth/" を付けると、accounts/urls.py の "login" が
        # 実際には "/auth/login" になる。
        path("auth/", include("accounts.urls")),
    ]

# --- 利用者が上げたファイル(プロフィールアイコンなど) ---
# ★開発モードのときだけ、Djangoが自分で画像を配る。
#   本番ではNginxが配るので、ここは登録しない(compose.prod.yml 参照)。
#   Djangoに画像配りをさせると遅いうえ、本番では動かないようになっている。
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --- デモ(動作確認用のページ) ---
# ★必ず最後に足す。
#   Djangoは上から順に照合して最初に一致したものを使うので、
#   main/urls.py に path("", ...) を書けば、そちらが勝ってデモは出なくなる。
#   開発モードのときだけ。本番では登録しないので絶対に出ない。
if settings.DEBUG:
    urlpatterns += [path("", include("demo.urls"))]
