#!/usr/bin/python3
__version__ = "0.1"

import kivy
kivy.require("1.9.0") #my current version as of 2015-07-21. Beware of using older versions.

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

import time

class Clapboard(Widget):
	def __init__(self, **kwargs):
		super(Clapboard, self).__init__(**kwargs)
		self.updateTime(dt = 0)
		Clock.schedule_interval(self.updateTime, 1.0)
		self.titleInput.bind( text=self.ensureTitleCase )
	
	def ensureTitleCase(self, instance, value):
		instance.text = instance.text.title()
	
	def updateTime(self, dt):
		'''Update the date label.
			Args:
				dt: According to Kivy's documentation, "the time elapsed between the scheduling and the calling of the callback" where this function is the callback. DT stands for Delta Time.
		'''
		self.dateLabel.text = time.strftime("%F %T")

class ClapdroidApp(App):
	def build(self):
		return Clapboard()

if __name__ == "__main__":
	ClapdroidApp().run()
