# Mobilium

Mobilium is an open-source testing framework that allows testing iOS/iPadOS applications. Mobilium can be used independently, but also can be included in other testing frameworks as a replacement for Appium WebDriver.

## Motivation
While Appium is build as unified UI testing framework for all possible platforms it's handy but have some drawbacks.
E.g. Appium is building XML representation of current application UI elements, and then allows to interact with those elements.
This leads to performance issues, issues with finding some UI elements, or other issues connected with that this structure is not always accurred.
Mobilium under the hood is ussing Xcode UITest framework, which should answer for issues laying under the unified frameworks architecture.

Check [architecture documentation](Architecture.md) for more details.

## Requirments
- Xcode 11.4 [Apple](https://developer.apple.com/news/releases/?id=03032020f)
- Python3 [Installation instructions](https://docs.python-guide.org/starting/install3/osx/)
- Pip [How to install pip](https://pip.pypa.io/en/stable/installing/)
- Carthage [Get Carthage](https://github.com/Carthage/Carthage)

NOTE:
```
Right now Mobilium can be used only with reali iOS/iPadOS devices. Sumulators are not supported!
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
- obtain desired device id using `instruments -s devices`
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
After those step, your app should be launched on your device.

## Available actions
All Mobilium client actions are listed and described [here](https://github.com/homersoft/Mobilium/blob/master/MobiliumClient/README.md)

## Permissions handling
Mobilium source code has added an interruption handler so all permission requests are handled automatically

## Running Mobilium on real devices

Because of apple requirements to run an Xcode project on the device you have to set correct provisioning profile inside MobiliumDriver project.
- Open MobiliumDriver.xcodeproj
- Open MobiliumDrvier project details
- Open Signing and capabilities tab
- Under iOS Platform select the correct provisioning profile to which your device has been assigned.
- Select MobiliumDriver target and your connected device in Xcode and run tests (Product -> Test) or `command + U`

## Example
Check [demo](demo) directory to see example Xcode project and UI tests written in Mobilium.

## Know issues
- As apple not allows to setup accessibility identifiers to UIAlertController titles and buttons Mobilium doesn't support system alerts
- Mobilium doesn't support testing on iOS simulators
-
## Licence
Mobilium is distributed under MIT license. You can check more [here](LICENSE.md)
