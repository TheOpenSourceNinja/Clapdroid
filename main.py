#!/usr/bin/python3

__version__ = "0.1"

import kivy
kivy.require("1.9.0") #my current version as of 2015-07-21. Beware of using older versions.

from kivy.app import App
from kivy.uix.widget import Widget

class Clapboard(Widget):
	pass

class ClapdroidApp(App):
	def build(self):
		return Clapboard()

if __name__ == "__main__":
	ClapdroidApp().run()
