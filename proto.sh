messages_file=proto/messages.proto
client=MobiliumClient/mobilium_client
server=MobiliumServer/mobilium_server
driver=MobiliumDriver/MobiliumDriver
protoc --python_out=$client --python_out=$server --swift_out=$driver $messages_file
