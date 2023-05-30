# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:01:22 2023

@author: gfraga
"""
import subprocess
import os 
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
scripts_index = thisScriptDir.find('scripts')
dirputput = os.path.join(thisScriptDir[:scripts_index])



# Run the pip list command to get a list of installed packages
result = subprocess.run(['pip', 'list'], capture_output=True, text=True)

# Get the output and split it into lines
output_lines = result.stdout.split('\n')

# Specify the file path where you want to save the list of installed packages
file_path = os.path.join(dirputput,'installed_packages.txt')

# Open the file in write mode
with open(file_path, 'w') as file:
    # Write each line (package information) to the file
    for line in output_lines:
        file.write(line + '\n')

print(f"The list of installed packages has been saved to {file_path}.")
