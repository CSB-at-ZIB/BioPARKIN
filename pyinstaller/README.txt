How to create executables of BioPARKIN with PyInstaller
=======================================================

Note: It's not possible to just use a .spec file from subversion. The .spec
file references not only the .py file (this could be done with a relative [../src/] path)
but also references the local installation of PyInstaller.
Easiest solution: Quickly create your own spec file and adjust it manually if needed.


1.
Download PyInstaller:

2.
Install and configure PyInstaller
(python Configure.py)

3.
Important: Change the PyQT hook file according to this information:
http://www.pyinstaller.org/wiki/PyQtChangeApiVersion

4. 
Make spec file (python Makespec.py [options] ./path/to/BioParkin.py

5.
Look at the local .spec file and adjust your file if necessary (e.g. including the icon).

6.
Build executable (python Build /path/to/spec/file)

