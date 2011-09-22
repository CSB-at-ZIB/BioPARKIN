WINDOWS
=======

python 2.6 (!) 32bit
libSBML-4.2.0-win-libxml2-x86.exe
(path setzen auf main-dir von libsbml)
pyqt (4.8.1 produced crashes, 4.8.3 works)
easyinstall


easyinstall networkx
easyinstall StableDict
(easy_install Cheetah) (should not be needed any longer)
easyinstall numpy

matplotlib-1.0.0.win32-py2.7.exe
gfortran


for developing:

mingw (gcc tools)



LINUX
=====

The following steps are necessary for Ubuntu 10.10 (Maverick):
--------------------------------------------------------------

a)
	[sudo] apt-get install python-networkx python-cheetah


b)
	[sudo] easy_install StableDict


c)	
	[preferably as root!]
	cd /opt			<-- or any other central directory 
	git clone git://github.com/matplotlib/matplotlib.git
	cd matplotlib
	python setup.py install

Step c) requires python development packages to be installed
(i.e. 'apt-get install python-dev' if not already present)

