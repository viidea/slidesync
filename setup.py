from distutils.core import setup
import py2exe

setup(name="slidesync",
      version="0.1",
      modules=["audiosync", "processing", "pyvideo", "widgets", "windows"],
      windows=["main.py"],
      data_files=["avbin.dll","flann.dll"],
      options={
          "py2exe":{
              "includes":["sip", "scipy.io.matlab.streams"]
          }
      })
