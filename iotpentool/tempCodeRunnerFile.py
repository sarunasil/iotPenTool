for flag in flags:
            temp_flag = ModuleGui._create_flag(flags[flag], style)
            temp_flag.setStyleSheet("background-color:black;");
            layout.addWidget(temp_flag)