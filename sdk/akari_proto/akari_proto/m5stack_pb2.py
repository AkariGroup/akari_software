# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: akari_proto/m5stack.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x61kari_proto/m5stack.proto\x12\x0b\x61kari_proto\x1a\x1bgoogle/protobuf/empty.proto\"\xb8\x02\n\x10SetPinOutRequest\x12N\n\x0b\x62inary_pins\x18\x01 \x03(\x0b\x32-.akari_proto.SetPinOutRequest.BinaryPinsEntryR\nbinaryPins\x12\x45\n\x08int_pins\x18\x02 \x03(\x0b\x32*.akari_proto.SetPinOutRequest.IntPinsEntryR\x07intPins\x12\x12\n\x04sync\x18\x03 \x01(\x08R\x04sync\x1a=\n\x0f\x42inaryPinsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x08R\x05value:\x02\x38\x01\x1a:\n\x0cIntPinsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x05R\x05value:\x02\x38\x01\"(\n\x12ResetPinOutRequest\x12\x12\n\x04sync\x18\x01 \x01(\x08R\x04sync\"V\n\x16SetDisplayColorRequest\x12(\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x12.akari_proto.ColorR\x05\x63olor\x12\x12\n\x04sync\x18\x02 \x01(\x08R\x04sync\"\xf9\x01\n\x15SetDisplayTextRequest\x12\x12\n\x04text\x18\x01 \x01(\tR\x04text\x12\x13\n\x05pos_x\x18\x02 \x01(\x05R\x04posX\x12\x13\n\x05pos_y\x18\x03 \x01(\x05R\x04posY\x12\x12\n\x04size\x18\x04 \x01(\x05R\x04size\x12\x31\n\ntext_color\x18\x05 \x01(\x0b\x32\x12.akari_proto.ColorR\ttextColor\x12-\n\x08\x62g_color\x18\x06 \x01(\x0b\x32\x12.akari_proto.ColorR\x07\x62gColor\x12\x18\n\x07refresh\x18\x07 \x01(\x08R\x07refresh\x12\x12\n\x04sync\x18\x08 \x01(\x08R\x04sync\"\x80\x01\n\x16SetDisplayImageRequest\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\x12\x13\n\x05pos_x\x18\x02 \x01(\x05R\x04posX\x12\x13\n\x05pos_y\x18\x03 \x01(\x05R\x04posY\x12\x14\n\x05scale\x18\x04 \x01(\x02R\x05scale\x12\x12\n\x04sync\x18\x05 \x01(\x08R\x04sync\"C\n\x05\x43olor\x12\x10\n\x03red\x18\x01 \x01(\x05R\x03red\x12\x14\n\x05green\x18\x02 \x01(\x05R\x05green\x12\x12\n\x04\x62lue\x18\x03 \x01(\x05R\x04\x62lue\"0\n\rM5StackStatus\x12\x1f\n\x0bstatus_json\x18\x01 \x01(\tR\nstatusJson2\xc1\x04\n\x0eM5StackService\x12\x42\n\tSetPinOut\x12\x1d.akari_proto.SetPinOutRequest\x1a\x16.google.protobuf.Empty\x12\x46\n\x0bResetPinOut\x12\x1f.akari_proto.ResetPinOutRequest\x1a\x16.google.protobuf.Empty\x12N\n\x0fSetDisplayColor\x12#.akari_proto.SetDisplayColorRequest\x1a\x16.google.protobuf.Empty\x12L\n\x0eSetDisplayText\x12\".akari_proto.SetDisplayTextRequest\x1a\x16.google.protobuf.Empty\x12N\n\x0fSetDisplayImage\x12#.akari_proto.SetDisplayImageRequest\x1a\x16.google.protobuf.Empty\x12\x37\n\x05Reset\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\x12\x39\n\x03Get\x12\x16.google.protobuf.Empty\x1a\x1a.akari_proto.M5StackStatus\x12\x41\n\tGetStream\x12\x16.google.protobuf.Empty\x1a\x1a.akari_proto.M5StackStatus0\x01\x62\x06proto3')



_SETPINOUTREQUEST = DESCRIPTOR.message_types_by_name['SetPinOutRequest']
_SETPINOUTREQUEST_BINARYPINSENTRY = _SETPINOUTREQUEST.nested_types_by_name['BinaryPinsEntry']
_SETPINOUTREQUEST_INTPINSENTRY = _SETPINOUTREQUEST.nested_types_by_name['IntPinsEntry']
_RESETPINOUTREQUEST = DESCRIPTOR.message_types_by_name['ResetPinOutRequest']
_SETDISPLAYCOLORREQUEST = DESCRIPTOR.message_types_by_name['SetDisplayColorRequest']
_SETDISPLAYTEXTREQUEST = DESCRIPTOR.message_types_by_name['SetDisplayTextRequest']
_SETDISPLAYIMAGEREQUEST = DESCRIPTOR.message_types_by_name['SetDisplayImageRequest']
_COLOR = DESCRIPTOR.message_types_by_name['Color']
_M5STACKSTATUS = DESCRIPTOR.message_types_by_name['M5StackStatus']
SetPinOutRequest = _reflection.GeneratedProtocolMessageType('SetPinOutRequest', (_message.Message,), {

  'BinaryPinsEntry' : _reflection.GeneratedProtocolMessageType('BinaryPinsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SETPINOUTREQUEST_BINARYPINSENTRY,
    '__module__' : 'akari_proto.m5stack_pb2'
    # @@protoc_insertion_point(class_scope:akari_proto.SetPinOutRequest.BinaryPinsEntry)
    })
  ,

  'IntPinsEntry' : _reflection.GeneratedProtocolMessageType('IntPinsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SETPINOUTREQUEST_INTPINSENTRY,
    '__module__' : 'akari_proto.m5stack_pb2'
    # @@protoc_insertion_point(class_scope:akari_proto.SetPinOutRequest.IntPinsEntry)
    })
  ,
  'DESCRIPTOR' : _SETPINOUTREQUEST,
  '__module__' : 'akari_proto.m5stack_pb2'
  # @@protoc_insertion_point(class_scope:akari_proto.SetPinOutRequest)
  })
_sym_db.RegisterMessage(SetPinOutRequest)
_sym_db.RegisterMessage(SetPinOutRequest.BinaryPinsEntry)
_sym_db.RegisterMessage(SetPinOutRequest.IntPinsEntry)

ResetPinOutRequest = _reflection.GeneratedProtocolMessageType('ResetPinOutRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESETPINOUTREQUEST,
  '__module__' : 'akari_proto.m5stack_pb2'
  # @@protoc_insertion_point(class_scope:akari_proto.ResetPinOutRequest)
  })
_sym_db.RegisterMessage(ResetPinOutRequest)

SetDisplayColorRequest = _reflection.GeneratedProtocolMessageType('SetDisplayColorRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETDISPLAYCOLORREQUEST,
  '__module__' : 'akari_proto.m5stack_pb2'
  # @@protoc_insertion_point(class_scope:akari_proto.SetDisplayColorRequest)
  })
_sym_db.RegisterMessage(SetDisplayColorRequest)

SetDisplayTextRequest = _reflection.GeneratedProtocolMessageType('SetDisplayTextRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETDISPLAYTEXTREQUEST,
  '__module__' : 'akari_proto.m5stack_pb2'
  # @@protoc_insertion_point(class_scope:akari_proto.SetDisplayTextRequest)
  })
_sym_db.RegisterMessage(SetDisplayTextRequest)

SetDisplayImageRequest = _reflection.GeneratedProtocolMessageType('SetDisplayImageRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETDISPLAYIMAGEREQUEST,
  '__module__' : 'akari_proto.m5stack_pb2'
  # @@protoc_insertion_point(class_scope:akari_proto.SetDisplayImageRequest)
  })
_sym_db.RegisterMessage(SetDisplayImageRequest)

Color = _reflection.GeneratedProtocolMessageType('Color', (_message.Message,), {
  'DESCRIPTOR' : _COLOR,
  '__module__' : 'akari_proto.m5stack_pb2'
  # @@protoc_insertion_point(class_scope:akari_proto.Color)
  })
_sym_db.RegisterMessage(Color)

M5StackStatus = _reflection.GeneratedProtocolMessageType('M5StackStatus', (_message.Message,), {
  'DESCRIPTOR' : _M5STACKSTATUS,
  '__module__' : 'akari_proto.m5stack_pb2'
  # @@protoc_insertion_point(class_scope:akari_proto.M5StackStatus)
  })
_sym_db.RegisterMessage(M5StackStatus)

_M5STACKSERVICE = DESCRIPTOR.services_by_name['M5StackService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SETPINOUTREQUEST_BINARYPINSENTRY._options = None
  _SETPINOUTREQUEST_BINARYPINSENTRY._serialized_options = b'8\001'
  _SETPINOUTREQUEST_INTPINSENTRY._options = None
  _SETPINOUTREQUEST_INTPINSENTRY._serialized_options = b'8\001'
  _SETPINOUTREQUEST._serialized_start=72
  _SETPINOUTREQUEST._serialized_end=384
  _SETPINOUTREQUEST_BINARYPINSENTRY._serialized_start=263
  _SETPINOUTREQUEST_BINARYPINSENTRY._serialized_end=324
  _SETPINOUTREQUEST_INTPINSENTRY._serialized_start=326
  _SETPINOUTREQUEST_INTPINSENTRY._serialized_end=384
  _RESETPINOUTREQUEST._serialized_start=386
  _RESETPINOUTREQUEST._serialized_end=426
  _SETDISPLAYCOLORREQUEST._serialized_start=428
  _SETDISPLAYCOLORREQUEST._serialized_end=514
  _SETDISPLAYTEXTREQUEST._serialized_start=517
  _SETDISPLAYTEXTREQUEST._serialized_end=766
  _SETDISPLAYIMAGEREQUEST._serialized_start=769
  _SETDISPLAYIMAGEREQUEST._serialized_end=897
  _COLOR._serialized_start=899
  _COLOR._serialized_end=966
  _M5STACKSTATUS._serialized_start=968
  _M5STACKSTATUS._serialized_end=1016
  _M5STACKSERVICE._serialized_start=1019
  _M5STACKSERVICE._serialized_end=1596
# @@protoc_insertion_point(module_scope)
