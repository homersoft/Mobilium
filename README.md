# Mobilium

Mobilium is an open source testing framework that allows to test iOS/iPadOS applications. Mobilium can be use independly, but also can be included into other testing framework as a replacement for Appium WebDriver.

## Motivation
We've build Mobilium as a Appium WebDriver replacement taking under the consideration Appium poor performance and many other Appium drawbacks.

## Requirments
- Xcode 11.4 [Apple](https://developer.apple.com/news/releases/?id=03032020f)
- Python3 [Installation instructions](https://docs.python-guide.org/starting/install3/osx/)
- Pip [How to install pip](https://pip.pypa.io/en/stable/installing/)
- Carthage [Get Carthage]()

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
- copy your app.ipa file into Mobilium dictionary
- write your first test:
```
client = MobiliumClient()
client.connect("719BB1CB-FCA2-4826-94AB-FEDC84BCE1AA", "192.168.1.7", 65432)
# simulator id, your server ip address, server port number
client.start_driver()
client.install_app("./app.ipa") #relative path to your app
client.launch_app("com.mobilium.demo") # bundle id of your app
```
- Save as `test.py` and run using: `python3 test.py`
After those step your app should be launched on the simulator
