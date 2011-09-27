# BioPARKIN
## Biology-related Parameter Identification in Large Kinetic Networks

Modelling, parameter identification, and simulation play an important role in Systems Biology. In recent years, various software packages have been established for scientific use in both licencing types, open source as well as commercial.  Many of these codes are based on inefficient and mathematically outdated algorithms. By introducing the package BioPARKIN, we want to improve this situation. The development of the software BioPARKIN involves long standing mathematical ideas that, however, have not yet entered the field of Systems Biology, as well as new ideas and tools that are particularly important for the analysis of the dynamics of biological networks.

Please visit the [project page with some additional background information](http://www.zib.de/en/numerik/csb/projekte/projektdetails/article/poem-1.html).

## License

This software package is released under the LGPL 3.0, see LICENSE file.


## Technical Overview

BioPARKIN is the graphical user interface (GUI) building upon PARKINcpp. PARKINcpp is another of our projects and can be found at github.com/CSB-at-ZIB/PARKINcpp.

It is the numerical core that BioPARKIN uses. It's written in performance-optimized C++. It is also available under the LGPL 3.0.

We decided to split the projects in two because the PARKINcpp library might be useful on its own (for integrating in other software tools, etc.).


## Prerequisites

BioPARKIN is written in Python 2.7 and Qt. It uses PySide (>1.0.6) to interface with Qt. The Python libraries listed in the next section also need to be installed.

BioPARKIN comes with a pre-compiled version of PARKINcpp for Windows 32bit and for Linux (Ubuntu 11.04, 32bit). These binaries are provided so that a freshly cloned repository "just works" on most (some?) machines. However, in order to have the most up-to-date PARKINcpp as well as to be able to develop within the BioPARKIN/PARKINcpp framework, you need to clone both repositories.


## Libraries

BioPARKIN uses the following open-source libraries:

* [PySide](http://www.pyside.org/) >= 1.0.6
* [libSBML](http://sbml.org/Software/libSBML) with Python bindings >= 4.02
* [matplotlib](http://matplotlib.sourceforge.net/) >= 1.1.0 
  * (currently only available as [source via their github repo](https://github.com/matplotlib/matplotlib))
* [NetworkX](http://networkx.lanl.gov/) >= 1.3 
  * (this is currently not used in the code, but might soon be, once we re-enable graphical model network views)
* [StableDict](http://pypi.python.org/pypi/StableDict/0.2) >= 0.2 
  * (this is a leftover from Python 2.6, we will switch to Python 2.7 OrderedDicts soon)
* Todo: Add the other libs...
