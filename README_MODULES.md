# Intro


Module structure:
module_name
	|- __manifest__.py
	|- README.md
	|- modals		<- Directory to store the custom modals
	|    |- modal1.html
	|- buttons		<- Directory to store button html code
	|	|- button1.html
	|- methods		<- Directory to store the custom methods. These should hold a class that inherits from <panel.Methods>
	|	|- method1.py
	|
	|- xxxxx		<- In future use for checks on host or container
	
# __manifest__.py

```
# -*- coding: utf-8 -*-
{
    "name": "MODULE_NAME",
    "summary": """SHORT_DESCRIPTION_OF_THE_MODULE""",
    "version": "1.0.0",
	"author" : "Open2Bizz",
	"website" : "http://www.open2bizz.nl",
	"license" : "LGPL-3",
	"modals" : ['modals/modal1.html'],
	"buttons" : ['buttons/button1.html'],
	
}

```