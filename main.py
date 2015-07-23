#!/usr/bin/python2
#Note: I usually program in Python 3, but 3 isn't well supported yet by kivy/buildozer.
__version__ = "0.1" #The version of Clapdroid. Will stay at 0.1 until I decide on a versin numbering scheme.

import six

import kivy
kivy.require("1.9.0") #my current version as of 2015-07-21. Beware of using older versions.

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
import time
import sys

class fake():
	def exists(self):
		return false

#Possibly Android specific; we want the app to work on as many platforms as possible
try:
	from plyer import vibrator
except ImportError:
	vibrator = fake()

class Clapboard(Widget):
	def __init__(self, **kwargs):
		super(Clapboard, self).__init__(**kwargs)
		self.updateTime(dt = 0)
		Clock.schedule_interval(self.updateTime, 1.0)
		self.titleInput.bind( text=self.ensureTitleCase )
		self.clapButton.bind( on_press=self.clap )
		self.sound = SoundLoader.load('clap.ogg')
		self.sceneUpButton.bind( on_press=self.increment )
		self.sceneDownButton.bind( on_press=self.increment )
		self.shotUpButton.bind( on_press=self.increment )
		self.shotDownButton.bind( on_press=self.increment )
		self.takeUpButton.bind( on_press=self.increment )
		self.takeDownButton.bind( on_press=self.increment )
	
	def addNumber(self, old, new):
		if not old.isdigit():
			old = "0"
		
		num = int( old ) + new
		if( num < 0 ):
			num = 0
		
		return str( num )
	
	def increment(self, instance):
		if instance == self.sceneUpButton:
			self.sceneInput.text = self.addNumber( self.sceneInput.text, 1 )
		elif instance == self.sceneDownButton:
			self.sceneInput.text = self.addNumber( self.sceneInput.text, -1 )
		elif instance == self.shotUpButton:
			self.shotInput.text = self.addNumber( self.shotInput.text, 1 )
		elif instance == self.shotDownButton:
			self.shotInput.text = self.addNumber( self.shotInput.text, -1 )
		elif instance == self.takeUpButton:
			self.takeInput.text = self.addNumber( self.takeInput.text, 1 )
		elif instance == self.takeDownButton:
			self.takeInput.text = self.addNumber( self.takeInput.text, -1 )
	
	def clap(self, instance):
		#six.print_("Clapping!")
		if self.sound:
			#six.print_( "test", file=sys.stderr )
			#six.print_( self.sound, file=sys.stderr )
			#six.print_( "Sound found at", self.sound.source, file=sys.stderr )
			#six.print_( "Sound is %.3f seconds" % self.sound.length, file=sys.stderr )
			self.sound.play()
		if vibrator.exists():
			vibrator.vibrate(1)
	
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
	
	def on_stop(self):
		#TODO: Save important data here
		pass
	
	def on_start(self):
		#TODO: Load important data here
		pass
	
	def on_pause(self):
		#TODO: Save important data here
		return True
	
	def on_resume(self):
		#TODO: Load important data here
		pass

if __name__ == "__main__":
	ClapdroidApp().run()
