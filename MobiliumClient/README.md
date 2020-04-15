# Mobilium Client

Mobilium Client is a part of Mobilium testing framework, it allows to communicate with Mobilium Server and perform actions required to perform UI tests on iOS/iPadOS device/simulator.

## Available methods
MobiliumClient object provides public API that allows using client.
This API can be divided into two groups: App management and user interactions.
##### App Management methods
- Connect client with a running Mobilium Server instance.
```
def connect(self, device_udid: str, address: str, port: int)
```
- Disconnect client from server
```
def disconnect(self)
```
- Update/install all underlying driver dependencies (Carthage).
```
def prepare_driver(self)
```
- Run Mobilium Driver on device/simulator
```
def start_driver(self, timeout: int = 180)
```
- Install app saved at file_path on the device/simulator
```
def install_app(self, file_path: str)
```
- Launch app with bundle_id on the device/simulator
```
def launch_app(self, bundle_id: str)
```
- Uninstall app with bundle_id from device/simulator
```
def uninstall_app(self, bundle_id: str)
```
- Terminate the currently running app
```
def terminate_app(self)
```


#### User interaction methods
- Perform touch action at given point
```
def touch(self, x: int, y: int)
```
- Get device/simulator screen dimensions (width, height)
```
def get_window_size(self) -> WindowSize
```
- Check if given element is visible on the screen with one second periods waiting for visibility of this element for a given timeout. If element doesn't appear until timeout then it returns false
```
def is_element_visible(self, accessibility: Accessibility, index: int = 0, timeout: float = 0) -> bool
```
- Verify if given element is not on the screen. This method can also wait given period of time (timeout) waiting until this element disappear if its currently visible
```
def is_element_invisible(self, accessibility: Accessibility, index: int = 0, timeout: float = 0) -> bool
```
- Check if user interactions for element with given accessibility is enabled
```
def is_element_enabled(self, accessibility: Accessibility, index: int = 0) -> bool
```
- Set text on elements that allows to do that (text fields, and text views). it allows to clear current text field content (`clears == true`) or leave it as it is.
```
def set_element_text(self, accessibility: Accessibility, text: str, index: int = 0, clears: bool = True)
```
- Adjust iOS sliders. Position should be between [0, 1].
```
def set_slider_position(self, accessibility: Accessibility, position: float, index: int = 0)
```
- Get value (text or label) of element with given accessibility.
```
def get_element_value(self, accessibility: Accessibility, index: int = 0) -> str
```
- Perform click (touch up inside) action on element with given accessibility
```
def click_element(self, accessibility: Accessibility, index: int = 0)
```
- Get total amount of elements with provided accessibility. For unique elements it will always returns 1.
```
def get_elements_count(self, accessibility: Accessibility) -> int
```
- Get element accessibility identifier based on element XPath.
```
def get_element_id(self, accessibility: Accessibility, index: int = 0) -> str
```

## Short story about accessibility
When you are working with XCUITests there are two possibilities to identify an element.
- Using accessibility identifier
- Building a query that allows finding elements that match this query

That's why we've decided to support two types of accessibility element matching:
- `AccessibilityById`
- `AccessibilityByXpath`

Accessibility identifiers is most popular way to identify an element. You can set element accessibility identifier be setting following element property.
```
let label = UILabel()
label.text = "My label text"
label.accessibilityIdentifier = "my_label"
```
And then you can access to that element using `AccessibilityById` reference
```
label_text = client.get_element_value(AccessibilityById("my_label"))
assert(label_text == "My label text") # true
```
But sometimes when view structure is complicated you would like to use a more sophisticated way to access an element. Let's assume that you have cells that are identified uniquely (cell_1, cell_2), and inside these cells there is a button with accessibility identifier "my_button". In this case to access a button inside the second cell you can't use AccessibilityById because there are two elements with this identifier on the screen. In this scenario AccessibilityByXpath is helpful. You can use the following code to touch button inside second cell.
```
button_xPath = "XCUIElementTypeCell[contains(@label, 'cell_2')]/XCUIElementTypeButton" \
                                   "[contains(@label, 'my_button')]"
client.click_element(AccessibilityByXpath(button_xPath))
```
You can read more about accessibility [here](https://bitbar.com/blog/appium-tip-18-how-to-use-xpath-locators-efficiently/)
