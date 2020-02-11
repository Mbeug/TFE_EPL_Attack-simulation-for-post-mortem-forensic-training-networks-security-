#!/usr/bin/env python
import sys

# Filename to write
filename = sys.argv[1]

# Open the file with writing permission
myfile = open(filename, 'w')

# Write a line to the file
myfile.write('Written with Python\n')

# Close the file
myfile.close()

print("File ", filename, "Done")
