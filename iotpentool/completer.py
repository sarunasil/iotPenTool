
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Takes values from ThreatModel fields and displays in InterfacesGui as field suggestions

By sarunasil
"""

import os
import re
from PyQt5.QtWidgets import QLineEdit, QWidget
from PyQt5.QtCore import QStringListModel

from iotpentool.interface import Interface, NESTED_SYMBOL
from iotpentool.utils import *


class Completer():
	'''Generates suggestions for interface value fields
	and
		populate interface gui QCompleters with those values
	'''

	def __init__(self, interfaces):
		'''Init
		'''

		self.interfaces = interfaces

	def generateSuggestions(self, threat):
		'''Generate new suggestions from ThreatModel fro specific threat

		Args:
			threat (Threat): threat to generate suggestions for
		'''

		for iden, interface in self.interfaces.items():

			#generate suggestions for interface flags
			for flag_iden, flag in interface.flags.items():
				flag.suggestions = self.scan_threat(threat, flag.keywords, flag.patterns)

			#generate suggestions for interface values
			for value_iden, value in interface.values.items():
				value.suggestions = self.scan_threat(threat, value.keywords, value.patterns)

	def scan_threat(self, threat, keywords, patterns):
		'''Scan Threat object for keyword accurances,
		iterate to lower object ref

		Args:
			threat (Threat): threat object to check
			keywords (set(String)): keywords to look for
			keywords (set(String)): regexes to look for

		Returns:
			list(String): found suggestions
		'''
		suggestions = set()

		text = threat.description.lower().replace('\n', ' ').replace('\n', ' ')
		suggestions |= self.look_for(text, keywords, patterns)

		text = threat.target.lower().replace('\n', ' ')
		suggestions |= self.look_for(text, keywords, patterns)

		text = threat.attack_tech.lower().replace('\n', ' ')
		suggestions |= self.look_for(text, keywords, patterns)

		text = threat.countermeasures.lower().replace('\n', ' ')
		suggestions |= self.look_for(text, keywords, patterns)

		suggestions |= self._scan_entry_point(threat.entry_point_used, keywords, patterns)
		suggestions |= self._scan_technologies(threat.technologies_used, keywords, patterns)

		return list(suggestions)

	def _scan_entry_point(self, entry_point, keywords, patterns):
		suggestions = set()

		text = entry_point.description.lower().replace('\n', ' ')
		suggestions |= self.look_for(text, keywords, patterns)

		suggestions |= self._scan_asset(entry_point.asset_used, keywords, patterns)

		return suggestions

	def _scan_asset(self, asset, keywords, patterns):
		suggestions = set()

		text = asset.description.lower().replace('\n', ' ')
		suggestions |= self.look_for(text, keywords, patterns)

		return suggestions

	def _scan_technologies(self, technologies, keywords, patterns):
		suggestions = set()

		for _, technology in technologies.items():
			text = technology.description.lower().replace('\n', ' ')
			suggestions |= self.look_for(text, keywords, patterns)

			#check all technology attributes
			for attrk, attrv in technology.attributes.items():
				attrk = attrk.lower().replace('\n', ' ')
				attrv = attrv.lower().replace('\n', ' ')
				#if attribute key in keywords - easy; just add value
				if attrk in keywords:
					suggestions.add(attrv)

				# if attribute value matches regex - just add it
				for regex in patterns:
					suggestions |= self.look_for_regex(attrv, regex)


		return suggestions

	def look_for(self, text, keywords, patterns):
		'''Look for keywords and patterns in given text

		Args:
			text (String):
			keywords (list(String)):
			patterns (list(String)):

		Returns:
			list(String):
		'''

		suggestions = set()
		for key in keywords:
			suggestions |= self.look_for_key(text, key)
		for regex in patterns:
			suggestions |= self.look_for_regex(text, regex)

		return suggestions

	def look_for_key(self, text, key, separator=' '):
		'''Look for keyword in text and return next word afterwards
		May be altered by 'options'

		Args:
			text (String): string to search
			key (String): string to search for
			separator (String), optional): word separator

		Returns:
			list(String): list of words after keyword
		'''

		results = set()
		index = 0
		while index != -1:
			index = text.find(key, index)
			if index == -1:
				continue

			index  = text.find(separator, index)
			if index == -1:
				continue

			index = index+len(separator)

			end_index = text.find(separator, index)
			if end_index == -1:
				results.add( text[index:] )
			else:
				results.add( text[index:end_index] )

		return results

	def look_for_regex(self, text, regex):
		'''Look for regex match in text and return if any

		Args:
			text (String): string to look search
			regex (String): regex to use

		Returns:
			list(String): word matching the regex
		'''

		result = set()
		for match in re.finditer(regex, text):
			result.add(match.group(0))

		return result


	def updateCompleters(self):
		'''Update QCompleter models of all interface gui's
		'''

		def process_flag(flag, interface):
			'''As flags can be recursive
			this process each flag in flag_widgets
			and if it has children - iterates into them as well
			DFS principle

			Args:
				flag (Flag): current flag which qcompleter is being updated
				interface (Interface): interface which flag belongs to
			'''

			#as flag_widgets are list() that's the only way of iteration
			widget = None
			for flag_widget in interface.gui_controller.flag_widgets:
				if flag_widget.objectName() == "flag_"+flag.iden:
					widget = flag_widget
					break
			if not widget:
				return

			lineedit = widget.findChild(QLineEdit)
			if not lineedit:
				return
			#update completer
			completer = lineedit.completer()
			completer.setModel( QStringListModel(flag.suggestions) )

			#recursive call to all flag children
			for _, flag_flag in flag.flag_flags.items():
				process_flag(flag_flag, interface)

		#go through every interface
		for _, interface in self.interfaces.items():
			#go through all interface flag objects
			for flag_iden, flag in interface.flags.items():
				process_flag(flag, interface)

			#reverse...
			#go through all value_widgets and find appropriate flag objects
			#for them to use flag.suggestions
			for widget in interface.gui_controller.value_widgets:
				value_widget = widget.findChild(QLineEdit)	#get qlineedit of this Value gui
				completer = value_widget.completer()		#get it's qcompleter

				value_iden = widget.objectName().replace('value_','',1)	#get Value identifier

				#use Value identifier to get Value object from interface and get it's 'suggestions' attribute
				completer.setModel( QStringListModel(interface.values[value_iden].suggestions) )

