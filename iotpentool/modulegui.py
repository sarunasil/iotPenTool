#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class to deal with Module interface generation and data
Abstracts gui details from Interface

By sarunasil
"""

import os
from PyQt5 import QtWidgets



class ModuleGui(QtWidgets.QWidget):
    '''Deals with module gui which is generated from Interface data
    '''

    def __init__(self, interface):
        '''Init
        '''
        super().__init__()
        self.interface = interface

        self.style = ""#TODO
        if self.style:
            self.setStyleSheet(self.style)

        self.setObjectName("widget_interface")
        layout = QtWidgets.QVBoxLayout()

        general = ModuleGui._create_general(interface)
        layout.addWidget(general)

        flags = ModuleGui._create_flags(interface.flags)
        # flags.setStyleSheet("background-color:grey;")
        layout.addWidget(flags)

        values = ModuleGui._create_values(interface.values)
        # values.setStyleSheet("background-color:brown;")
        layout.addWidget(values)

        self.setLayout(layout)

        #TODO _create_footer

    @staticmethod
    def _create_label(object_name, text, style=None):
        '''Create a QLabel object, set it's style

        Args:
            text (String): text to print
            style (String, optional): Defaults to None. Provide a StyleSheet if needed

        Returns:
            QLabel: label to display

        TODO set a custom default style sheet (when no 'style' is provided)
        '''

        label = QtWidgets.QLabel(text)
        label.setObjectName("label_"+object_name)

        if style:
            label.setStyleSheet(style)

        return label

    @staticmethod
    def _create_flag(flag, style=None):
        '''creates a widget representing a tool Flag

        Args:
            flag (_Flag): flag to create gui for
            style (String, optional): Default ot None. Provide a StyleSheet if needed

        Returns:
            QWidget:
        '''

        widget = QtWidgets.QWidget()
        widget.setObjectName("flag_"+flag.iden)
        layout = QtWidgets.QHBoxLayout()

        check_box = QtWidgets.QCheckBox(flag.flag + " - " + flag.iden)
        check_box.setObjectName("check_box_" + flag.iden)
        layout.addWidget(check_box)

        if flag.has_value:
            text_box = QtWidgets.QLineEdit()
            text_box.setObjectName("text_box_"+flag.iden)
            layout.addWidget(text_box)

        widget.setLayout(layout)
        widget.setToolTip(flag.description)

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

        label = QtWidgets.QLabel(value.iden)
        label.setObjectName("label_"+value.iden)
        layout.addWidget(label)

        text_box = QtWidgets.QLineEdit()
        text_box.setObjectName("text_box_"+value.iden)
        layout.addWidget(text_box)

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

        name_lbl = ModuleGui._create_label("name", interface.name, style)
        layout.addWidget(name_lbl)

        version_lbl = ModuleGui._create_label("version", interface.version, style)
        layout.addWidget(version_lbl)

        command_lbl = ModuleGui._create_label("command", interface.command, style)
        layout.addWidget(command_lbl)

        widget.setLayout(layout)

        return widget

    @staticmethod
    def _create_flags(flags):
        '''Generates flag part of the module tab, defines style for it's children

        Args:
            flags (dict(Flag)): module flags

        Returns:
            QWidget: flags part of the module tab
        '''

        style = ""#TODO

        widget = QtWidgets.QWidget()
        widget.setObjectName("widget_flags")
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        for flag in flags:
            temp_flag = ModuleGui._create_flag(flags[flag], style)
            layout.addWidget(temp_flag)



        return widget

    @staticmethod
    def _create_values(values):
        '''Generates values part of the module tab, defines style for it's children

        Args:
            values (dict(_Value)): module values

        Returns:
            QWidget: values part of the module tab
        '''

        style = ""#TODO

        widget = QtWidgets.QWidget()
        widget.setObjectName("widget_values")
        layout = QtWidgets.QVBoxLayout()

        for value in values:
            temp_value = ModuleGui._create_value(values[value], style)
            layout.addWidget(temp_value)


        widget.setLayout(layout)

        return widget