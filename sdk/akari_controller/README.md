Akariをdynamixelで動かすためのパッケージ

## インストール

```
sudo python setup.py install
```

## 機能

### `class AkariController`

akari専用のコントローラ。

pan関節とtilt関節が存在し、初期化時に可動範囲制限が設定される。

関節角度や速度の指定、および関節角度の取得などが可能。

### `class DynamixelController`

dynamixelのコントローラ。

基本的なパケット通信を行う。
