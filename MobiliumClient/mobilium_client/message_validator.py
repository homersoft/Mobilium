from mobilium_proto_messages.message_deserializer import MessageDeserializer


def validate_is_element_visible_response(data: bytes, is_visible: bool):
    def validate(message):
        return message.is_visible == is_visible
    __validate(data, MessageDeserializer.is_element_visible_response, validate)


def validate_set_value_of_element_response(data: bytes, success: bool):
    def validate(message):
        return message.success == success
    __validate(data, MessageDeserializer.set_value_of_element_response, validate)


def validate_get_value_of_element_response(data: bytes, value: str):
    def validate(message):
        return message.value == value
    __validate(data, MessageDeserializer.get_value_of_element_response, validate)


def validate_click_element_response(data: bytes, success: bool):
    def validate(message):
        return message.success == success
    __validate(data, MessageDeserializer.click_element_response, validate)


def validate_element_not_exists(data: bytes, parser):
    def validate(message):
        return message.failure.elementNotExists
    __validate(data, parser, validate)


def __validate(data: bytes, parser, validator):
    message = parser(data)
    if not validator(message):
        print("Message validation failed. Message %s" % message)
