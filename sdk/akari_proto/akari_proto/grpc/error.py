import contextlib
import functools
import json
import logging
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    Optional,
    Protocol,
    Type,
    TypeVar,
    cast,
    runtime_checkable,
)

import grpc

_logger = logging.getLogger(__name__)

TRequest = TypeVar("TRequest")
TException = TypeVar("TException", bound=BaseException, covariant=True)

TServicerCallable = TypeVar(
    "TServicerCallable", bound=Callable[[Any, Any, grpc.ServicerContext], Any]
)
TCallable = TypeVar("TCallable", bound=Callable[..., Any])


@runtime_checkable
class SerializableException(Protocol):
    __name__: str

    def to_dict(self) -> Dict[str, Any]:
        ...

    @classmethod
    def from_dict(cls: Type[TException], data: Dict[str, Any]) -> TException:
        ...


class RPCErrorSerializer:
    def __init__(self) -> None:
        self._mapping: Dict[str, Type[SerializableException]] = {}

    def register(self, klass: Type[SerializableException]) -> None:
        name = klass.__name__
        if name in self._mapping:
            raise ValueError(f"Exception name duplicated: {name}")

        self._mapping[name] = klass

    def serialize(self, exception: BaseException) -> Optional[str]:
        if not isinstance(exception, SerializableException):
            return None

        name = exception.__name__
        if name not in self._mapping:
            return None

        try:
            data = exception.to_dict()
            payload_dict = {
                "exception_class": name,
                "exception_data": data,
            }
            return json.dumps(payload_dict)
        except Exception:
            _logger.exception(f"Failed to serialize exception: '{exception}'")
            return None

    def deserialize(self, payload: Optional[str]) -> Optional[BaseException]:
        try:
            if payload is None:
                return None

            payload_dict = json.loads(payload)
            name = payload_dict["exception_class"]
            data = payload_dict["exception_data"]
            klass = self._mapping.get(name)
            if klass is None:
                _logger.warning(f"Failed to lookup class: {klass}")
                return None

            return klass.from_dict(data)
        except Exception:
            _logger.exception(f"Failed to deserialize payload: '{payload}'")
            return None


@contextlib.contextmanager
def _serialize_error(
    serializer: RPCErrorSerializer, context: grpc.ServicerContext
) -> Iterator[None]:
    try:
        yield
    except BaseException as e:
        data = serializer.serialize(e)
        if data is None:
            raise
        else:
            context.set_details(data)


@contextlib.contextmanager
def _deserialize_error(serializer: RPCErrorSerializer) -> Iterator[None]:
    try:
        yield
    except grpc.RpcError as e:
        code = getattr(e, "code", None)
        if code is not grpc.StatusCode.INTERNAL:
            raise

        err = serializer.deserialize(e.details())
        if err is None:
            raise
        else:
            raise err from None


def serialize_error(
    serializer: RPCErrorSerializer,
) -> Callable[[TServicerCallable], TServicerCallable]:
    def deco(f: TServicerCallable) -> TServicerCallable:
        @functools.wraps(f)
        def impl(self: Any, request: TRequest, context: grpc.ServicerContext) -> Any:
            with _serialize_error(serializer, context):
                return f(self, request, context)

        return cast(TServicerCallable, impl)

    return deco


def deserialize_error(
    serializer: RPCErrorSerializer,
) -> Callable[[TCallable], TCallable]:
    def deco(f: TCallable) -> TCallable:
        @functools.wraps(f)
        def impl(*args: Any, **kwargs: Any) -> Any:
            with _deserialize_error(serializer):
                return f(*args, **kwargs)

        return cast(TCallable, impl)

    return deco
