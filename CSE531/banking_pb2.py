# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: banking.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='banking.proto',
  package='app',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rbanking.proto\x12\x03\x61pp\"m\n\x12MsgDeliveryRequest\x12\x0e\n\x06REQ_ID\x18\x01 \x01(\x03\x12\x1a\n\x02OP\x18\x02 \x01(\x0e\x32\x0e.app.Operation\x12\x0e\n\x06\x41mount\x18\x03 \x01(\x03\x12\x0c\n\x04\x44_ID\x18\x04 \x01(\x03\x12\r\n\x05\x43lock\x18\x05 \x01(\x03\"]\n\x13MsgDeliveryResponse\x12\n\n\x02ID\x18\x01 \x01(\x03\x12\x1b\n\x02RC\x18\x02 \x01(\x0e\x32\x0f.app.ReturnCode\x12\x0e\n\x06\x41mount\x18\x03 \x01(\x03\x12\r\n\x05\x43lock\x18\x04 \x01(\x03\"\x0f\n\rEventsRequest\",\n\x0e\x45ventsResponse\x12\x1a\n\x06\x65vents\x18\x01 \x03(\x0b\x32\n.app.Event\"1\n\x05\x45vent\x12\x0b\n\x03id_\x18\x01 \x01(\x03\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05\x63lock\x18\x03 \x01(\x03*\x82\x01\n\tOperation\x12\t\n\x05QUERY\x10\x00\x12\x0b\n\x07\x44\x45POSIT\x10\x01\x12\x0c\n\x08WITHDRAW\x10\x02\x12\x0e\n\nEV_REQUEST\x10\x03\x12\x0e\n\nEV_EXECUTE\x10\x04\x12\x0e\n\nPR_REQUEST\x10\x05\x12\x0e\n\nPR_EXECUTE\x10\x06\x12\x0f\n\x0bPR_RESPONSE\x10\x07*1\n\nReturnCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0b\n\x07\x46\x41ILURE\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x32\x85\x01\n\x07\x42\x61nking\x12\x42\n\x0bMsgDelivery\x12\x17.app.MsgDeliveryRequest\x1a\x18.app.MsgDeliveryResponse\"\x00\x12\x36\n\tGetEvents\x12\x12.app.EventsRequest\x1a\x13.app.EventsResponse\"\x00\x62\x06proto3'
)

_OPERATION = _descriptor.EnumDescriptor(
  name='Operation',
  full_name='app.Operation',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='QUERY', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEPOSIT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WITHDRAW', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EV_REQUEST', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EV_EXECUTE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PR_REQUEST', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PR_EXECUTE', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PR_RESPONSE', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=343,
  serialized_end=473,
)
_sym_db.RegisterEnumDescriptor(_OPERATION)

Operation = enum_type_wrapper.EnumTypeWrapper(_OPERATION)
_RETURNCODE = _descriptor.EnumDescriptor(
  name='ReturnCode',
  full_name='app.ReturnCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FAILURE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=475,
  serialized_end=524,
)
_sym_db.RegisterEnumDescriptor(_RETURNCODE)

ReturnCode = enum_type_wrapper.EnumTypeWrapper(_RETURNCODE)
QUERY = 0
DEPOSIT = 1
WITHDRAW = 2
EV_REQUEST = 3
EV_EXECUTE = 4
PR_REQUEST = 5
PR_EXECUTE = 6
PR_RESPONSE = 7
SUCCESS = 0
FAILURE = 1
ERROR = 2



_MSGDELIVERYREQUEST = _descriptor.Descriptor(
  name='MsgDeliveryRequest',
  full_name='app.MsgDeliveryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='REQ_ID', full_name='app.MsgDeliveryRequest.REQ_ID', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='OP', full_name='app.MsgDeliveryRequest.OP', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Amount', full_name='app.MsgDeliveryRequest.Amount', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='D_ID', full_name='app.MsgDeliveryRequest.D_ID', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Clock', full_name='app.MsgDeliveryRequest.Clock', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=131,
)


_MSGDELIVERYRESPONSE = _descriptor.Descriptor(
  name='MsgDeliveryResponse',
  full_name='app.MsgDeliveryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='app.MsgDeliveryResponse.ID', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='RC', full_name='app.MsgDeliveryResponse.RC', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Amount', full_name='app.MsgDeliveryResponse.Amount', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Clock', full_name='app.MsgDeliveryResponse.Clock', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=133,
  serialized_end=226,
)


_EVENTSREQUEST = _descriptor.Descriptor(
  name='EventsRequest',
  full_name='app.EventsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=228,
  serialized_end=243,
)


_EVENTSRESPONSE = _descriptor.Descriptor(
  name='EventsResponse',
  full_name='app.EventsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='events', full_name='app.EventsResponse.events', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=245,
  serialized_end=289,
)


_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='app.Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id_', full_name='app.Event.id_', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='app.Event.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clock', full_name='app.Event.clock', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=291,
  serialized_end=340,
)

_MSGDELIVERYREQUEST.fields_by_name['OP'].enum_type = _OPERATION
_MSGDELIVERYRESPONSE.fields_by_name['RC'].enum_type = _RETURNCODE
_EVENTSRESPONSE.fields_by_name['events'].message_type = _EVENT
DESCRIPTOR.message_types_by_name['MsgDeliveryRequest'] = _MSGDELIVERYREQUEST
DESCRIPTOR.message_types_by_name['MsgDeliveryResponse'] = _MSGDELIVERYRESPONSE
DESCRIPTOR.message_types_by_name['EventsRequest'] = _EVENTSREQUEST
DESCRIPTOR.message_types_by_name['EventsResponse'] = _EVENTSRESPONSE
DESCRIPTOR.message_types_by_name['Event'] = _EVENT
DESCRIPTOR.enum_types_by_name['Operation'] = _OPERATION
DESCRIPTOR.enum_types_by_name['ReturnCode'] = _RETURNCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MsgDeliveryRequest = _reflection.GeneratedProtocolMessageType('MsgDeliveryRequest', (_message.Message,), {
  'DESCRIPTOR' : _MSGDELIVERYREQUEST,
  '__module__' : 'banking_pb2'
  # @@protoc_insertion_point(class_scope:app.MsgDeliveryRequest)
  })
_sym_db.RegisterMessage(MsgDeliveryRequest)

MsgDeliveryResponse = _reflection.GeneratedProtocolMessageType('MsgDeliveryResponse', (_message.Message,), {
  'DESCRIPTOR' : _MSGDELIVERYRESPONSE,
  '__module__' : 'banking_pb2'
  # @@protoc_insertion_point(class_scope:app.MsgDeliveryResponse)
  })
_sym_db.RegisterMessage(MsgDeliveryResponse)

EventsRequest = _reflection.GeneratedProtocolMessageType('EventsRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVENTSREQUEST,
  '__module__' : 'banking_pb2'
  # @@protoc_insertion_point(class_scope:app.EventsRequest)
  })
_sym_db.RegisterMessage(EventsRequest)

EventsResponse = _reflection.GeneratedProtocolMessageType('EventsResponse', (_message.Message,), {
  'DESCRIPTOR' : _EVENTSRESPONSE,
  '__module__' : 'banking_pb2'
  # @@protoc_insertion_point(class_scope:app.EventsResponse)
  })
_sym_db.RegisterMessage(EventsResponse)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), {
  'DESCRIPTOR' : _EVENT,
  '__module__' : 'banking_pb2'
  # @@protoc_insertion_point(class_scope:app.Event)
  })
_sym_db.RegisterMessage(Event)



_BANKING = _descriptor.ServiceDescriptor(
  name='Banking',
  full_name='app.Banking',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=527,
  serialized_end=660,
  methods=[
  _descriptor.MethodDescriptor(
    name='MsgDelivery',
    full_name='app.Banking.MsgDelivery',
    index=0,
    containing_service=None,
    input_type=_MSGDELIVERYREQUEST,
    output_type=_MSGDELIVERYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetEvents',
    full_name='app.Banking.GetEvents',
    index=1,
    containing_service=None,
    input_type=_EVENTSREQUEST,
    output_type=_EVENTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BANKING)

DESCRIPTOR.services_by_name['Banking'] = _BANKING

# @@protoc_insertion_point(module_scope)
