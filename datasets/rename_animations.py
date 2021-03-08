# Copyright 2021 K. S. Ernest (iFire) Lee
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
import os
import re

root_dir = '.'
animation_set = "mixamo"
file_count = 0

files_sorted = []
for directory, subdirectories, files in os.walk(root_dir):
    for file in files:
        file_no_ext = os.path.splitext(file)[0]
        file_ext = os.path.splitext(file)[1]
        input_name = os.path.join(directory, file)
        files_sorted.append([input_name])

files_sorted.sort()

for files in files_sorted:
    for file in files:
        file_no_ext = os.path.splitext(file)[0]
        file_ext = os.path.splitext(file)[1]
        file_no_ext = f"skel_{animation_set}_anim_{str(file_count).zfill(4)}_desc{file_no_ext}"
        file_no_ext = re.sub("[^_0-9a-zA-Z]+", "_", file_no_ext)
        file_no_ext = file_no_ext.lstrip("_")
        file_no_ext = file_no_ext.rstrip("_")
        file_no_ext = file_no_ext.lower()
        file_no_ext = file_no_ext + file_ext
        os.rename(file, file_no_ext)
        print(f"Output: {file_no_ext}")
        file_count += 1
