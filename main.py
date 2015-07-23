#!/usr/bin/python2

__version__ = "0.1" #The version of Clapdroid. Will stay at 0.1 until I decide on a version numbering scheme.

import six #I usually program in Python 3, but 3 isn't well supported yet by kivy/buildozer.

import kivy
kivy.require("1.9.0") #my current version as of 2015-07-21. Beware of using older versions.

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import time
import sys
import os

class fake():
	def exists(self):
		'''Tell the program this hardware doesn't exist.
		'''
		return False

#Possibly Android specific; we want the app to work on as many platforms as possible
try:
	from plyer import vibrator
except ImportError:
	vibrator = fake()

class Clapboard(Widget):
	def __init__(self, **kwargs):
		'''Initialize the clapboard.
			Args:
				**kwargs: Ignored by this class, passed to parent class.
		'''
		super(Clapboard, self).__init__(**kwargs)
		self.updateTime(dt = 0)
		Clock.schedule_interval(self.updateTime, 1.0)
		self.titleInput.bind( text=self.ensureTitleCase )
		self.clapButton.bind( on_press=self.clap )
		self.sound = SoundLoader.load('clap.ogg')
		self.sceneUpButton.bind( on_press=self.adjustByOne )
		self.sceneDownButton.bind( on_press=self.adjustByOne )
		self.shotUpButton.bind( on_press=self.adjustByOne )
		self.shotDownButton.bind( on_press=self.adjustByOne )
		self.takeUpButton.bind( on_press=self.adjustByOne )
		self.takeDownButton.bind( on_press=self.adjustByOne )
	
	def addNumber(self, old, new):
		'''Add a given number to another given number.
			Args:
				old: A string representing an integer.
				new: The number to add to old.
			Returns:
				A string representing the result of the addition.
		'''
		if not old.isdigit():
			old = "0"
		
		num = int( old ) + new
		if num < 0: #We only want positive integers
			num = 0
		
		return str( num )
	
	def adjustByOne(self, instance):
		'''Increment or decrement a number.
			Args:
				instance: The object which caused this function to be called.
		'''
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
		'''Produce simultaneous visual and audio output.
			Args:
				instance: (ignored) The object which caused this function to be called
		'''
		if self.sound:
			self.sound.play()
		if vibrator.exists():
			vibrator.vibrate(1) #Vibrate for one second
		# TODO: Find a way to flash the screen, activate the camera flash, or some other visual output aside from the button looking like it's being pressed.
	
	def ensureTitleCase(self, instance, value):
		'''Ensure that the movie title is title case.
			Args:
				instance: The object whose text content has just been changed
				value: (ignored) Text being inserted or otherwise modified. We ignore this because it may not contain all of instance's text.
		'''
		instance.text = instance.text.title()
	
	def updateTime(self, dt):
		'''Update the date label.
			Args:
				dt: According to Kivy's documentation, "the time elapsed between the scheduling and the calling of the callback" where this function is the callback. DT stands for Delta Time.
		'''
		self.dateLabel.text = time.strftime("%F %T")
	
	def saveData(self, theFile):
		'''Save data.
			Args:
				theFile: An already-open file into which to save the data.
		'''
		theFile.write( "title:" + self.titleInput.text + "\n" )
		theFile.write( "scene:" + self.sceneInput.text + "\n" )
		theFile.write( "shot:" + self.shotInput.text + "\n" )
		theFile.write( "take:" + self.takeInput.text + "\n" )
	
	def loadData(self, theFile):
		'''Load data.
			Args:
				theFile: An already-open file from which to load the data.
		'''
		for line in theFile:
			line = line.strip()
			data = line.partition(":")
			begin = data[0].strip().lower()
			if begin == "title":
				self.titleInput.text = data[2]
			elif begin == "scene":
				if data[2].isdigit():
					self.sceneInput.text = data[2]
			elif begin == "shot":
				if data[2].isdigit():
					self.shotInput.text = data[2]
			elif begin == "take":
				if data[2].isdigit():
					self.takeInput.text = data[2]

class ClapdroidApp(App):
	def __init__(self):
		super(ClapdroidApp, self).__init__()
		self.saveFilePath = self.user_data_dir + "/state"
	
	def build(self):
		'''Create whatever widgets the app needs to start. Other widgets may be created later.
		'''
		self.clapboard = Clapboard()
		return self.clapboard
	
	def saveData(self):
		'''Save data.
		'''
		try:
			if not os.path.exists( os.path.dirname( self.saveFilePath ) ):
				os.makedirs( os.path.dirname( self.saveFilePath ) )
		
			theFile = open( self.saveFilePath, "wt" )
			self.clapboard.saveData( theFile )
			theFile.close()
		except IOError, error:
			six.print_( "IOError caught in saveData():", error, file=sys.stderr )
	
	def loadData(self):
		'''Load data.
		'''
		try:
			if os.path.exists( self.saveFilePath ):
				theFile = open( self.saveFilePath, "rt" )
				self.clapboard.loadData( theFile )
				theFile.close()
		except IOError, error:
			six.print_( "IOError caught in loadData():", error, file=sys.stderr )
	
	def on_stop(self):
		'''When the program exits, save data.
		'''
		self.saveData()
		pass
	
	def on_start(self):
		'''When the program starts, load data.
		'''
		self.loadData()
		pass
	
	def on_pause(self):
		'''When execution is paused, save data - the program might be killed without calling on_resume().
		'''
		self.saveData()
		return True
	
	def on_resume(self):
		'''When execution is resumed (after being paused), load data.
		'''
		self.loadData()
		pass

if __name__ == "__main__":
	ClapdroidApp().run()
