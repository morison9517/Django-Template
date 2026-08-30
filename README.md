# Django Template Demo

**Team AIB** のハッカソン用Django開発テンプレート。
**`docker compose up` だけで、アプリとDBが揃った開発環境が立ち上がります。**

> リポジトリ名は `case_django`、画面上の表示名は `Django Template Demo` です。
> プロダクト名が決まったら、表示名は `main/context_processors.py` の
> `SITE_NAME` の1か所を直してください(全ページのタイトルとヘッダーに反映されます)。

---

## いきなり動かす

```bash
# 1. 金庫を作る(初回だけ)
cp .env.example .env          # Windows: Copy-Item .env.example .env

# 2. 起動する
docker compose up --build

# 3. 管理画面に入るアカウントを作る(別のターミナルで、初回だけ)
docker compose exec web python manage.py createsuperuser
```

→ <http://localhost:8000> を開く
→ 管理画面は <http://localhost:8000/admin/>

**DBに表を作るコマンドはありません。** 起動のたびに自動で用意されます。

うまくいかないときは **[docs/SETUP.md](docs/SETUP.md)** を見てください。困ったときの対処が全部書いてあります。

---

## 最初に出るデモページについて

起動して `/` を開くと「セットアップ完了 🎉」というデモページが出ます。
**これは消さなくて大丈夫です。** Djangoの初期画面(The install worked successfully!)と同じ仕組みで、条件を満たすと自動で出なくなります。

| | |
| --- | --- |
| 出る条件 | `DEBUG=True` **かつ** `main/urls.py` にまだ `path("", ...)` が無いとき |
| 消える条件 | `main/urls.py` の `path("", ...)` を1行足す(それだけ) |
| 本番 | `DJANGO_DEBUG=False` では最初から出ない。デモ用の表もDBに作られない |
| あとで見たい | `/__demo` で開ける(開発モードのときだけ) |

```python
# main/urls.py のこの行のコメントを外した瞬間、デモは出なくなります
urlpatterns = [
    path("", views.index, name="index"),
    ...
]
```

Djangoは**上から順に照合して最初に一致したURLを使う**ので、`main` のほうが先に読み込まれていれば自動的にそちらが勝ちます。

デモの画面は**1枚で完結しています**(`base.html` も `style.css` も `main.js` も使いません)。
デモの役目は「セットアップが動いているか」を見せる計器なので、共通ファイルに頼らせていません。
おかげで `base.html` を自分たちの見た目に作り替えても、この計器だけは最後まで正しく動きます。
ページの書き方の見本は `templates/login.html` を見てください(`base.html` を継いだ本物のページです)。

デモ一式は `demo/` にまとまっています。不要になったらフォルダごと削除して、`config/settings.py` と `config/urls.py` の「デモ」の各3行を消してください。

---

## 使っている技術

| 分類 | 技術 |
| --- | --- |
| フロント | 素のHTML / CSS / JavaScript(Djangoテンプレート) |
| バック | Python 3.13 / Django 5.2(LTS) |
| DB | MySQL 8.4(確認は DBeaver、ポートは **3309**) |
| 環境 | Docker Compose |
| 本番 | Nginx / AWS / gunicorn |
| 部品管理 | uv |

> Django 5.2 は **LTS(長期サポート版)** です。最新版より解説記事が多く、
> 調べ物をしたときに情報が見つかりやすいので、あえてこちらを選んでいます。

---

## ★Djangoの一番の強み:自分で作らなくていいものが多い

他の2つ(Flask版・Gin版)では自分で書いていたものが、Djangoでは最初から付いてきます。

| 機能 | Flask版・Gin版 | Django版 |
| --- | --- | --- |
| ユーザーの表 | 自分で設計する | **最初からある** |
| パスワードの安全な保存 | 自分で書く | **`create_user()` がやる** |
| パスワードの強さチェック | 自分で条件を書く | **設定済み(日本語で警告)** |
| 管理画面 | 無い | **`/admin/` が最初からある** |
| DBの形の変更 | 作り直し(データが消える) | **データを保ったまま変更できる** |

**特に管理画面はハッカソンで効きます。**
デモ用のデータを画面から手で入れられるので、入力画面を作る前にデモの形が作れます。

---

## フォルダの地図

「アプリ = 1軒のお店」だと思って読んでください。

```
case_django/
├── manage.py               お店の道具箱(コマンドの入口)
│
├── config/                 お店全体の決まりごと
│   ├── settings.py         設定を1か所に集める(★ここに書いた機能だけが動く)
│   ├── urls.py             URLの振り分け(親)
│   └── wsgi.py / asgi.py   本番サーバーとの接続口(触らない)
│
├── main/                   売り場①:画面とAPI(★ここに書く)
│   ├── models.py           データの形(DBの表)を決める
│   ├── views.py            画面(HTML)を返す
│   ├── api.py              JavaScript向けにデータだけ返す
│   ├── urls.py             このアプリが担当するURL
│   ├── admin.py            管理画面での見せ方
│   ├── context_processors.py  全ページで使う共通の情報
│   └── migrations/         DBの変更履歴(★必ずコミットする)
│
├── accounts/               売り場②:ログイン・新規登録
│   ├── views.py
│   └── urls.py
│
├── demo/                   売り場③:動作確認用のデモ(開発モード限定・触らない)
│                           1枚完結なので、書き方の見本は login.html を見ること
│
├── templates/              お客さんが見るHTML(base.html が共通の型紙)
├── static/                 CSS / JS / 画像
│
├── docs/                   チームで見る手順書
├── tools/                  開発中だけ使う小道具スクリプト
│
├── compose.yml             アプリとDBをまとめて動かす段取り表
├── Dockerfile              箱を組み立てるレシピ
├── pyproject.toml          買い物リスト(必要な部品の一覧)
├── uv.lock                 レシート(全員が同じバージョンを使うための記録)
│
├── .vscode/                チーム共通のエディタ設定
│
├── .env                    金庫(★GitHubに上げない)
└── .env.example            金庫の中身の見本(こちらは上げる)
```

> **「アプリ」という言葉について**
> Djangoでは、機能のまとまりを「アプリ」と呼びます。お店でいう売り場です。
> 1つの売り場に、データの形・処理・URLがセットで入っています。
> 増やすときは `python manage.py startapp <名前>` で作り、
> `config/settings.py` の `INSTALLED_APPS` に1行足します。

---

## 担当ごとに触る場所

**基本的に他の人と同じファイルを触らないように分けてあります。** これでコンフリクト(変更の取り合い)がほぼ起きません。

| 担当 | 触る場所 |
| --- | --- |
| 見た目 | `templates/` `static/css/` |
| 画面の動き | `static/js/` |
| データの形 | `main/models.py` |
| URLと処理(画面) | `main/views.py` `main/urls.py` |
| URLと処理(データ) | `main/api.py` |
| ログイン | `accounts/` |

`config/` `compose.yml` `Dockerfile` は**土台**です。
触る必要が出たら、**先にチームに共有してから**変更してください(全員に影響します)。

---

## ページを1枚増やす手順

1. **`templates/` にHTMLを1枚置く**(`index.html` をコピーするのが早い)

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h1>マイページ</h1>
   {% endblock %}
   ```

   > ヘッダーとフッターは書きません。`base.html` から自動的に付きます。
   > ★`{% extends %}` は必ず1行目に書いてください。

2. **`main/views.py` に関数を書く**

   ```python
   def my_page(request):
       return render(request, "mypage.html", {"title": "マイページ"})
   ```

3. **`main/urls.py` に1行足す**

   ```python
   path("mypage", views.my_page, name="my_page"),
   ```

4. 保存して2〜3秒待つ → <http://localhost:8000/mypage>

ログインしている人だけに見せたいときは、1行足すだけです。

```python
from django.contrib.auth.decorators import login_required

@login_required          # ← これを足す
def my_page(request):
    ...
```

未ログインの人は、自動でログイン画面へ案内され、
**ログイン後に元のページへ戻してもらえます。**

---

## base.html(型紙)の仕組み

**今回いちばん新しい考え方なので、ここだけ先に押さえてください。**

ヘッダーとフッターを全ページにコピペすると、直すときに全ファイルを回ることになります。
そこで**共通部分を1枚の「型紙」にまとめ、各ページは真ん中の中身だけを書く**形にしています。

```
base.html(型紙)                    index.html(中身)
┌──────────────────┐
│ ヘッダー          │
├──────────────────┤
│                  │  ←──  {% block content %}
│  ここが穴         │            <h1>ホーム</h1>
│                  │        {% endblock %}
├──────────────────┤
│ フッター          │
└──────────────────┘
```

- 型紙側:`{% block content %}{% endblock %}` と書いた場所が**穴**になる
- ページ側:1行目に `{% extends "base.html" %}` と書き、
  `{% block content %} ～ {% endblock %}` に中身を書くと**その穴に入る**
- 名前(`content`)が両者で一致していることが条件

穴は3つ用意してあります。

| 穴の名前 | 用途 |
| --- | --- |
| `content` | ページの本体(必須) |
| `head_extra` | そのページだけで使うCSSを足したいとき |
| `scripts` | そのページだけで使うJSを足したいとき |

**ヘッダーを直したいときは `base.html` を1枚直すだけ**で、全ページに反映されます。

> ★つまずきやすい点が3つあります。詳しくは `templates/base.html` の
> 冒頭のコメントに書いてあるので、最初に一度読んでください。
>
> 1. `{% extends %}` は**必ず1行目**(上にコメントも書けない)
> 2. `{% block content %}` の**外に書いたものは表示されない**
> 3. `{{ title }}` は、`views.py` から渡していなければ**空になるだけ**(エラーは出ない)

---

## よく使うコマンド

| やりたいこと | コマンド |
| --- | --- |
| 起動する | `docker compose up` |
| 裏で起動する | `docker compose up -d` |
| 止める | `docker compose down` |
| エラーを見る | `docker compose logs -f web` |
| モデルの変更を反映 | `docker compose exec web python manage.py makemigrations` → `migrate` |
| 管理者を作る | `docker compose exec web python manage.py createsuperuser` |
| 新しいアプリを作る | `docker compose exec web python manage.py startapp <名前>` |
| 箱の中に入る | `docker compose exec web bash` |
| 書き方をチェック | `docker compose exec web ruff check .` |

---

## 3つのテンプレートの対応表

同じ構成・同じ画面で作ってあるので、1つ分かれば他も読めます。

| やること | Flask版 | Gin版 | Django版 |
| --- | --- | --- | --- |
| 起動の入口 | `src/web/app.py` | `cmd/server/main.go` | `manage.py` + `config/` |
| 設定 | `config.py` | `internal/config/` | `config/settings.py` |
| データの形 | `models.py` | `internal/models/` | `main/models.py` |
| 画面を返す | `routes.py` | `handlers/page.go` | `main/views.py` |
| ログイン | `auth/routes.py` | `handlers/auth.go` | `accounts/views.py` |
| 型紙 | `base.html`(Jinja) | `base.html`(Go) | `base.html`(Django) |
| 表を作る | `flask init-db` | 起動時に自動 | 起動時に自動 |
| 表の形を変える | 作り直し(データ消滅) | 作り直し(データ消滅) | **データを保ったまま変更可** |
| 管理画面 | 無い | 無い | **`/admin/`** |
| アプリのポート | 5000 | 8080 | 8000 |
| DBのポート | 3307 | 3308 | 3309 |

> ポートをずらしてあるので、**3つ同時に起動しても衝突しません。**

---

## ドキュメント

- **[docs/SETUP.md](docs/SETUP.md)** — 環境構築、日々の操作、DBeaverでの接続、困ったときの対処
- **[docs/Pyhelp.md](docs/Pyhelp.md)** — Pythonの書き方(Java・PHPをやった人向けの早わかり)
- **[docs/DEPLOY.md](docs/DEPLOY.md)** — 本番に出す手順(AWS・HTTPS・困ったときの対処)
