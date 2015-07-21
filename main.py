#!/usr/bin/python3

__version__ = "0.1"

import kivy
kivy.require("1.9.0") #my current version as of 2015-07-21. Beware of using older versions.

from kivy.app import App
from kivy.uix.button import Label

class ClapDroid(App):
	def build(self):
		return Label(text="Clap!")

if __name__ == "__main__":
	ClapDroid().run()
