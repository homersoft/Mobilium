## Prepare
It is good to have prepared virtual environment for server i.e. in PyCharm, and run
all commends inside them.

## Initialize
To initialize all requirements, simply run command below:
```
pip install .
```
MobiliumServer uses `ideviceinstaller` in order to install application on a device. You can get it via brew.
```
brew install ideviceinstaller
```
If you haven't installed brew yet you can do that using command below:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
## Run
Use command below to start server with given address:
```
mobilium-server -a SERVER-IP-ADDRESS
```
