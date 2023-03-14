# How-to-Run Search Engine

Prerequisites:
	- Python 3.9

Step 1. Download Required Library/Modules
	a) pip install nltk
	b) pip install bs4
	c) pip install Flask

Step 2.
	Modiy line 23 of engine.py to match the
	relative folder that contains the folders of domains.
	By default, it is set to 'developer/DEV'

Running Index (Expected time: ~2-3 hours):
	- python3 engine.py

Running Search Engine:

	- Terminal GUI
		- python3 search.py

	- Web GUI
		# Does not work on openlabs
		# Local machine with IDE( VSCode ) is recommended
		- python3 app.py
	
