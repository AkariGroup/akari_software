from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TypedDict

from .color import Color
from .position import Positions


class M5ComDict(TypedDict):
    """
    M5から取得する情報を格納するDict。
    """
    din0: bool
    din1: bool
    ain0: int
    dout0: bool
    dout1: bool
    pwmout0: int
    general0: float
    general1: float
    button_a: bool
    button_b: bool
    button_c: bool
    temperature: float
    pressure: float
    brightness: int
    time: float
    is_response: bool


class M5StackClient(ABC):
    @abstractmethod
    def set_dout(self, pin_id: int, value: bool, sync: bool = True) -> None:
        """ヘッド部GPIOピンのデジタル出力を設定する。

        Args:
            pin_id: pin番号。0でdout0、1でdout1を指定する。
            value: デジタル出力の値。``False``で0V,``True``で3.3V出力。
            sync: 同期実行の指定。``True``の場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.color import Colors, Color
        >>> with AkariClient() as akari:
        >>>     m5 = akari.m5stack
        >>>     m5.set_dout(0, True)
        # dout0がTrueになる。

        """
        ...

    @abstractmethod
    def set_pwmout(self, pin_id: int, value: int, sync: bool = True) -> None:
        """ヘッド部GPIOピンのPWM出力を設定する。

        Args:
            pin_id: pin番号。デフォルトではpwmout0しかないため、0を指定すること。
            value: PWM出力の値。 0-255で指定し、0で0V、255で3.3Vを出力する。
            sync: 同期実行の指定。``True``の場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.color import Colors, Color
        >>> with AkariClient() as akari:
        >>>     m5 = akari.m5stack
        >>>     m5.set_pwmout(0, 200)
        # pwmout0が200になる。

        """
        ...

    @abstractmethod
    def set_allout(
        self,
        *,
        dout0: bool,
        dout1: bool,
        pwmout0: int,
        sync: bool = True,
    ) -> None:
        """ヘッド部GPIOピンの出力をまとめて設定する。

        Args:
            dout0: dout0の出力値。``False``で0V,``True``で3.3V出力。
            dout1: dout1の出力値。``False``で0V,``True``で3.3V出力。
            pwmout0: pwmout0の出力値。0-255で指定し、0で0V、255で3.3Vを出力する。
            sync: 同期実行の指定。``True``の場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.color import Colors, Color
        >>> with AkariClient() as akari:
        >>>     m5 = akari.m5stack
        >>>     m5.set_allout(dout0=False, dout1=True, pwmout0=100)
        # dout0がFalse, dout1がTrue, pwmout0が100になる。

        """
        ...

    @abstractmethod
    def reset_allout(self, sync: bool = True) -> None:
        """ヘッド部GPIOピンの出力を初期値にリセットする。
        dout0、dout1はFalse、pwmout0は0となる。

        Args:
            sync: 同期実行の指定。``True``の場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.color import Colors, Color
        >>> with AkariClient() as akari:
        >>>     m5 = akari.m5stack
        >>>     m5.reset_allout()
        # dout0がFalse, dout1がFalse, pwmout0が0になる。

        """
        ...

    @abstractmethod
    def set_display_color(
        self,
        color: Color,
        sync: bool = True,
    ) -> None:
        """ボディー部M5のディスプレイ背景色を変更する。

        Args:
            color: 背景色を指定。色は``color.Colors``から色名を引用する、もしくはRGBの数値指定も可能。
            sync: 同期実行の指定。``True``の場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.color import Colors, Color
        >>> with AkariClient() as akari:
        >>>     m5 = akari.m5stack
        >>>     color = Colors.WHITE
        >>>     m5.set_display_color(color)
        # 画面色が白になる。
        >>>     color = Color(red=0, green=100, blue=200)
        >>>     m5.set_display_color(color)
        # 画面色が指定したRGB値になる。

        """
        ...

    @abstractmethod
    def set_display_text(
        self,
        text: str,
        pos_x: int = Positions.CENTER,
        pos_y: int = Positions.CENTER,
        size: int = 3,
        text_color: Optional[Color] = None,
        back_color: Optional[Color] = None,
        refresh: bool = True,
        sync: bool = True,
    ) -> None:
        """ボディー部M5のディスプレイに文字を表示する。

        Args:
            text: 表示する文字列。文字列の最後に空白を挿入したい場合は空白の後ろに"\n"をつけること。
            pos_x: x方向の描画位置ピクセルを0-320で指定。左端が0。``position.Positions``を用いた位置指定も可能。デフォルト値は中央揃え。
            pos_y: y方向の描画位置ピクセルを0-240で指定。上端が0。``position.Positions``を用いた位置指定も可能。デフォルト値は中央揃え。
            size: 文字サイズを1-7の7段階で指定。デフォルト値は3。
            text_color: 文字色を指定。色は``color.Colors``から色名を引用する、もしくはRGBの数値指定も可能。値を指定しない場合、前回値を引き継ぐ。
            back_color: 背景色を指定。色は``color.Colors``から色名を引用する、もしくはRGBの数値指定も可能。値を指定しない場合、画面全体の背景色に合わせる。
            refresh: trueの場合画面全体をback_colorで更新する。falseの場合は現在の表示を維持しつつ、文字を描画する範囲のみ更新する。デフォルト値は背景更新あり。
            sync: 同期実行の指定。Trueの場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.color import Colors
        >>> from akari_client.position import Positions
        >>> with AkariClient() as akari:
        >>>    _text = "AKARI"
        >>>    _pos_x = Positions.LEFT
        >>>    _pos_y = Positions.TOP
        >>>    _size = 4
        >>>    _text_color = Colors.WHITE
        >>>    _back_color = Colors.BLACK
        >>>    _refresh = True
        >>>    m5.set_display_text(
        ...        _text, _pos_x, _pos_y, _size, _text_color, _back_color, _refresh
        ...    )
        # 画面に「AKARI」と表示される。

        """
        ...

    @abstractmethod
    def set_display_image(
        self,
        filepath: str,
        pos_x: int = Positions.CENTER,
        pos_y: int = Positions.CENTER,
        scale: float = -1.0,
        sync: bool = True,
    ) -> None:
        """ボディー部M5のディスプレイにM5のSDカード内の画像を表示する。

        Args:
            filepath: M5のSDカード内のファイルパス。(例;"image/hoge.jpg")
            pos_x: x方向の描画位置ピクセルを0-320で指定。左端が0。``position.Positions``を用いた位置指定も可能。デフォルト値は中央揃え。
            pos_y: y方向の描画位置ピクセルを0-240で指定。上端が0。``position.Positions``を用いた位置指定も可能。デフォルト値は中央揃え。
            scale: 画像の拡大縮小倍率を指定。1.0で等倍表示。マイナスの値を入れた場合、画面サイズに合わせて自動でサイズ調整される。
                   デフォルト値は自動サイズ調整となっている。
            sync: 同期実行の指定。Trueの場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.position import Positions
        >>> with AkariClient() as akari:
        >>>    _filepath = "/logo320.jpg"
        >>>    _pos_x = Positions.LEFT
        >>>    _pos_y = Positions.TOP
        >>>    _scale = 0.75
        >>>    m5.set_display_image(_filepath, _pos_x, _pos_y, _scale)
        # 画面に"/logo320.jpg"の画像が表示される。

        """
        ...

    @abstractmethod
    def play_mp3(
        self,
        filepath: str,
        sync: bool = True,
    ) -> None:
        """M5のSDカード内のmp3ファイルを再生する。

        .. note::
            M5Stackのハード特性上、再生時にスピーカーにホワイトノイズが乗る。
            またmp3再生を行いながら、ディスプレイ等の表示を行うと音声にノイズが乗るので注意。
            音声再生を本格的に行いたい場合は、スピーカーをメインPCのイヤホンジャックやUSBに接続して、
            メインPCから直接再生することを推奨。

        Args:
            filepath: M5のSDカード内のファイルパス。(例;"mp3/hoge.mp3")
            sync: 同期実行の指定。Trueの場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.position import Positions
        >>> with AkariClient() as akari:
        >>>    _filepath = "/mp3/hello.mp3"
        >>>    m5.play_mp3(filepath)
        # "/mp3/hello.mp3"が再生される。

        """
        ...

    @abstractmethod
    def stop_mp3(
        self,
        sync: bool = True,
    ) -> None:
        """mp3ファイルの再生を停止する。

        Args:
            sync: 同期実行の指定。``True``の場合M5側で実行完了するまで関数の終了待ちを行う。

        example:
        >>> from akari_client.position import Positions
        >>> with AkariClient() as akari:
        >>>    _filepath = "/mp3/hello.mp3"
        >>>    m5.play_mp3(filepath)
        >>>    time.sleep(1)
        >>>    m5.stop_mp3()
        # 1秒後に再生停止する。

        """
        ...

    @abstractmethod
    def reset_m5(self) -> None:
        """M5をリセットして再起動する。

        example:
        >>> from akari_client.position import Positions
        >>> with AkariClient() as akari:
        >>>    m5.reset_m5()
        # M5が再起動する。

        """
        ...

    @abstractmethod
    def get(self) -> M5ComDict:
        """M5から環境センサ、ヘッドGPIOの入力値、M5のボタンの状態を取得する。

        example:
        >>> from akari_client.position import Positions
        >>> with AkariClient() as akari:
        >>>    data = m5.get()
        >>>    print(data["temperature"])
        31.675

        """
        ...
