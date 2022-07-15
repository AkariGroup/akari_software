# akari_mainのsetupディレクトリ

## ディレクトリ構成
- Arduino  
Arduino関連の設定ファイルとM5のsourceファイル。  
- lattepanda_BIOS  
lattepandaの自動起動用BIOSファイル。  
- m5_sd  
M5stack用のSDカード内のファイル。フォント、画像など。  
- script  
lattepandaのUbuntuセットアップ用スクリプトファイル。  

## AKARIのセットアップ手順

### lattepandaのセットアップ
1. Ubuntu 20.04をlattepanda alphaにインストール。  
escキーを起動画面で押すとBIOSに入れるので、ubuntuインストールメディアをboot deviceとして選択してインストール  
2. akariのgitレポジトリをホーム直下にcloneする。  
`cd ~/`  
`sudo apt-get -y install git`  
(HTTP) `git clone https://github.com/AkariGroup/akari_main.git`  
(SSH) `git clone git@github.com:AkariGroup/akari_main.git`  
3. セットアップスクリプトの実行  
各セットアップスクリプトを順番通り実行することでmainPCのセットアップが完了する。  
`cd ~/akari_main/setup/script`  
`chmod +x *`  
- 必要なライブラリのインストール  
`./1_mainpc_setup_libraries.sh`  
- OAK-Dの設定、ArduinoのIDEインストール、dynamixel、M5stack用の設定  
`./2_mainpc_setup_peripherals.sh`  
- 自動起動サービスの追加  
`./3_mainpc_setup_autostart.sh`  
- (任意)推奨ツールのセットアップ  
`./tool_setup.sh`  

その他のAppのセットアップは必要に応じて実施。詳細は各パッケージのREADME参照。  

### lattepanda alphaの自動起動BIOS書き込み
AKARIのCPUにlattepanda alphaを使用する場合、物理スイッチに合わせて起動させるために自動起動用のBIOSを書き込む必要がある。  
`akarimainpu/setup/lattepanda_BIOS`内の`readme.docx`に沿ってBIOSの書き換えを実行する。  
実行後はlattepanda alphaの12Vコネクタに電源を入力すると、自動で電源ONするようになる。  

### Dynamixel motorへのID書き込み
1. 下記リンク先からDynamixel wizardのLinux版をダウンロードし、インストール  
   https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/  
1. Dynamixel wizardを起動し、Scanで2XL430-W250が2軸分検出されることを確認する。  
1. ID1のモータを左ツリーから選択。  
1. 右上のモータ名表示の下にあるプルダウンから制御モードをPositionに設定  
1. 中央のアドレス一覧からAddress:116 Goal Positionを選択し、0°で初期位置、つまみでモータの角度制御ができるか確認。  
1. この際上下方向のモータが動く場合は、中央のアドレス一覧からAddress:7を選択し、IDを2に変更しsaveする。  
もう１個の軸がID2に割り振られている場合重複したIDが触れないため、一旦２つのモータをID3,4などの空きIDでsaveしたのち、改めてID1,2を設定する。  
パン(左右方向)がID1、チルト(上下方向)がID2になるように設定する。  
1. Baud Rate欄を選択し、1Mbpsを選択後、Saveボタンを押す。
1. もう一方のモータに関しても4.-6.の手順を繰り返す。

### M5のSDカードへのデータコピー
1. M5Stack用のmicroSDのroot直下に、`akari_main/setup/m5_sd`以下のファイルをコピーする。  

### M5のBaseソフトの書き込みと使用
1. Arduino IDEの起動  
`cd ~/arduino-1.8.13`  
`./arduino`  
2. "ファイル"->"開く"から~/akari_main/setup/Arduino/src/m5base_for_akari/m5base_for_akari.inoを選択  
3. "ツール"->"ボード"->"M5Stack-Core-ESP32"を選択  
 "ツール"->"シリアルポート"からM5Stackのポートを選択(ttyUSB0かttyUSB1のどちらかになる。)  
4. "マイコンボードに書き込む"で書き込み  

### AKARI開発仮想環境へのログイン
AKARIはpoetryを使った仮想環境を用いている。コード実行時などはpoetry環境下へ移動して実行する。
1. akari_main直下へ移動
` cd ~/akari_main`
2. 下記コマンドを実行して仮想環境下へ移動
`poetry shell`
