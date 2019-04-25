

"""
IoT Penetration testing toolset
Startup file

By sarunasil
"""

import sys
import pickle
from ruamel import yaml
import jsonpickle
from os import path

from PyQt5.QtWidgets import QApplication

from iotpentool.configmanager import ConfigManager
from iotpentool.maingui import MainGui
from iotpentool.interfaceloader import InterfaceLoader
from iotpentool.threatmodel import ThreatModel
from iotpentool.utils import Outcome, Message, MsgType, PersistenceException
from iotpentool.manager import Manager
from iotpentool.completer import Completer

CURRENT_DIR = path.dirname(path.realpath(__file__))
CONFIG_FILE = path.join(CURRENT_DIR, "../data/config.ini")

class Main():
	'''Main class of the application
	Reads configuration file
	Starts InterfaceLoader
	Starts ThreatModel
	Starts MainGUI
	'''

	def __init__(self):
		'''Init
		'''

		self.root_dir = path.join(CURRENT_DIR, "..")
		self.config_manager = ConfigManager(self.root_dir)

		self.thread_manager = Manager()

		result = self.config_manager.parse_config(CONFIG_FILE)
		if result == Outcome.FAILURE:
			result = self.config_manager.create_config(CONFIG_FILE)
			if result == Outcome.FAILURE:
				Message.print_message(MsgType.ERROR, "CAN'T READ OR RECREATE CONFIG FILE. ABORT.")
				input("Press any key...")
				return

		self.interface_loader = InterfaceLoader(self.config_manager.interface_dir)
		self.threat_model = self.create_threat_model()

		self.completer = Completer(self.interface_loader.interfaces)

		self.main_gui = MainGui(self, self.interface_loader.interfaces, self.thread_manager, self.completer, self.threat_model)
		self.main_gui.show()

	def create_threat_model(self):
		'''Open new threat model object

		Returns:
			ThreatModel: new threat model object
		'''

		return ThreatModel(self.config_manager.architecture_site, self.config_manager.data_flow_site, self.config_manager.model_dir) #DEV=True

	def open_threat_model(self, file_path):
		'''Open threat saved as Python serialized (.pickle) object

		Args:
			file_path (String): file to open

		Raises:
			PersistenceException: Exception to throw if error - generalizes error type

		Returns:
			ThreatModel: deseraliazed threat model object
		'''

		threat_model = None
		try:
			with open(file_path, 'rb') as binary_file:
				threat_model = pickle.load(binary_file)
		except (OSError, IOError, EOFError, pickle.UnpicklingError, pickle.PicklingError, pickle.PickleError) as e:
			raise PersistenceException(e)

		self.threat_model = threat_model
		return threat_model


	def save_threat_model(self, file_path, threat_model):
		'''Saves given ThreatModel object as python serialized file (.pickle)

		Args:
			file_path (String): file_path to save new file
			threat_model (ThreatModel): object to save

		Raises:
			PersistenceException: Exception to throw if error (generalises exact exceptions)
		'''

		try:
			with open(file_path, 'wb') as binary_file:
				pickle.dump(threat_model, binary_file)
		except (OSError, IOError, pickle.UnpicklingError, pickle.PicklingError, pickle.PickleError) as e:
			raise PersistenceException(e)

	def export_json(self, file_path, threat_model):
		'''Export current threat model to json

		Args:
			file_path (String): file path to save to
			threat_model (ThreatModel): current threat model instance

		Raises:
			PersistenceException: Exception to throw if error (generalises exact exceptions)
		'''

		with open(file_path, 'w') as stream:
			try:
				jsonpickle.set_encoder_options('simplejson', indent=4)
				jsonpickle.set_encoder_options('json', indent=4)
				jsonpickle.set_encoder_options('demjson', indent=4)
				json_object = jsonpickle.encode(threat_model, unpicklable=False)
				stream.write(json_object)
			except Exception as e:
				raise PersistenceException(e)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Main()
	sys.exit(app.exec_())

