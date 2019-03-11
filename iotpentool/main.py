

"""
IoT Penetration testing toolset
Startup file

By sarunasil
"""
import sys
from os import path

from PyQt5.QtWidgets import QApplication

from iotpentool.configmanager import ConfigManager
from iotpentool.maingui import MainGui
from iotpentool.interfaceloader import InterfaceLoader
from iotpentool.mymessage import Outcome, Message, MsgType

CURRENT_DIR = path.dirname(path.realpath(__file__))
CONFIG_FILE = path.join(CURRENT_DIR, "../data/config.ini")

class Main():
	'''Main class of the application
	Reads configuration file
	Starts InterfaceLoader
	Starts MainGUI
	'''

	def __init__(self):
		'''Init
		'''

		root_dir = path.join(CURRENT_DIR, "..")
		config_manager = ConfigManager(root_dir)

		result = config_manager.parse_config(CONFIG_FILE)
		if result == Outcome.FAILURE:
			result = config_manager.create_config(CONFIG_FILE)
			if result == Outcome.FAILURE:
				Message.print_message(MsgType.ERROR, "CAN'T READ OR RECREATE CONFIG FILE. ABORT.")
				return

		self.interface_loader = InterfaceLoader(config_manager.interface_dir)

		self.main_gui = MainGui(self.interface_loader.interfaces)
		self.main_gui.show()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Main()
	sys.exit(app.exec_())
