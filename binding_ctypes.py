""" Simple examples of calling C functions through ctypes module. """
import os
import ctypes
import sys
import pathlib

# # load the library
# lib = cdll.LoadLibrary('./x64/Release/pythonBinder.dll')

if __name__ == "__main__":
	libname = pathlib.Path().absolute()
	libname = os.path.join(libname, '../x64', 'Release')
	print("libname: ", libname)

	# Load the shared library into c types.
	if sys.platform.startswith("win"):
		c_lib = ctypes.CDLL(os.path.join(libname, "pythonBinder.dll"))
	else:
		c_lib = ctypes.CDLL(os.path.join(libname, "pythonBInder.so"))

	# Sample data for our call:
	x, y = 6, 2.3

	# This will not work:
	# answer = c_lib.cmult(x, y)

	# This produces a bad answer:
	answer = c_lib.cppmult(x, ctypes.c_float(y))
	print(f"    In Python: int: {x} float {y:.1f} return val {answer:.1f}")
	print()

	# You need tell ctypes that the function returns a float
	c_lib.cppmult.restype = ctypes.c_float
	answer = c_lib.cppmult(x, ctypes.c_float(y))
	print(f"    In Python: int: {x} float {y:.1f} return val {answer:.1f}")

	# create a Geek class
	class Geek(object):
		# constructor
		def __init__(self):
			# attribute
			self.obj = c_lib.Geek_new()
		# define method
		def myFunction(self):
			c_lib.Geek_myFunction(self.obj)
		def readImage(self, imageName):
			c_lib.Geek_readImage(self.obj, imageName)
	f = Geek()
	f.myFunction()

	# This doesn't work! OSError: exception: access violation reading 0x000000010000000F
	# f.readImage(imageName="C:/Users/zhenyuanshen/Documents/projects/tools/input/face_align/0001.jpg")