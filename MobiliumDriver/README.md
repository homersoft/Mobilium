## Prepare
You need to have Xcode and Carthage installed on machine.

## Initialize
To initialize all requirements, simply run command below:
```
carthage update --platform iOS --cache-builds --use-ssh
```

## Run
MobiliumDriver should be started by MobiliumServer. If you want to start it manually, run command below:
```
xcodebuild -project MobiliumDriver.xcodeproj \
    -scheme MobiliumDriver \
    -destination "id=UDID_OF_YOUR_CONNECTED_DEVICE" \
    HOST=MOBILIUM_SERVER_HOST \
    PORT=MOBILIUM_SERVER_PORT \
    test
```
* **UDID_OF_YOUR_CONNECTED_DEVICE** - UDID of device you want to run test on
* **MOBILIUM_SERVER_HOST** - IP Address of Mobilium Server
* **MOBILIUM_SERVER_PORT** - Port of Mobilium Server, default is 65432
