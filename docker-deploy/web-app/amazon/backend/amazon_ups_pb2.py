# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: amazon_ups.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='amazon_ups.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x10\x61mazon_ups.proto\"\x1d\n\nUTAConnect\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\"\x1e\n\x0b\x41UConnected\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\"!\n\tDesti_loc\x12\t\n\x01x\x18\x01 \x02(\x03\x12\t\n\x01y\x18\x02 \x02(\x03\"\x8f\x01\n\x10\x41TURequestPickup\x12\x14\n\x0cproduct_name\x18\x01 \x02(\t\x12\x11\n\tpackageid\x18\x02 \x02(\x03\x12\x13\n\x0bups_account\x18\x03 \x01(\t\x12\x0c\n\x04whid\x18\x04 \x02(\x03\x12\x1f\n\x0b\x64\x65stination\x18\x05 \x02(\x0b\x32\n.Desti_loc\x12\x0e\n\x06seqnum\x18\x06 \x02(\x03\"N\n\nUTAArrived\x12\x11\n\tpackageid\x18\x01 \x03(\x03\x12\x0f\n\x07truckid\x18\x02 \x02(\x03\x12\x0c\n\x04whid\x18\x03 \x02(\x03\x12\x0e\n\x06seqnum\x18\x04 \x02(\x03\"?\n\tATULoaded\x12\x11\n\tpackageid\x18\x01 \x03(\x03\x12\x0f\n\x07truckid\x18\x02 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"I\n\x0eUTAOutDelivery\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\t\n\x01x\x18\x02 \x02(\x03\x12\t\n\x01y\x18\x03 \x02(\x03\x12\x0e\n\x06seqnum\x18\x04 \x02(\x03\"1\n\x0cUTADelivered\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0e\n\x06seqnum\x18\x02 \x02(\x03\":\n\x05\x41UErr\x12\x0b\n\x03\x65rr\x18\x01 \x02(\t\x12\x14\n\x0coriginseqnum\x18\x02 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"q\n\x0b\x41TUCommands\x12#\n\x08topickup\x18\x01 \x03(\x0b\x32\x11.ATURequestPickup\x12\x1a\n\x06loaded\x18\x02 \x03(\x0b\x32\n.ATULoaded\x12\x13\n\x03\x65rr\x18\x03 \x03(\x0b\x32\x06.AUErr\x12\x0c\n\x04\x61\x63ks\x18\x04 \x03(\x03\"\x93\x01\n\x0bUTACommands\x12\x1b\n\x06\x61rrive\x18\x01 \x03(\x0b\x32\x0b.UTAArrived\x12\"\n\ttodeliver\x18\x02 \x03(\x0b\x32\x0f.UTAOutDelivery\x12 \n\tdelivered\x18\x03 \x03(\x0b\x32\r.UTADelivered\x12\x13\n\x03\x65rr\x18\x04 \x03(\x0b\x32\x06.AUErr\x12\x0c\n\x04\x61\x63ks\x18\x05 \x03(\x03')
)




_UTACONNECT = _descriptor.Descriptor(
  name='UTAConnect',
  full_name='UTAConnect',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='worldid', full_name='UTAConnect.worldid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=49,
)


_AUCONNECTED = _descriptor.Descriptor(
  name='AUConnected',
  full_name='AUConnected',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='worldid', full_name='AUConnected.worldid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=81,
)


_DESTI_LOC = _descriptor.Descriptor(
  name='Desti_loc',
  full_name='Desti_loc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Desti_loc.x', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='Desti_loc.y', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=116,
)


_ATUREQUESTPICKUP = _descriptor.Descriptor(
  name='ATURequestPickup',
  full_name='ATURequestPickup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_name', full_name='ATURequestPickup.product_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='packageid', full_name='ATURequestPickup.packageid', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ups_account', full_name='ATURequestPickup.ups_account', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='whid', full_name='ATURequestPickup.whid', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='destination', full_name='ATURequestPickup.destination', index=4,
      number=5, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='ATURequestPickup.seqnum', index=5,
      number=6, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=262,
)


_UTAARRIVED = _descriptor.Descriptor(
  name='UTAArrived',
  full_name='UTAArrived',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='UTAArrived.packageid', index=0,
      number=1, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='UTAArrived.truckid', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='whid', full_name='UTAArrived.whid', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='UTAArrived.seqnum', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=264,
  serialized_end=342,
)


_ATULOADED = _descriptor.Descriptor(
  name='ATULoaded',
  full_name='ATULoaded',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='ATULoaded.packageid', index=0,
      number=1, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='ATULoaded.truckid', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='ATULoaded.seqnum', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=344,
  serialized_end=407,
)


_UTAOUTDELIVERY = _descriptor.Descriptor(
  name='UTAOutDelivery',
  full_name='UTAOutDelivery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='UTAOutDelivery.packageid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='x', full_name='UTAOutDelivery.x', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='UTAOutDelivery.y', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='UTAOutDelivery.seqnum', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=409,
  serialized_end=482,
)


_UTADELIVERED = _descriptor.Descriptor(
  name='UTADelivered',
  full_name='UTADelivered',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='UTADelivered.packageid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='UTADelivered.seqnum', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=484,
  serialized_end=533,
)


_AUERR = _descriptor.Descriptor(
  name='AUErr',
  full_name='AUErr',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='err', full_name='AUErr.err', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='originseqnum', full_name='AUErr.originseqnum', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='AUErr.seqnum', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=535,
  serialized_end=593,
)


_ATUCOMMANDS = _descriptor.Descriptor(
  name='ATUCommands',
  full_name='ATUCommands',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='topickup', full_name='ATUCommands.topickup', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loaded', full_name='ATUCommands.loaded', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='err', full_name='ATUCommands.err', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acks', full_name='ATUCommands.acks', index=3,
      number=4, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=595,
  serialized_end=708,
)


_UTACOMMANDS = _descriptor.Descriptor(
  name='UTACommands',
  full_name='UTACommands',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arrive', full_name='UTACommands.arrive', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='todeliver', full_name='UTACommands.todeliver', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delivered', full_name='UTACommands.delivered', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='err', full_name='UTACommands.err', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acks', full_name='UTACommands.acks', index=4,
      number=5, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=711,
  serialized_end=858,
)

_ATUREQUESTPICKUP.fields_by_name['destination'].message_type = _DESTI_LOC
_ATUCOMMANDS.fields_by_name['topickup'].message_type = _ATUREQUESTPICKUP
_ATUCOMMANDS.fields_by_name['loaded'].message_type = _ATULOADED
_ATUCOMMANDS.fields_by_name['err'].message_type = _AUERR
_UTACOMMANDS.fields_by_name['arrive'].message_type = _UTAARRIVED
_UTACOMMANDS.fields_by_name['todeliver'].message_type = _UTAOUTDELIVERY
_UTACOMMANDS.fields_by_name['delivered'].message_type = _UTADELIVERED
_UTACOMMANDS.fields_by_name['err'].message_type = _AUERR
DESCRIPTOR.message_types_by_name['UTAConnect'] = _UTACONNECT
DESCRIPTOR.message_types_by_name['AUConnected'] = _AUCONNECTED
DESCRIPTOR.message_types_by_name['Desti_loc'] = _DESTI_LOC
DESCRIPTOR.message_types_by_name['ATURequestPickup'] = _ATUREQUESTPICKUP
DESCRIPTOR.message_types_by_name['UTAArrived'] = _UTAARRIVED
DESCRIPTOR.message_types_by_name['ATULoaded'] = _ATULOADED
DESCRIPTOR.message_types_by_name['UTAOutDelivery'] = _UTAOUTDELIVERY
DESCRIPTOR.message_types_by_name['UTADelivered'] = _UTADELIVERED
DESCRIPTOR.message_types_by_name['AUErr'] = _AUERR
DESCRIPTOR.message_types_by_name['ATUCommands'] = _ATUCOMMANDS
DESCRIPTOR.message_types_by_name['UTACommands'] = _UTACOMMANDS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UTAConnect = _reflection.GeneratedProtocolMessageType('UTAConnect', (_message.Message,), dict(
  DESCRIPTOR = _UTACONNECT,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UTAConnect)
  ))
_sym_db.RegisterMessage(UTAConnect)

AUConnected = _reflection.GeneratedProtocolMessageType('AUConnected', (_message.Message,), dict(
  DESCRIPTOR = _AUCONNECTED,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:AUConnected)
  ))
_sym_db.RegisterMessage(AUConnected)

Desti_loc = _reflection.GeneratedProtocolMessageType('Desti_loc', (_message.Message,), dict(
  DESCRIPTOR = _DESTI_LOC,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:Desti_loc)
  ))
_sym_db.RegisterMessage(Desti_loc)

ATURequestPickup = _reflection.GeneratedProtocolMessageType('ATURequestPickup', (_message.Message,), dict(
  DESCRIPTOR = _ATUREQUESTPICKUP,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:ATURequestPickup)
  ))
_sym_db.RegisterMessage(ATURequestPickup)

UTAArrived = _reflection.GeneratedProtocolMessageType('UTAArrived', (_message.Message,), dict(
  DESCRIPTOR = _UTAARRIVED,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UTAArrived)
  ))
_sym_db.RegisterMessage(UTAArrived)

ATULoaded = _reflection.GeneratedProtocolMessageType('ATULoaded', (_message.Message,), dict(
  DESCRIPTOR = _ATULOADED,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:ATULoaded)
  ))
_sym_db.RegisterMessage(ATULoaded)

UTAOutDelivery = _reflection.GeneratedProtocolMessageType('UTAOutDelivery', (_message.Message,), dict(
  DESCRIPTOR = _UTAOUTDELIVERY,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UTAOutDelivery)
  ))
_sym_db.RegisterMessage(UTAOutDelivery)

UTADelivered = _reflection.GeneratedProtocolMessageType('UTADelivered', (_message.Message,), dict(
  DESCRIPTOR = _UTADELIVERED,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UTADelivered)
  ))
_sym_db.RegisterMessage(UTADelivered)

AUErr = _reflection.GeneratedProtocolMessageType('AUErr', (_message.Message,), dict(
  DESCRIPTOR = _AUERR,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:AUErr)
  ))
_sym_db.RegisterMessage(AUErr)

ATUCommands = _reflection.GeneratedProtocolMessageType('ATUCommands', (_message.Message,), dict(
  DESCRIPTOR = _ATUCOMMANDS,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:ATUCommands)
  ))
_sym_db.RegisterMessage(ATUCommands)

UTACommands = _reflection.GeneratedProtocolMessageType('UTACommands', (_message.Message,), dict(
  DESCRIPTOR = _UTACOMMANDS,
  __module__ = 'amazon_ups_pb2'
  # @@protoc_insertion_point(class_scope:UTACommands)
  ))
_sym_db.RegisterMessage(UTACommands)


# @@protoc_insertion_point(module_scope)
