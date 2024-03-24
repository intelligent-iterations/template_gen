import inflection
import os
import re
import os
from src.jobs.template import create_file_from_template

# Get the current script's directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate upwards until reaching the project directory 'dart_gen'.
PROJECT_ROOT = SCRIPT_DIR
while os.path.basename(PROJECT_ROOT) != 'dart_gen':
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

# Construct the paths for your template files using the PROJECT_ROOT.
TEMPLATE_VIEW_PATH = os.path.join(PROJECT_ROOT, "src/templates/lib/view.txt")
TEMPLATE_VIEW_MODEL_PATH = os.path.join(PROJECT_ROOT, "src/templates/lib/view_model.txt")
TEMPLATE_VIEW_MODEL_TEST_PATH = os.path.join(PROJECT_ROOT, "src/templates/test/view_model_test.txt")


def create_view(model_path):
    ClassName = getModelClassName(model_path)
    class_name = getModelPathName(model_path)
    className = inflection.camelize(ClassName, False)


    # Paths for generated files
    view_output_path = f"lib/view/{class_name}_view/{class_name}_view.dart"
    view_model_output_path = f"lib/view_models/{class_name}_view_model.dart"
    view_model_test_output_path = f"test/view_models/{class_name}_view_model.dart"

    # Create view and view_model based on templates
    create_file_from_template(
        TEMPLATE_VIEW_PATH,
        view_output_path,
        ClassName,
        className,
        class_name,
    )

    create_file_from_template(
        TEMPLATE_VIEW_MODEL_PATH,
        view_model_output_path,
        ClassName,
        className,
        class_name,
    )
    create_file_from_template(
        TEMPLATE_VIEW_MODEL_TEST_PATH,
        view_model_test_output_path,
        ClassName,
        className,
        class_name,
    )


def camel_case(name):
    return ''.join(x for x in name.title() if x.isalnum())


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



def get_template_content(filepath):
    with open(filepath, 'r') as file:
        return file.read()
