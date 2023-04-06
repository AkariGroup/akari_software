# AKARI構成管理ツール

AKARIに初期インストールするためのソフトウェア環境を管理・構築するためのツールです。


## 前準備

1. Python 3.8+ および venv がインストールされていることを確認
   ```sh
   $ python --version
   Python 3.8.11
   ```
  - インストールされていない場合には以下のコマンドで Python をインストールしてください
   ```sh
   $ sudo apt install python3.8 python3.8-venv
   ```

1. sshpassをインストール
   ```sh
   $ sudo apt install sshpass
   ```

## 実行方法

### AKARIのローカル環境で実行する場合

1. `hosts.example` を `hosts` という名前で同一ディレクトリ内にコピー
   ```sh
   $ cp hosts.example hosts
   ```

2. 構成を適用
   ```sh
   $ ./run-ansible.py -i hosts ./system.yml -K --diff -c local
   (初回実行時だけ時間がかかります)
   BECOME password: <Akariユーザーのパスワードを入力する>
   ```
### AKARI外のPCからリモート実行する場合

1. セットアップに使うPC側にakari_softwareをcloneし、AKARIとPCを同一ネットワークに接続する。

2. `hosts.example` を `hosts` という名前で同一ディレクトリ内にコピー
   ```sh
   $ cp hosts.example hosts
   ```

3. `hosts` の `[mainpc]` 以下の127.0.0.1を削除し、 AKARIの IPアドレスに書き換える

4. 構成を適用
   ```sh
   $ ./run-ansible.py -i hosts ./system.yml --ask-vault-pass -Kk --diff
   (初回実行時だけ時間がかかります)
   BECOME password: <Akariユーザーのパスワードを入力する>
   Vault password: <シークレットファイル復号化用のパスワードを入力する>
   ```


**NOTE**: 実際に構成を適用せずに変更内容だけを確認するには `--check` オプションを指定してください

**NOTE**: PythonのModuleエラーや "ansible-playbook" が見つからないといったエラーが発生する場合には `--clean` オプションを指定してください

### AKARI本体の再起動

`run-ansible` コマンドを実行した後は、かならずAKARI本体を再起動してください。
