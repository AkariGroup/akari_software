# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

TITLECOLOR=36 #Cyan:各ステップのタイトル用
COMMENTCOLOR=35 #Magenta:各ステップのタイトル用
SKIPCOLOR=33 #yellow:重複ステップのスキップメッセージ用
SUCCESSCOLOR=32 #Green:各ステップの実行、成功
FAILCOLOR=31 #Red:実行の失敗

## エラーメッセージを表示して終了
abort () {
  echo $1 2>&1
  exit 1
}

## 各ステップのタイトルを強調表示する際に使用
titleEcho () {
echo -e ""
echo -e "\e[$TITLECOLOR;1m----------------------------------------\e[m"
echo -e "\e[$TITLECOLOR;1m$1\e[m"
echo -e "\e[$TITLECOLOR;1m----------------------------------------\e[m"
#echo -e ""
}

## 各ステップ内のコメントを強調表示する際に使用
commentEcho () {
echo -e "\e[$COMMENTCOLOR;1m $1\e[m"
}

## 各ステップ内のスキップコメントを強調表示する際に使用
skipEcho () {
echo -e "\e[$SKIPCOLOR;1m [SKIP!] $1\e[m"
}

## 各ステップ内の成功コメントを強調表示する際に使用
successEcho () {
echo -e "\e[$SUCCESSCOLOR;1m [SUCCESS!] $1\e[m"
}

## スクリプトの終了コメントを強調表示する際に使用
finishEcho () {
echo -e " "
echo -e "\e[$SUCCESSCOLOR;1m----------------------------------------\e[m"
echo -e "\e[$SUCCESSCOLOR;1mAll steps were finished!!\e[m"
echo -e "\e[$SUCCESSCOLOR;1m----------------------------------------\e[m"
echo -e " "
}

# エラーで停止した際にメッセージを出力
errorHandler() {
echo -e " "
echo -e "\e[$FAILCOLOR;1m----------------------------------------\e[m"
echo -e "\e[$FAILCOLOR;1m Set up failed! Check the previous step! \e[m"
echo -e "\e[$FAILCOLOR;1m----------------------------------------\e[m"
echo -e " "
  # スクリプトを終了する
  exit 1
}

## 引数で指定されたコマンドを表示して実行するシェル関数
## （ここで「$PS4」には「+」が入っているのでそれを使う）
+ () {   # 関数名が「+」であるような関数を定義（bash only）
  if [[ $# -eq 1 ]]; then      # 引数が1個のとき
    echo $PS4 "$1"; eval "$1"
  else                         # 引数が2個以上のとき
    echo $PS4 $@  ; eval $@
  fi
}

## 引数を色つきで表示する（注：bashでのみ動作）
:: () {
  echo -e "\033[33m::" $@ "\033[m"   # yellow
}

## 指定時間以内に apt-get update を実行していれば終了ステータスが 0
apt_updated_recently () {
  ## ディレクトリが指定時間内に更新されていれば正常終了
  local minute=${1:-$APT_UPDATED_MINUTES}  # 第1引数は分（デフォルト60分）
  local dir="/var/lib/apt/lists/partial"
  local out=`find $dir -maxdepth 0 -mmin "-$minute"`
  [[ -n "$out" ]] && return 0  # 正常終了
  return 1                     # エラー終了
}

APT_UPDATED_MINUTES=30    # デフォルト30分

## 指定したパッケージがすべてインストール済みなら正常終了、
## インストールされてないパッケージが1つでもあればエラー終了
## （もしすべてインストール済みなら apt-get install をスキップできる）
apt_installed () {
  local pkg
  for pkg in $@; do
    dpkg -l | grep -e "^ii  $pkg " -e "^ii  $pkg:"  > /dev/null || return 1   # エラー終了
  done
  return 0  # 正常終了
}

## 指定時間以内に apt update を実行していなければapt updateを実行
apt_check_and_update () {
  if apt_updated_recently; then
   skipEcho "Update has done recently."
  else
   sudo apt update 
   successEcho "Update has been finished."
  fi
}

## 指定時間以内に apt update を実行していなければapt updateとupgradeを実行
apt_check_and_upgrade () {
  apt_check_and_update
  sudo apt upgrade
  successEcho "Upgrade has been finished."
}

## 指定したパッケージがインストールされていなければインストール
apt_check_and_install () {
  local pkg
  for pkg in $@; do
    if apt_installed $pkg; then
     skipEcho "$pkg has been available."
    else
     sudo apt-get install -qq -y $pkg
     successEcho "$pkg was installed."
    fi
  done
  return 0
}

## 指定したパッケージがデフォルトのpythonバージョンにすべてインストール済みなら正常終了、
## インストールされてないパッケージが1つでもあればエラー終了
## （もしすべてインストール済みなら apt-get install をスキップできる）
pip_installed () {
  local pkg
  for pkg in $@; do
    pip list | grep "$pkg "  > /dev/null || return 1   # エラー終了
  done
  return 0  # 正常終了
}

## 指定したパッケージがpython2にすべてインストール済みなら正常終了、
## インストールされてないパッケージが1つでもあればエラー終了
## （もしすべてインストール済みなら apt-get install をスキップできる）
pip2_installed () {
  local pkg
  for pkg in $@; do
    pip2 list | grep "$pkg "  > /dev/null || return 1   # エラー終了
  done
  return 0  # 正常終了
}

## 指定したパッケージがpython3にすべてインストール済みなら正常終了、
## インストールされてないパッケージが1つでもあればエラー終了
## （もしすべてインストール済みなら apt-get install をスキップできる）
pip3_installed () {
  local pkg
  for pkg in $@; do
    pip3 list | grep "$pkg "  > /dev/null || return 1   # エラー終了
  done
  return 0  # 正常終了
}

## 指定したパッケージがインストールされていなければインストールする
## python2とpython3両方に対して実行
pip_check_and_install () {
  local pkg
  for pkg in $@; do
    if pip3_installed $pkg; then
     skipEcho "$pkg has been available in python3."
    else
     pip3 install $pkg --user
     successEcho "$pkg was installed in python3."
    fi    
  done
  return 0
}

## 指定したパッケージがインストールされていなければインストールする
## python3に対して実行
pip3_check_and_install () {
  local pkg
  for pkg in $@; do
    if pip3_installed $pkg; then
     skipEcho "$pkg has been available in python3."
    else
     pip3 install $pkg --user
     successEcho "$pkg was installed in python3."
    fi    
  done
  return 0
}

## 再起動を表す終了ステータス
REBOOT_EXIT=246
