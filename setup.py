import sys
from cx_Freeze import setup, Executable

setup(name="world_generator",
      version="0.1",
      options={"build_exe": {"packages": ["kivy"]}},
      description="",
      executables=[Executable("main.py", base=None)])
