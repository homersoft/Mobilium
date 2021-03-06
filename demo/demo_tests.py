import argparse
from mobilium_client.client import MobiliumClient
from mobilium_proto_messages.accessibility import Accessibility, AccessibilityById, AccessibilityByXpath


class TestRunner:

    def __init__(self, device_udid: str, server_address: str, port: int):
        self.client = MobiliumClient()
        self.device_udid = device_udid
        self.server_address = server_address
        self.port = port

    def perform_tests(self):
        self.client.connect(self.device_udid, self.server_address, self.port)
        self.client.start_driver()
        self.client.install_app(file_path="demo/demo.ipa")
        self.test_user_puts_phone_and_code_and_touch_login()
        self.test_user_saves_all_required_data()
        self.test_user_logout()
        self.client.terminate_app()
        self.client.disconnect()

    def test_user_puts_phone_and_code_and_touch_login(self):
        # given: login page is visible
        self.client.launch_app(bundle_id="com.silvair.demo")

        # when user login in with valid credentials
        self.client.set_element_text(AccessibilityById("phone_field"), "111111111")
        self.client.set_element_text(AccessibilityById("code_field"), "1111")
        self.client.click_element(AccessibilityById("login_button"))

        #then "Your accoount" page is visible
        navigation_title = self.client.get_element_id(AccessibilityByXpath("//XCUIElementTypeNavigationBar"))
        assert navigation_title in "Your account", "Your account page is not visible"

    def test_user_saves_all_required_data(self):
        # given: Your account page is visible

        #when: User fulfill all data
        self.client.set_element_text(AccessibilityById("first_name_field"), "John")
        self.client.set_element_text(AccessibilityById("second_name_field"), "Doe")
        self.client.set_element_text(AccessibilityById("email_field"), "john_doe@example.com")
        self.client.set_element_text(AccessibilityById("phone_field"), "111111111")
        self.client.set_element_text(AccessibilityById("location_field"), "Example")
        self.client.click_element(AccessibilityById("save_button"))

        # then: success label is visible
        is_success_visible = self.client.is_element_visible(AccessibilityById("success_label"))
        assert is_success_visible, "Success label is not visible"

    def test_user_logout(self):
        # given: User is on "Your account" page

        #when: user logouts
        self.client.click_element(AccessibilityById("logout_button"))

        #then "Login" page is visible
        page_title = self.client.get_element_id(AccessibilityByXpath("//XCUIElementTypeNavigationBar"))
        assert page_title in "Login", "Login page is not visible"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--address", help="Mobilium Server IP Address", required=True)
    parser.add_argument("-p", "--port", help="Mobilium Server port. Default: 65432", default=65432)
    parser.add_argument("-u", "--udid", help="UDID of iOS device on which tests are run", required=True)
    arguments = parser.parse_args()

    test_runner = TestRunner(arguments.udid, arguments.address, arguments.port)
    test_runner.perform_tests()

if __name__ == '__main__':
    main()
