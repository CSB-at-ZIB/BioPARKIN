import os, logging

__author__ = "Moritz Wade"
__contact__ = "wade@zib.de"
__copyright__ = "Zuse Institute Berlin 2010"

def removeFilesOfTypeFromDir(dir, type):
  """
  Remove all files of the given type in the given directory.
  File type is determined by its suffix.
  """
  for file in os.listdir(dir):
      if file.endswith("." + type):
        name = os.path.join(dir, file)
        try: os.remove(name)
        except:
          logging.error("File %s could not be removed." & name)
          
def removeFileFromDir(dir, name):
  """
  Delete the given file in the given directory.
  """
  for file in os.listdir(dir):
      if file.endswith(name):
        name = os.path.join(dir, file)
        try: os.remove(name)
        except:
          logging.error("File %s could not be removed." & name)

def renameFile(dir, oldName, newName):
    """
    Helper method to rename a file.
    """
    oldPath = os.path.join(dir, oldName)
    newPath = os.path.join(dir, newName)

    os.rename(oldPath, newPath)


def getHomeDir():
    """
    Returns the home directory. OS independent (hopefully ;)).
    """
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    return home

    