from mobilium_proto_messages.message_deserializer import MessageDeserializer
from mobilium_proto_messages.proto.messages_pb2 import ElementNotExists

class MessageValidator:
    def validate_is_element_visible_response(self, data: bytes, is_visible: bool):
        def validate(message):
            return message.is_visible == is_visible
        self.__validate(data, MessageDeserializer.is_element_visible_response, validate)

    def validate_set_value_of_element_response(self, data: bytes, success: bool):
        def validate(message):
            return message.success == success
        self.__validate(data, MessageDeserializer.set_value_of_element_response, validate)

    def validate_get_value_of_element_response(self, data: bytes, value: str):
        def validate(message):
            return message.value == value
        self.__validate(data, MessageDeserializer.get_value_of_element_response, validate)

    def validate_click_element_response(self, data: bytes, success: bool):
        def validate(message):
            return message.success == success
        self.__validate(data, MessageDeserializer.click_element_response, validate)

    def validate_element_not_exists(self, data: bytes, parser):
        def validate(message):
            return message.failure.elementNotExists
        self.__validate(data, parser, validate)

    def __validate(self, data: bytes, parser, validator):
        message = parser(data)
        if not validator(message):
            print("Invalid message: %s" % message)

