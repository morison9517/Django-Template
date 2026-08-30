# 本番に出す手順

このファイルは**サーバーにアプリを載せるとき**に見る紙です。
日々の開発は [SETUP.md](SETUP.md) を見てください。

> ★**本番前に一度、必ず練習してください。**
> ここに書いてある手順を、本番当日に初めて打つのは危険です。
> 9月中に1回通しておけば、当日は同じことを繰り返すだけになります。

---

## 開発と本番の違い(先に頭に入れておくこと)

| | 開発 | 本番 |
| --- | --- | --- |
| 使うファイル | `compose.yml` | **`compose.prod.yml`** |
| サーバー | runserver(1人ずつ捌く) | **gunicorn(3人同時)** |
| コードの反映 | 保存したら即 | **build し直したとき** |
| CSS・画像を配る人 | Django | **Nginx** |
| DBのポート | PCから見える(3309) | **開けない** |
| エラー画面 | 詳しく出る | **出ない(内部情報が漏れるため)** |

**「保存しても本番に反映されない」のは正しい動きです。** 本番は箱に焼き込んだコードで動きます。

---

## 1. 準備(初回だけ)

### ① サーバーに Docker を入れる

AWSのサーバーに入って、Docker と Docker Compose が使える状態にします。

```bash
docker version
docker compose version
```

### ② コードを置く

```bash
git clone <リポジトリのURL>
cd case_django
```

### ③ 金庫(`.env`)を作る

```bash
cp .env.example .env
```

**そして必ず中身を書き換えます。** 見本のままだと危険です。

| 項目 | 本番で入れる値 |
| --- | --- |
| `DJANGO_SECRET_KEY` | **長いランダムな文字列**(下のコマンドで作る) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | 使うドメイン(例:`app.example.com`) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://app.example.com` |
| `DB_PASSWORD` / `DB_ROOT_PASSWORD` | **開発用と違うパスワード** |

割り印(SECRET_KEY)はこれで作れます。

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

> ★`DJANGO_DEBUG=True` のまま本番に出すと、エラーが起きたときに
> **設定ファイルの中身やDBのパスワードが画面に出ます。** 必ず `False` にしてください。

---

## 2. 起動する

```bash
docker compose -f compose.prod.yml up -d --build
```

**`-f compose.prod.yml` を毎回付けます。** 忘れると開発用が起動します。

初回は数分かかります。終わったら状態を見ます。

```bash
docker compose -f compose.prod.yml ps
```

`db` `web` `nginx` の3つが `running` なら成功です。

### 管理者アカウントを作る(初回だけ)

```bash
docker compose -f compose.prod.yml exec web python manage.py createsuperuser
```

### 開いて確認

ブラウザで `http://<サーバーのアドレス>/auth/login` を開きます。

> ★`/`(トップページ)は、まだ自分たちで作っていないうちは **404 になります。**
> 開発中は `/` にデモページが出ますが、**本番ではデモを登録しないため**です。
> 「デモが本番に出ない」ことの裏返しなので、故障ではありません。
> `main/urls.py` に `path("", ...)` を書けば解消します。
>
> ★同じ理由で、**新規登録とログインは成功しても飛び先が404に見えます。**
> 成功したかどうかは、404の画面ではなくログで判断してください
> (302 が返っていれば成功しています)。

---

## 3. コードを直したとき

```bash
git pull
docker compose -f compose.prod.yml up -d --build
```

**この2行だけです。** `migrate` と `collectstatic` は起動時に自動で走ります。

> DBの表の変更(マイグレーション)も自動で当たります。
> ただし**マイグレーションのファイルをコミットし忘れていると当たりません。**
> `main/migrations/` の中身は必ずpushしてください。

---

## 4. HTTPSにする

練習の段階では `http://` のままで構いません。**本番では必ずHTTPSにします。**

やり方は2つあります。**AWSを使うなら1番が圧倒的に楽です。**

### ① AWSのロードバランサーに任せる(おすすめ)

証明書をAWS側(ACM)で取って、ロードバランサーに付けます。
アプリ側は何も変えなくて構いません。HTTPSはAWSが終わらせて、
サーバーにはHTTPで届きます。`prod.conf` の `X-Forwarded-Proto` が
「元はHTTPSだった」と Django に伝えるので、それで正しく動きます。

**証明書の期限切れもAWSが自動で更新してくれます。**

### ② サーバーの中で証明書を取る(Let's Encrypt)

Nginxの箱に証明書を読ませて、443番を開けます。
無料ですが、**90日ごとの更新を自分で回す必要があります。**
ハッカソン当日までなら期限内なので問題ありませんが、
設定の手間は1番より明らかに多いです。

### ★HTTPSにしたら必ず戻すこと

`.env` の1行です。

```
DJANGO_SECURE_COOKIES=True
```

練習中に `False` にしていた場合、**戻し忘れるとログイン状態が
HTTPSでない経路でも持ち歩けてしまいます。**

---

## 5. よく使うコマンド

| やりたいこと | コマンド |
| --- | --- |
| 起動 | `docker compose -f compose.prod.yml up -d --build` |
| 停止 | `docker compose -f compose.prod.yml down` |
| 状態を見る | `docker compose -f compose.prod.yml ps` |
| ログを見る | `docker compose -f compose.prod.yml logs -f web` |
| Nginxのログ | `docker compose -f compose.prod.yml logs -f nginx` |
| 箱の中に入る | `docker compose -f compose.prod.yml exec web bash` |
| 設定の総点検 | `docker compose -f compose.prod.yml exec web python manage.py check --deploy` |

> ★`down -v` は**絶対に打たないでください。**
> `-v` はDBと画像の保管庫ごと消す指定です。利用者のデータが全部消えます。

---

## 6. 本番のDBをDBeaverで見たいとき

本番では**DBのポートを開けていません。** 開けると世界中からログインを試されます。

代わりに、SSHのトンネルを通して見ます。DBeaverの接続設定で
「SSH」タブを開き、サーバーへのSSH情報を入れてください。
そのうえで、ホストは `127.0.0.1`、ポートは `3306` にします。

> トンネル = 自分のPCとサーバーの間に専用の通路を1本引くイメージです。
> 通路の中を通るので、外からは見えません。

---

## 7. 困ったとき

### 画面が真っ白 / デザインが崩れている

CSSが配れていません。まず `collectstatic` が動いたか見ます。

```bash
docker compose -f compose.prod.yml logs web | grep -i static
```

`static files copied` と出ていれば集められています。
出ていなければ、web の箱が起動途中で止まっている可能性があります。

### ログインできない(ログイン画面に戻される)

**`DJANGO_SECURE_COOKIES` が原因です。**

`http://` でアクセスしているのに `True` になっていると、
ログイン自体は成功しているのにログイン状態が保存されません。
エラーも出ないので、まずここを疑ってください。

練習中は `.env` に `DJANGO_SECURE_COOKIES=False` を入れてください。

### ログインボタンを押すと 403(CSRF verification failed)

`.env` の `DJANGO_CSRF_TRUSTED_ORIGINS` に、使っているURLを
`https://` から書いてください。書き忘れが原因のほぼ全部です。

```
DJANGO_CSRF_TRUSTED_ORIGINS=https://app.example.com
```

### 「DisallowedHost」と出る

`.env` の `DJANGO_ALLOWED_HOSTS` にドメインを足してください。

```
DJANGO_ALLOWED_HOSTS=app.example.com
```

### 502 Bad Gateway と出る

Nginxは動いているが、Django が返事をしていません。
web のログを見てください。だいたい起動時のエラーです。

```bash
docker compose -f compose.prod.yml logs web
```

### プロフィールアイコンが表示されない

`media` の保管庫がNginxから見えていない可能性があります。
`compose.prod.yml` の nginx に `media_files:/var/www/media:ro` があるか確認してください。

**なお、開発用と本番用で画像の保管庫は別です。** 開発中に入れた画像は本番にはありません。

### 起動しない / 起動してすぐ落ちる

`volumes:` に `- .:/app` を書いていないか確認してください。
**本番でこれを書くと、箱に焼き込んだものが隠れて起動しません。**
本番でいちばん多い事故です。

---

## 8. 本番に出す前のチェックリスト

デプロイの練習のときに、この順で確認してください。

- [ ] `.env` の `DJANGO_DEBUG` が `False`
- [ ] `.env` の `DJANGO_SECRET_KEY` を見本から変えた
- [ ] `.env` の `DB_PASSWORD` を開発用から変えた
- [ ] `DJANGO_ALLOWED_HOSTS` に本番のドメインを書いた
- [ ] `DJANGO_CSRF_TRUSTED_ORIGINS` に `https://` から書いた
- [ ] `check --deploy` を打って、致命的な警告が無い
- [ ] `/auth/login` が開ける
- [ ] **CSSが当たっている**(見た目が崩れていない)
- [ ] **新規登録 → ログイン → ログアウトが通る**
- [ ] 管理画面(`/admin/`)に入れる
- [ ] `docker compose -f compose.prod.yml restart` して、データが残っている

**最後の1つが特に大事です。** 再起動でデータが消えるなら、保管庫の設定が間違っています。
