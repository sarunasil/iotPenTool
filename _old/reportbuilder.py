#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
creating html report from ThreatModel provided

By sarunasil
"""

import os
from yattag import Doc, indent

from iotpentool.threatmodel import ThreatModel



import pickle
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PICKLE = os.path.join(CURRENT_DIR, "../testas.pickle")


class ReportBuilder():
	'''Creates html report
	'''


	def __init__(self):
		'''Init
		'''

		threat_model = None
		try:
			with open(PICKLE, 'rb') as binary_file:
				threat_model = pickle.load(binary_file)
				print (threat_model)
		except (OSError, IOError, EOFError, pickle.UnpicklingError, pickle.PicklingError, pickle.PickleError) as e:
			print ("BLET")

		with open("report.html", 'w') as report_file:
			report_file.write(self.func(threat_model))

	def func(self, threat_model):
		doc, tag, text, line = Doc().ttl()

		doc.asis("<!DOCTYPE html>")
		with tag('html', lang='en'):
			with tag('head'):
				line('title','Threat Model report')
				doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
				doc.asis('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">')
				doc.asis('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>')
				doc.asis('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>')

			with tag('body'):
				with tag('div', klass='container'):
					line('h2', 'Threat model')
					line('h2', threat_model.save_file)
					line('h2', 'Report')

					#Assets
					#table: Asset name | Description

					#Architecture
						#Architectural Diagram
						#link to diagram

						#Technologies
						#table: Technology name | Description | Attribute key - value | 
						#						|			  | Attribute key - value |

					#Decomposition
						#Data flow diagram
						#Entry points

					#Threats
		result = indent(doc.getvalue())

		return result

if __name__ == "__main__":
	ReportBuilder()
