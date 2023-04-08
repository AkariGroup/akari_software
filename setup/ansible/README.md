# AKARI構成管理ツール

AKARIの動作に必要なソフトウェアをインストールするためのツールです。


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


## 実行方法

### AKARIのローカル環境で実行する場合

1. Ansibleを実行する
   ```sh
   $ ./run-ansible.py -i hosts ./system.yml -K --diff -c local
   (初回実行時だけ時間がかかります)
   BECOME password: <Akariユーザーのパスワードを入力する>
   ```
### AKARI外のPCからリモート実行する場合

1. セットアップに使うPC側にakari_softwareをcloneし、AKARIとPCを同一ネットワークに接続する。

2. sshpassをインストール
   ```sh
   $ sudo apt install sshpass
   ```

3. `hosts` ファイルを開き、 `[mainpc]` 以下にある `127.0.0.1` をAKARIのIPアドレスに書き換える

4. Ansibleを実行する
   ```sh
   $ ./run-ansible.py -i hosts ./system.yml -Kk --diff
   (初回実行時だけ時間がかかります)
   BECOME password: <Akariユーザーのパスワードを入力する>
   ssh password: <Akariユーザーのパスワードを入力する>
   ```


**NOTE**: 実際に構成を適用せずに変更内容だけを確認するには `--check` オプションを指定してください

**NOTE**: PythonのModuleエラーや "ansible-playbook" が見つからないといったエラーが発生する場合には `--clean` オプションを指定してください

### AKARI本体の再起動

`run-ansible` コマンドを実行した後は、かならずAKARI本体を再起動してください。
