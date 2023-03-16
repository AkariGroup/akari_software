# akari\_client

[AKARI](https://github.com/AkariGroup/) を使うためのクライアントライブラリ

## インストール

```sh
pip install akari_client
```

**注意:** `akari_client` を使う前に `AKARI` 本体の設定が完了している必要があります。
詳しくはオンラインドキュメントを参照してください。

## Getting Started: ディスプレイに文字を表示する

```py
with AkariClient() as akari:
    m5 = akari.m5stack
    m5.set_display_text("Hello, world!")
```

その他のサンプルや使い方はオンラインドキュメントを参照してください。

## ドキュメント

[https://AkariGroup.github.io/docs](https://AkariGroup.github.io/docs)

