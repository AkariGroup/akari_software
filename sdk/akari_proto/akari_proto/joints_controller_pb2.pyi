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

class JointSpecifier(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    JOINT_NAME_FIELD_NUMBER: builtins.int
    joint_name: typing.Text
    def __init__(self,
        *,
        joint_name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["joint_name",b"joint_name"]) -> None: ...
global___JointSpecifier = JointSpecifier

class GetPositionLimitResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    min: builtins.float
    max: builtins.float
    def __init__(self,
        *,
        min: builtins.float = ...,
        max: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["max",b"max","min",b"min"]) -> None: ...
global___GetPositionLimitResponse = GetPositionLimitResponse

class GetJointNamesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    JOINT_NAMES_FIELD_NUMBER: builtins.int
    @property
    def joint_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    def __init__(self,
        *,
        joint_names: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["joint_names",b"joint_names"]) -> None: ...
global___GetJointNamesResponse = GetJointNamesResponse

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
    TARGET_JOINT_FIELD_NUMBER: builtins.int
    ENABLED_FIELD_NUMBER: builtins.int
    @property
    def target_joint(self) -> global___JointSpecifier: ...
    enabled: builtins.bool
    def __init__(self,
        *,
        target_joint: typing.Optional[global___JointSpecifier] = ...,
        enabled: builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["target_joint",b"target_joint"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["enabled",b"enabled","target_joint",b"target_joint"]) -> None: ...
global___SetServoEnabledRequest = SetServoEnabledRequest

class SetProfileAccelerationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TARGET_JOINT_FIELD_NUMBER: builtins.int
    RAD_PER_SEC2_FIELD_NUMBER: builtins.int
    @property
    def target_joint(self) -> global___JointSpecifier: ...
    rad_per_sec2: builtins.float
    def __init__(self,
        *,
        target_joint: typing.Optional[global___JointSpecifier] = ...,
        rad_per_sec2: builtins.float = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["target_joint",b"target_joint"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad_per_sec2",b"rad_per_sec2","target_joint",b"target_joint"]) -> None: ...
global___SetProfileAccelerationRequest = SetProfileAccelerationRequest

class GetProfileAccelerationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RAD_PER_SEC2_FIELD_NUMBER: builtins.int
    rad_per_sec2: builtins.float
    def __init__(self,
        *,
        rad_per_sec2: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad_per_sec2",b"rad_per_sec2"]) -> None: ...
global___GetProfileAccelerationResponse = GetProfileAccelerationResponse

class SetProfileVelocityRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TARGET_JOINT_FIELD_NUMBER: builtins.int
    RAD_PER_SEC_FIELD_NUMBER: builtins.int
    @property
    def target_joint(self) -> global___JointSpecifier: ...
    rad_per_sec: builtins.float
    def __init__(self,
        *,
        target_joint: typing.Optional[global___JointSpecifier] = ...,
        rad_per_sec: builtins.float = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["target_joint",b"target_joint"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad_per_sec",b"rad_per_sec","target_joint",b"target_joint"]) -> None: ...
global___SetProfileVelocityRequest = SetProfileVelocityRequest

class GetProfileVelocityResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RAD_PER_SEC_FIELD_NUMBER: builtins.int
    rad_per_sec: builtins.float
    def __init__(self,
        *,
        rad_per_sec: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad_per_sec",b"rad_per_sec"]) -> None: ...
global___GetProfileVelocityResponse = GetProfileVelocityResponse

class SetGoalPositionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TARGET_JOINT_FIELD_NUMBER: builtins.int
    RAD_FIELD_NUMBER: builtins.int
    @property
    def target_joint(self) -> global___JointSpecifier: ...
    rad: builtins.float
    def __init__(self,
        *,
        target_joint: typing.Optional[global___JointSpecifier] = ...,
        rad: builtins.float = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["target_joint",b"target_joint"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["rad",b"rad","target_joint",b"target_joint"]) -> None: ...
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

class GetMovingStateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MOVING_FIELD_NUMBER: builtins.int
    moving: builtins.bool
    def __init__(self,
        *,
        moving: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["moving",b"moving"]) -> None: ...
global___GetMovingStateResponse = GetMovingStateResponse
