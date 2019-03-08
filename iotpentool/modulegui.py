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
from PyQt5.QtCore import Qt

from iotpentool.line import QHLine


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
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        general = ModuleGui._create_general(interface)
        layout.addWidget(general)

        flags = ModuleGui._create_flags(interface.flags)
        # flags.setStyleSheet("background-color:grey;")
        layout.addWidget(flags, 1)

        values = ModuleGui._create_values(interface.values)
        # values.setStyleSheet("background-color:brown;")
        layout.addWidget(values, 1)

        footer = ModuleGui._create_footer()
        layout.addWidget(footer)

        # layout.addStretch(1)

        self.setLayout(layout)

        #TODO _create_footer

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
            scroll.setMaximumHeight(100)
            scroll.setObjectName("label_scroll_"+object_name)

            value = QtWidgets.QLabel(text)
            value.setWordWrap(True)
            value.setObjectName("label_value_"+object_name)
            scroll.setWidget(value)


            layout.addWidget(scroll)
        else:
            value = QtWidgets.QLabel(text)
            value.setObjectName("label_value_"+object_name)
            layout.addWidget(value)

        widget.setLayout(layout)

        if style:
            widget.setStyleSheet(style)

        return widget

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
        layout.setContentsMargins(2,2,2,2)
        layout.setSpacing(2)

        check_box = QtWidgets.QCheckBox(flag.flag)
        check_box.setObjectName("check_box_" + flag.iden)
        layout.addWidget(check_box, 1)

        if flag.has_value:
            text_box = QtWidgets.QLineEdit()
            text_box.setObjectName("text_box_"+flag.iden)
            layout.addWidget(text_box, 3)
        else:
            layout.addStretch(3)

        desc_lbl = QtWidgets.QLabel(flag.description)
        desc_lbl.setObjectName("label_"+flag.iden)
        desc_lbl.setWordWrap(True)
        layout.addWidget(desc_lbl, 20)

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
        layout.setSpacing(2)

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
        layout.setContentsMargins(0,0,0,5)
        layout.setSpacing(2)

        section_txt = "   Module flags:"
        section_name_lbl = QtWidgets.QLabel(section_txt)
        layout.addWidget(section_name_lbl)

        scroll = QtWidgets.QScrollArea()
        # scroll.setMaximumHeight(200)
        scroll.setMinimumHeight(100)
        scroll_w = QtWidgets.QWidget()
        scroll_w_layout = QtWidgets.QVBoxLayout()
        scroll_w_layout.setContentsMargins(2,0,0,1)
        scroll_w_layout.setSpacing(2)

        header_txt = "   Flag \t | \t Value \t | \t Description"
        header_lbl = QtWidgets.QLabel(header_txt)
        scroll_w_layout.addWidget(header_lbl)
        for flag in flags:
            temp_flag = ModuleGui._create_flag(flags[flag], style)
            scroll_w_layout.addWidget(temp_flag)

        scroll_w.setLayout(scroll_w_layout)
        scroll.setWidget(scroll_w)


        layout.addWidget(scroll)

        widget.setLayout(layout)

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
        layout.setContentsMargins(0,0,0,5)
        layout.setSpacing(2)


        section_txt = "   Module values:"
        section_name_lbl = QtWidgets.QLabel(section_txt)
        layout.addWidget(section_name_lbl)

        scroll = QtWidgets.QScrollArea()
        # scroll.setMaximumHeight(200)
        scroll.setMinimumHeight(100)
        scroll_w = QtWidgets.QWidget()
        scroll_w_layout = QtWidgets.QVBoxLayout()
        scroll_w_layout.setContentsMargins(2,0,0,1)
        scroll_w_layout.setSpacing(2)

        header_txt = "   Value  | \t Value Name \t | \tDescription"
        header_lbl = QtWidgets.QLabel(header_txt)
        scroll_w_layout.addWidget(header_lbl)
        for value in values:
            temp_value = ModuleGui._create_value(values[value], style)
            scroll_w_layout.addWidget(temp_value)

        scroll_w.setLayout(scroll_w_layout)
        scroll.setWidget(scroll_w)


        layout.addWidget(scroll)

        widget.setLayout(layout)

        return widget

    @staticmethod
    def _create_footer():
        '''Creates module tab footer section

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
        exe_text = "Run module"
        btn_exe = QtWidgets.QPushButton(exe_text)
        btn_exe.setObjectName("btn_execute")
        layout.addWidget(btn_exe)
        layout.addStretch(1)

        widget.setLayout(layout)

        return widget
