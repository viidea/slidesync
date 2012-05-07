from distutils.core import setup
import py2exe

setup(name="slidesync",
      version="0.1",
      modules=["audiosync", "processing", "pyvideo", "widgets", "windows"],
      windows=[{
          "script":"main.py",
          "icon_resources":[(0,"viidea.ico")]
      }],
      data_files=["avbin.dll","flann.dll"],
      options={
          "py2exe":{
              "includes" : ["sip", "scipy.io.matlab.streams"],
              "optimize":2
          }
      })
