import os
import shutil
import inflection
import re
from  src.services.file_service import project_path

view_template_path = 'src/templates/lib/view.txt'
view_test_template_path = 'src/templates/test/view_test.txt'

view_model_template_path = 'src/templates/lib/view_model.txt'
view_model_test_template_path = 'src/templates/test/view_model_test.txt'

repo_template_path = 'src/templates/lib/repository.txt'
repo_test_template_path = 'src/templates/test/repository_test.txt'

service_template_path = 'src/templates/lib/service.txt'
service_test_template_path = 'src/templates/test/service_test.txt'

def template(model_path, ClassName, destination):
    # Check if the model_path exists and is a file
    if not os.path.isfile(model_path):
        raise ValueError(f"'{model_path}' does not exist or is not a valid file.")

    # Determine the destination path for the model content within your source code
    destination_path = destination

    # Ensure the directory for the destination file exists
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    # Check if a directory with the same name as the destination file already exists
    if os.path.isdir(destination_path):
        print(f"A directory with the name '{destination_path}' already exists.")
        response = input("Would you like to remove it? (y/n) ")
        if response.lower() == 'y':
            shutil.rmtree(destination_path)
        else:
            print("Exiting without copying...")
            return

    with open(model_path, 'r') as source_file:
        content = source_file.read()

    updated_content = replace_placeholders(content, ClassName)

    with open(destination_path, 'w') as dest_file:
        dest_file.write(updated_content)

    print(f"Model content from '{model_path}' has been copied to '{destination_path}'.")


def create_file_from_template(template_path, output_path, ClassName, className, class_name):
    content = get_template_content(template_path)
    modified_content = content.replace("ClassName", ClassName)
    modified_content = modified_content.replace("className", className)
    modified_content = modified_content.replace("class_name", class_name)
    modified_content = modified_content.replace("package_name", project_path())

    # Ensure directory exists before writing
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as file:
        file.write(modified_content)

    return modified_content

def get_template_content(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def getModelClassName(model_path):
    with open(model_path, 'r') as file:
        content = file.read()
    match = re.search(r'class (\w+)', content)
    if match:
        return match.group(1)
    else:
        return None


def getModelPathName(model_path):
    base_name = os.path.basename(model_path)
    model_name, _ = os.path.splitext(base_name)
    return model_name


def replace_placeholders(template_str, ClassName):
    # example ClassName has the value of MyClass
    class_name = inflection.underscore(ClassName)
    # example class_name has the value of my_class
    className = inflection.camelize(ClassName, False)
    # example class_name has the value of myClass


    # Order maatterns when replacing the class names
    template_str = template_str.replace(f'{class_name}_', 'class_name_')
    template_str = template_str.replace(f'{class_name}.dart', 'class_name.dart')
    template_str = template_str.replace(ClassName, 'ClassName', )
    template_str = template_str.replace(className, 'className', )

    template_str = template_str.replace(get_package_name(), 'package_name')

    return template_str


def get_package_name():
    # Get current working directory
    pwd = os.getcwd()
    # Split path and get last directory
    package_name = os.path.basename(pwd)
    return package_name
