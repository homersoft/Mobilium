# Mobilium

Mobilium is an open-source testing framework that allows testing iOS/iPadOS applications. Mobilium can be used independently, but also can be included in other testing frameworks as a replacement for Appium WebDriver.

## Motivation
We build Mobilium as an Appium WebDriver replacement taking under the consideration Appium poor performance and many other Appium drawbacks.

## Requirments
- Xcode 11.4 [Apple](https://developer.apple.com/news/releases/?id=03032020f)
- Python3 [Installation instructions](https://docs.python-guide.org/starting/install3/osx/)
- Pip [How to install pip](https://pip.pypa.io/en/stable/installing/)
- Carthage [Get Carthage](https://github.com/Carthage/Carthage)

NOTE:
```
iOS/iPad device needs to be connected to this same local network to which Mobilium Server machine is connected
```

## How to install

- Clone this repo
- In terminal run `pip install .`
- Navigate to  `MobiliumDriver` and run `carthage update --platform iOS --cache-builds`

This will install 2 command-line tools in your environment: `mobilium-server`, and `mobilium-client`.

## How to use

- Obtain your localhost ip address using `ifconfig`
- run server `mobilium-server ip_address` e.g. `mobilium-server 192.168.1.7`
- obtain desired simulator or device id using `instruments -s devices`
- if you are running your app on simulator open Simulator.app `open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app`
- copy your app.ipa file into Mobilium directory
- write your first test:
```
client = MobiliumClient()
client.connect(device_udid: "719BB1CB-FCA2-4826-94AB-FEDC84BCE1AA", \
               address: "192.168.1.7", port: 65432)
client.start_driver()
client.install_app("./app.ipa") # relative path to your app to Mobilium repo
client.launch_app("com.mobilium.demo") # bundle id of your app
```
- Save as `test.py` and run using: `python3 test.py`
After those step, your app should be launched on the simulator

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
- Install app saved at file_path on the device/simulator. If file_path will be nil, then file_path from config.py file will be taken
```
def install_app(self, file_path: Optional[str] = None)
```
- Launch app with bundle_id on the device/simulator. If bundle_id is nil, bundle_id from config.py will be used.
```
def launch_app(self, bundle_id: Optional[str] = None)
```
- Uninstall app with bundle_id from device/simulator
```
def uninstall_app(self, bundle_id: Optional[str] = None)
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
When you are working with XCUITests there is two possibilities to identify an element.
- Using accessibility identifier
- Building query that allows to find elements that match this query

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
But sometimes when view structure is complicated you would like to use more sofisticated way to access an element. Let's assume that you have cells that are identified uniqly (cell_1, cell_2), and inside this cells there is a button with accessibility identifier "my_button". In this case to access a button inside second cell you can't use AccessibilityById because there are two elements with this identifier on the screen. In this scenarios AccessibilityByXpath is helpfull. You can use following code to touch button inside second cell.
```
button_xPath = "XCUIElementTypeCell[contains(@label, 'cell_2')]/XCUIElementTypeButton" \
                                   "[contains(@label, 'my_button')]"
client.click_element(AccessibilityByXpath(button_xPath))
```
You can read more about accessibility [here](https://bitbar.com/blog/appium-tip-18-how-to-use-xpath-locators-efficiently/)
