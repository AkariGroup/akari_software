"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class GetJointNameResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    JOINT_NAME_FIELD_NUMBER: builtins.int
    joint_name: typing.Text
    def __init__(self,
        *,
        joint_name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["joint_name",b"joint_name"]) -> None: ...
global___GetJointNameResponse = GetJointNameResponse

class GetServoEnabledResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ENABLED_FIELD_NUMBER: builtins.int
    enabled: builtins.bool
    def __init__(self,
        *,
        enabled: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["enabled",b"enabled"]) -> None: ...
global___GetServoEnabledResponse = GetServoEnabledResponse

class SetServoEnabledRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ENABLED_FIELD_NUMBER: builtins.int
    enabled: builtins.bool
    def __init__(self,
        *,
        enabled: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["enabled",b"enabled"]) -> None: ...
global___SetServoEnabledRequest = SetServoEnabledRequest

class SetProfileAccelerationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RAD_PER_SEC2_FIELD_NUMBER: builtins.int
    rad_per_sec2: builtins.float
    def __init__(self,
        *,
        rad_per_sec2: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad_per_sec2",b"rad_per_sec2"]) -> None: ...
global___SetProfileAccelerationRequest = SetProfileAccelerationRequest

class SetProfileVelocityRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RAD_PER_SEC_FIELD_NUMBER: builtins.int
    rad_per_sec: builtins.float
    def __init__(self,
        *,
        rad_per_sec: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad_per_sec",b"rad_per_sec"]) -> None: ...
global___SetProfileVelocityRequest = SetProfileVelocityRequest

class SetGoalPositionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RAD_FIELD_NUMBER: builtins.int
    rad: builtins.float
    def __init__(self,
        *,
        rad: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad",b"rad"]) -> None: ...
global___SetGoalPositionRequest = SetGoalPositionRequest

class GetPresentPositionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RAD_FIELD_NUMBER: builtins.int
    rad: builtins.float
    def __init__(self,
        *,
        rad: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad",b"rad"]) -> None: ...
global___GetPresentPositionResponse = GetPresentPositionResponse