#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class to deal with Module interface generation and data
Abstracts gui details from Interface

By sarunasil
"""

import uuid
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from iotpentool.line import QHLine


class ModuleGui(QtWidgets.QWidget):
    '''Deals with module gui which is generated from Interface data
    '''

    def __init__(self, controller):
        '''Init
        '''
        super().__init__()
        self.style = ""#TODO
        self.controller = controller

        self.initUI()

    # def print_general_size(self):
    #     self.btns[0].setText(
    #         "Actual: "+str(self.flags.size().height()) + "\n Hint: " + str(self.flags.sizeHint().height())
    #         )

    def initUI(self):
        '''Function to move GUI creation from __init__
        '''

        if self.style:
            self.setStyleSheet(self.style)

        self.setObjectName("widget_interface")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        general = ModuleGui._create_general(self.controller.interface)
        layout.addWidget(general)

        flags = ModuleGui._create_flags(self.controller.interface.flags, self.controller.flag_widgets)
        # flags.setStyleSheet("background-color:grey;")
        layout.addWidget(flags)

        values = ModuleGui._create_values(self.controller.interface.values, self.controller.value_widgets)
        # values.setStyleSheet("background-color:brown;")
        layout.addWidget(values)

        layout.addStretch(1)

        footer = ModuleGui._create_footer(self.controller.btns)
        layout.addWidget(footer)
        self.updateGeometry()

        self.setLayout(layout)

    @staticmethod
    def _create_label(label, object_name, text, wrap, style=None):
        '''Create a QLabel object, set it's style

        Args:
            label (String): label of the value
            text (String): text to print
            wrap (Boolean): wrap text or not
            style (String, optional): Defaults to None. Provide a StyleSheet if needed

        Returns:
            QWidget: label qwidget to display

        TODO set a custom default style sheet (when no 'style' is provided)
        '''

        widget = QtWidgets.QWidget()
        widget.setObjectName("label_"+object_name)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(1,0,1,1)
        layout.setSpacing(0)


        qlabel = QtWidgets.QLabel(label)
        qlabel.setObjectName("label_"+label)
        layout.addWidget(qlabel)

        if wrap:
            scroll = QtWidgets.QScrollArea()
            scroll.setMaximumHeight(200)
            scroll.setObjectName("label_scroll_"+object_name)

            value = QtWidgets.QLabel(text)
            value.setWordWrap(True)
            value.setObjectName("label_value_"+object_name)
            scroll.setWidget(value)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            scroll.setSizePolicy(sizePolicy)


            scroll.setWidgetResizable(True)
            layout.addWidget(scroll)
        else:
            value = QtWidgets.QLabel(text)
            value.setWordWrap(True)
            value.setObjectName("label_value_"+object_name)
            layout.addWidget(value)

        widget.setLayout(layout)

        if style:
            widget.setStyleSheet(style)

        return widget

    @staticmethod
    def _create_flag(flag, flag_widgets, style=None):
        '''creates a widget representing a tool Flag

        Args:
            flag (_Flag): flag to create gui for
            style (String, optional): Default ot None. Provide a StyleSheet if needed
            flag_widgets (list(QWidget)): reference to the ModuleGui self.flag_widgets list

        Returns:
            QWidget:
        '''

        widget = QtWidgets.QWidget()
        widget.setObjectName("flag_"+flag.iden)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(2,2,2,2)
        layout.setSpacing(2)

        widget_top = QtWidgets.QWidget()
        widget_top.setObjectName("widget_top_"+flag.iden)
        layout_top = QtWidgets.QHBoxLayout()
        check_box = QtWidgets.QCheckBox(flag.flag)
        check_box.setObjectName("check_box_" + flag.iden)
        layout_top.addWidget(check_box)

        if flag.has_value:
            text_box = QtWidgets.QLineEdit()
            text_box.setObjectName("text_box_"+flag.iden)
            layout_top.addWidget(text_box)
        else:
            layout_top.addSpacing(50)
            # pass

        desc_lbl = QtWidgets.QLabel(flag.description)
        desc_lbl.setObjectName("label_"+flag.iden)
        desc_lbl.setWordWrap(True)
        layout_top.addWidget(desc_lbl)
        layout_top.addStretch(1)

        widget_top.setLayout(layout_top)
        layout.addWidget(widget_top)
        #nested flag
        for flag_iden, flag_flag in flag.flag_flags.items():
            nested_flag = ModuleGui._create_flag(flag_flag, flag_widgets, style)
            nested_flag.layout().setContentsMargins(20,0,0,0) #make indentation

            # Add to modulegui flag widgets list to access value later
            flag_widgets.append(nested_flag)
            layout.addWidget(nested_flag)

        layout.addStretch(1)

        widget.setLayout(layout)
        widget.setToolTip(flag.iden)

        if style:
            widget.setStyleSheet(style)

        return widget

    @staticmethod
    def _create_value(value, style=None):
        '''creates a widget representing a tool value

        Args:
            value (_Value): flag to create gui for
            style (String, optional): Default ot None. Provide a StyleSheet if needed

        Returns:
            QWidget:
        '''

        widget = QtWidgets.QWidget()
        widget.setObjectName("value_"+value.iden)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(2,2,2,2)
        layout.setSpacing(10)

        text_box = QtWidgets.QLineEdit()
        text_box.setObjectName("text_box_"+value.iden)
        layout.addWidget(text_box, 2)

        label = QtWidgets.QLabel(value.iden)
        label.setObjectName("label_"+value.iden)
        layout.addWidget(label, 2)

        desc_lbl = QtWidgets.QLabel(value.description)
        desc_lbl.setObjectName("label_desc_"+value.iden)
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl, 20)

        widget.setLayout(layout)
        widget.setToolTip(value.description)

        if style:
            widget.setStyleSheet(style)

        return widget

    @staticmethod
    def _create_general(interface):
        '''Generates the general information part of the module tab, defines style for it's children

        Args:
            interface (Interface): interface which info needs to be presented

        Returns:
            QWidget: part of the general tab
        '''

        style = ""#TODO

        widget = QtWidgets.QWidget()
        widget.setObjectName("widget_general")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,2)
        layout.setSpacing(0)


        widget_top = QtWidgets.QWidget()
        widget_top.setObjectName("widget_general_top")
        layout_top = QtWidgets.QHBoxLayout()
        layout_top.setContentsMargins(0,0,0,0)
        layout_top.setSpacing(0)
        widget_top.setLayout(layout_top)

        name_lbl = ModuleGui._create_label("Module name:", "name", interface.name, False, style)
        layout_top.addWidget(name_lbl)

        version_lbl = ModuleGui._create_label("Version:", "version", interface.version, False, style)
        layout_top.addWidget(version_lbl)

        command_lbl = ModuleGui._create_label("Command:", "command", interface.command, False, style)
        layout_top.addWidget(command_lbl)

        layout.addWidget(widget_top)


        description_lbl = ModuleGui._create_label("Description:", "description", interface.description, True, style)
        layout.addWidget(description_lbl)
        # layout.addStretch(1)

        widget.setLayout(layout)

        return widget

    @staticmethod
    def _create_flags(flags, flag_widgets):
        '''Generates flag part of the module tab, defines style for it's children

        Args:
            flags (dict(Flag)): module flags
            flag_widgets (list(QWidget)): reference to the ModuleGui self.flag_widgets list

        Returns:
            QWidget: flags part of the module tab
        '''

        style = ""#TODO

        widget = QtWidgets.QWidget()
        widget.setObjectName("widget_flags")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,5)
        layout.setSpacing(2)

        section_txt = "   Module flags:"
        section_name_lbl = QtWidgets.QLabel(section_txt)
        layout.addWidget(section_name_lbl)

        scroll = QtWidgets.QScrollArea()
        # scroll.setMaximumHeight(200)
        scroll.setMinimumHeight(50)
        scroll.setWidgetResizable(True)
        scroll_w = QtWidgets.QWidget()
        scroll_w_layout = QtWidgets.QVBoxLayout()
        scroll_w_layout.setContentsMargins(2,0,0,1)
        scroll_w_layout.setSpacing(2)

        header_txt = "   ---- Flag -------- [Value] -------- Description ----"
        header_lbl = QtWidgets.QLabel(header_txt)
        scroll_w_layout.addWidget(header_lbl)
        for flag in flags:
            position = len(flag_widgets)
            temp_flag = ModuleGui._create_flag(flags[flag], flag_widgets, style)

            # Add to modulegui flag widgets list to access value later
            flag_widgets.insert(position, temp_flag)

            scroll_w_layout.addWidget(temp_flag)

        scroll_w_layout.addStretch(1)
        scroll_w.setLayout(scroll_w_layout)
        scroll.setWidget(scroll_w)


        layout.addWidget(scroll)
        layout.addStretch(1)

        widget.setLayout(layout)

        return widget

    @staticmethod
    def _create_values(values, value_widgets):
        '''Generates values part of the module tab, defines style for it's children

        Args:
            values (dict(_Value)): module values
            value_widgets (list(QWidget)): reference to the ModuleGui self.value_widgets

        Returns:
            QWidget: values part of the module tab
        '''

        style = ""#TODO

        widget = QtWidgets.QWidget()
        widget.setObjectName("widget_values")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,5)
        layout.setSpacing(2)


        section_txt = "   Module values:"
        section_name_lbl = QtWidgets.QLabel(section_txt)
        layout.addWidget(section_name_lbl)

        scroll = QtWidgets.QScrollArea()
        # scroll.setMaximumHeight(200)
        scroll.setMinimumHeight(50)
        scroll.setWidgetResizable(True)
        scroll_w = QtWidgets.QWidget()
        scroll_w_layout = QtWidgets.QVBoxLayout()
        scroll_w_layout.setContentsMargins(2,0,0,1)
        scroll_w_layout.setSpacing(2)

        header_txt = "   ---- Value -------- Value Name -------- Description ----"
        header_lbl = QtWidgets.QLabel(header_txt)
        scroll_w_layout.addWidget(header_lbl)
        for value in values:
            temp_value = ModuleGui._create_value(values[value], style)

            # Add to modulegui value widgets list to access value later
            value_widgets.append(temp_value)

            scroll_w_layout.addWidget(temp_value)
        scroll_w_layout.addStretch(1)
        scroll_w.setLayout(scroll_w_layout)
        scroll.setWidget(scroll_w)


        layout.addWidget(scroll)
        layout.addStretch(1)


        widget.setLayout(layout)

        return widget

    @staticmethod
    def _create_footer(btns_ref):
        '''Creates module tab footer section

        Args:
            btns_ref (list(QPushButton)): buttons list of reference

        Returns:
            QWidget: footer section
        '''

        style = ""#TODO

        widget = QtWidgets.QWidget()
        widget.setObjectName("widget_footer")
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0,0,0,2)
        layout.setSpacing(0)

        layout.addStretch(1)

        # execute button
        exe_text = "Run module"
        btn_exe = QtWidgets.QPushButton(exe_text)
        btn_exe.setObjectName("btn_execute")
        btns_ref.append(btn_exe)
        layout.addWidget(btn_exe)

        layout.addStretch(1)

        # terminate button
        exe_text = "Terminate run"
        btn_term = QtWidgets.QPushButton(exe_text)
        btn_term.setObjectName("btn_terminate")
        btns_ref.append(btn_term)
        layout.addWidget(btn_term)

        layout.addStretch(1)

        widget.setLayout(layout)

        return widget


class ModuleGuiController():
    '''ModuleGui action controller
    '''
    def __init__(self, interface, manager):
        '''Init

        Args:
            modulegui (ModuleGui): callbac to ModuleGui
        '''
        self.interface = interface
        self.flag_widgets = []
        self.value_widgets = []
        self.btns = []

        self.manager = manager #class reference to deal with multithreading

        self.execution_id = None
        self.modulegui = ModuleGui(self)

        self.btns[0].pressed.connect(self.execute_action)
        self.btns[1].pressed.connect(self.terminate_action)

    def gather_params(self):
        '''Gathers flag and value states from text fields and checkboxes in the gui

        Returns:
            dict(String: [String|None] ), dict(String: String ): 2 values: ACTUALLY... Does are lists now. USE ORDEREDDICT !!!
            - dict of checked flags (with values if hasValue==True) f:value
            - dict of checked values with values    value_name:value
        '''
        #HACKI HACK HACKI HACK .... use list instead of dict to 
        #maintain orer - thus nested flags will always go after parent flags...
        #gather states of checked flags
        flags = []
        for flag_widget in self.flag_widgets:
            checkbox = flag_widget.findChild(QtWidgets.QCheckBox)
            if checkbox.isChecked():
                flag_iden = flag_widget.objectName().replace('flag_','',1)

                textbox = flag_widget.findChild(QtWidgets.QLineEdit)
                if textbox:
                    flags.append((flag_iden, textbox.text()))
                else:
                    flags.append((flag_iden, None))

        #gather states of values
        #so most likely, all the values as all of them have to have default values
        values = []
        for value_widget in self.value_widgets:
            value_iden = value_widget.objectName().replace('value_','',1)

            textbox = value_widget.findChild(QtWidgets.QLineEdit)
            values.append((value_iden, textbox.text()))

        return flags, values

    def execute_action(self):
        '''Execute button action:
            gather interface command arguments,
            build command string in Interface
            call manager to run command and deal with output
        '''

        flags, values = self.gather_params()
        iden = self.interface.command
        command_string = self.interface.build_command(flags, values)
        self.execution_id = str(uuid.uuid4())

        self.manager.run_executor(iden, self.execution_id, command_string)

    def terminate_action(self):
        '''Terminate button action:
            terminates a running process 
        '''
        if self.execution_id:
            self.manager.terminate_executor(self.execution_id)
            self.execution_id = None

