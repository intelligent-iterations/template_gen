import os
import re

from src.jobs.dto_to_service_and_controller import generate_service_file, generate_controller_file
from src.jobs.dart_model_to_dto import generate_dto_file_from_dart
from src.services.file_service import getModelPathName, getModelClassName


def modelToDto(server_root, dart_model_path):
    class_path_name = getModelPathName(dart_model_path)
    modelName = getModelClassName(dart_model_path)
    basepath = f'{server_root}/src/modules/{class_path_name}/{class_path_name}'

    dto_filepath = f'{basepath}.dto.ts'
    service_path = f'{basepath}.service.ts'
    controller_path = f'{basepath}.controller.ts'
    module_path = f'{basepath}.module.ts'
    
    generate_dto_file_from_dart(dart_model_path, dto_filepath)
    generate_service_file(dto_filepath,
                          service_path, modelName)
    generate_controller_file(service_path, dto_filepath, controller_path, modelName)
    generate_module_file(service_path, controller_path, module_path, modelName)


def generate_module_file(service_file_path, controller_file_path, output_file_path, module_name):
    with open(service_file_path, 'r') as file:
        service_content = file.read()
        service_name_match = re.search(r'export class (\w+)', service_content)

        if not service_name_match:
            raise ValueError("Cannot find a class definition in the service file")

        service_name = service_name_match.group(1)

    with open(controller_file_path, 'r') as file:
        controller_content = file.read()
        controller_name_match = re.search(r'export class (\w+)', controller_content)

        if not controller_name_match:
            raise ValueError("Cannot find a class definition in the controller file")

        controller_name = controller_name_match.group(1)

    # Define the TypeScript module code template
    module_template = f"""
import {{ Module }} from '@nestjs/common';
import {{ {service_name} }} from './{os.path.basename(service_file_path)[:-3]}';
import {{ {controller_name} }} from './{os.path.basename(controller_file_path)[:-3]}';

@Module({{
    providers: [{service_name}],
    controllers: [{controller_name}],
}})
export class {module_name}Module {{ }}
"""
    # Ensure the directory exists before trying to write to it
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Write the generated module code to a TypeScript file
    with open(output_file_path, 'w') as file:
        file.write(module_template)
