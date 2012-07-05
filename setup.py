from distutils.core import setup
import py2exe
import datetime

setup(name="slidesync",
      version=datetime.date.today().strftime("%Y.%m.%d"),
      modules=["audiosync", "processing", "pyvideo", "widgets", "windows"],
      windows=[{
          "script":"main.py",
          "icon_resources":[(0,"viidea.ico")],
          "dest_base":"slidesync"
      }],
      data_files=["avbin.dll","flann.dll"],
      options={
          "py2exe":{
              "includes" : ["sip", "scipy.io.matlab.streams"],
              "excludes": ["TKinter", "_ssl", "pywin", "pywin.debugger", "pywin.debugger.dbgcon", 
                           "pywin.dialogs", "pywin.dialogs.list", "Tkconstants", "Tkinter", "tcl",
                           "_imagingtk", "PIL._imagingtk", "ImageTk", "PIL.ImageTk", "FixTk"],
              "optimize":2
          }
      },
      requires=['numpy', 'scipy', 'pyvideo'])