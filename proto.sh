#!/usr/bin/env bash

messages_file=proto/messages.proto
messages_module=MobiliumProtoMessages/mobilium_proto_messages
driver=MobiliumDriver/MobiliumDriver
protoc --python_out=$messages_module --swift_out=$driver $messages_file
