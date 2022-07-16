"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class SetPinOutRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class BinaryPinsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: builtins.bool
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: builtins.bool = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    class IntPinsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: builtins.int
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: builtins.int = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    BINARY_PINS_FIELD_NUMBER: builtins.int
    INT_PINS_FIELD_NUMBER: builtins.int
    SYNC_FIELD_NUMBER: builtins.int
    @property
    def binary_pins(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, builtins.bool]: ...
    @property
    def int_pins(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, builtins.int]: ...
    sync: builtins.bool
    def __init__(self,
        *,
        binary_pins: typing.Optional[typing.Mapping[typing.Text, builtins.bool]] = ...,
        int_pins: typing.Optional[typing.Mapping[typing.Text, builtins.int]] = ...,
        sync: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["binary_pins",b"binary_pins","int_pins",b"int_pins","sync",b"sync"]) -> None: ...
global___SetPinOutRequest = SetPinOutRequest

class SetDisplayColorRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    COLOR_FIELD_NUMBER: builtins.int
    SYNC_FIELD_NUMBER: builtins.int
    @property
    def color(self) -> global___Color: ...
    sync: builtins.bool
    def __init__(self,
        *,
        color: typing.Optional[global___Color] = ...,
        sync: builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["color",b"color"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["color",b"color","sync",b"sync"]) -> None: ...
global___SetDisplayColorRequest = SetDisplayColorRequest

class SetDisplayTextRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TEXT_FIELD_NUMBER: builtins.int
    POS_X_FIELD_NUMBER: builtins.int
    POS_Y_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    TEXT_COLOR_FIELD_NUMBER: builtins.int
    BG_COLOR_FIELD_NUMBER: builtins.int
    REFRESH_FIELD_NUMBER: builtins.int
    SYNC_FIELD_NUMBER: builtins.int
    text: typing.Text
    pos_x: builtins.int
    pos_y: builtins.int
    size: builtins.int
    @property
    def text_color(self) -> global___Color: ...
    @property
    def bg_color(self) -> global___Color: ...
    refresh: builtins.bool
    sync: builtins.bool
    def __init__(self,
        *,
        text: typing.Text = ...,
        pos_x: builtins.int = ...,
        pos_y: builtins.int = ...,
        size: builtins.int = ...,
        text_color: typing.Optional[global___Color] = ...,
        bg_color: typing.Optional[global___Color] = ...,
        refresh: builtins.bool = ...,
        sync: builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bg_color",b"bg_color","text_color",b"text_color"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bg_color",b"bg_color","pos_x",b"pos_x","pos_y",b"pos_y","refresh",b"refresh","size",b"size","sync",b"sync","text",b"text","text_color",b"text_color"]) -> None: ...
global___SetDisplayTextRequest = SetDisplayTextRequest

class SetDisplayImageRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PATH_FIELD_NUMBER: builtins.int
    POS_X_FIELD_NUMBER: builtins.int
    POS_Y_FIELD_NUMBER: builtins.int
    SCALE_FIELD_NUMBER: builtins.int
    SYNC_FIELD_NUMBER: builtins.int
    path: typing.Text
    pos_x: builtins.int
    pos_y: builtins.int
    scale: builtins.int
    sync: builtins.bool
    def __init__(self,
        *,
        path: typing.Text = ...,
        pos_x: builtins.int = ...,
        pos_y: builtins.int = ...,
        scale: builtins.int = ...,
        sync: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["path",b"path","pos_x",b"pos_x","pos_y",b"pos_y","scale",b"scale","sync",b"sync"]) -> None: ...
global___SetDisplayImageRequest = SetDisplayImageRequest

class UseJapaneseFontRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ENABLED_FIELD_NUMBER: builtins.int
    SYNC_FIELD_NUMBER: builtins.int
    enabled: builtins.bool
    sync: builtins.bool
    def __init__(self,
        *,
        enabled: builtins.bool = ...,
        sync: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["enabled",b"enabled","sync",b"sync"]) -> None: ...
global___UseJapaneseFontRequest = UseJapaneseFontRequest

class Color(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RED_FIELD_NUMBER: builtins.int
    GREEN_FIELD_NUMBER: builtins.int
    BLUE_FIELD_NUMBER: builtins.int
    red: builtins.float
    green: builtins.float
    blue: builtins.float
    def __init__(self,
        *,
        red: builtins.float = ...,
        green: builtins.float = ...,
        blue: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["blue",b"blue","green",b"green","red",b"red"]) -> None: ...
global___Color = Color

class M5Status(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STATUS_JSON_FIELD_NUMBER: builtins.int
    status_json: typing.Text
    def __init__(self,
        *,
        status_json: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["status_json",b"status_json"]) -> None: ...
global___M5Status = M5Status
