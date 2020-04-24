#!/usr/bin/env bash

messages_file=messages.proto
messages_module=../MobiliumProtoMessages/mobilium_proto_messages/proto
driver=../MobiliumDriver/MobiliumDriver/proto
protoc --python_out=$messages_module --swift_out=$driver $messages_file
