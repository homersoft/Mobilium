messages_file=proto/messages.proto
client=MobiliumClient/mobilium_client
server=MobiliumServer/mobilium_server
messages=MobiliumProtoMessages/mobilium_proto_messages
driver=MobiliumDriver/MobiliumDriver
protoc --python_out=$client --python_out=$server --python_out=$messages --swift_out=$driver $messages_file
