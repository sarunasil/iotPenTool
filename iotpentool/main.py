

"""
IoT Penetration testing toolset
Startup file

By sarunasil
"""

import sys
import pickle
from os import path

from PyQt5.QtWidgets import QApplication

from iotpentool.configmanager import ConfigManager
from iotpentool.maingui import MainGui
from iotpentool.interfaceloader import InterfaceLoader
from iotpentool.threatmodel import ThreatModel
from iotpentool.utils import Outcome, Message, MsgType, PersistenceException
from iotpentool.manager import Manager

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
				return

		self.interface_loader = InterfaceLoader(self.config_manager.interface_dir)
		self.threat_model = self.create_threat_model()
		#DEV adds some predefined values to make testing easier

		self.main_gui = MainGui(self, self.interface_loader.interfaces, self.thread_manager, self.threat_model)
		self.main_gui.show()

	def create_threat_model(self):
		return ThreatModel(self.config_manager.architecture_site, self.config_manager.data_flow_site, self.config_manager.model_dir, DEV=True)

	def open_threat_model(self, file_path):
		#check file
		#deserialize?

		threat_model = None
		try:
			with open(file_path, 'rb') as binary_file:
				threat_model = pickle.load(binary_file)
		except (OSError, IOError, EOFError, pickle.UnpicklingError, pickle.PicklingError, pickle.PickleError) as e:
			raise PersistenceException(e)

		self.threat_model = threat_model
		return threat_model


	def save_threat_model(self, file_path, threat_model):
		#serialize file
		#if failure - exception

		try:
			with open(file_path, 'wb') as binary_file:
				pickle.dump(threat_model, binary_file)
		except (OSError, IOError, pickle.UnpicklingError, pickle.PicklingError, pickle.PickleError) as e:
			raise PersistenceException(e)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Main()
	sys.exit(app.exec_())


# gui load all data and not just the one that's enter by itself
