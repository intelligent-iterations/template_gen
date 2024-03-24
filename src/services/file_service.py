import os
import re

def read_file(file_path):
    print(f"Reading {file_path}")
    with open(file_path, 'r') as f:
        file_contents = f.read()
    return file_contents

def save_file(file_path, content):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_dartgen_path():
    # Get the current script's directory.
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Navigate upwards until reaching the project directory 'dart_gen'.
    PROJECT_ROOT = SCRIPT_DIR
    while os.path.basename(PROJECT_ROOT) != 'dart_gen':
        PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

    return PROJECT_ROOT

def project_path():
    working_path = os.getcwd()  # Get the current working directory
    last_directory = os.path.basename(working_path)  # Extract the last directory
    return last_directory

def getModelClassName(modelPath):
    # Read the content of the Dart file
    with open(modelPath, 'r') as file:
        content = file.read()

    # Find a Dart class definition in the content
    match = re.search(r'class (\w+)', content)

    if match:
        # Return the class name if found
        return match.group(1)
    else:
        # Return None if no class was found
        return None

def getModelPathName(modelPath):
    # Extract the model's name from the file path
    base_name = os.path.basename(modelPath)
    model_name, _ = os.path.splitext(base_name)

    return model_name

def camel_case(name):
    return ''.join(x for x in name.title() if x.isalnum())