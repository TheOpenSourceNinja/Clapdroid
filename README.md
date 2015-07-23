# Clapdroid
A digital clapboard (a.k.a. sync slate) app for mobile devices (not limited to Android)

# Prerequisites
* [Python 2](https://www.python.org/)
* [Buildozer](https://github.com/kivy/buildozer) (for building the Android and iOS apps)
Buildozer will automatically download the following required software.
* [Six](https://pythonhosted.org/six/)
* [Kivy](http://kivy.org)
* [Android SDK](https://developer.android.com/sdk/index.html) (only needed if building for Android)

# To build and run
## for Android:
### To build:
In a terminal, cd to the Clapdroid directory and run the command `buildozer android debug`
### To run:
1. Connect an Android device or start an Android emulator.
2. Ensure the device or emulator has USB debugging enabled.
3. In a terminal, cd to the Clapdroid directory and run the command `buildozer android deploy run`
### To build and run at the same time:
Simply combine the above commands: `buildozer android debug deploy run`
## for iOS:
I don't know; try the same commands as for Android, replacing `android` with `ios`
## for Linux:
### To build:
On Linux there is no need to build a package, just make sure you have all of the prerequisites.
### To run:
Just run main.py in the Clapdroid directory, either by double-clicking on it or (in a terminal) cd'ing to the directory and running `./main.py`
## for Windows:
See the Linux instructions
## for Mac OS X:
See the Linux instructions
