import re
import os


def extract_classes_and_properties(dart_content: str) -> dict:
    # Regex pattern to match class definitions and their content.
    class_pattern = re.compile(r'class\s+(\w+)(?:\s+extends\s+\w+)?\s*\{([\s\S]+?)\}\n\n', re.DOTALL)

    # Extract classes and their content
    classes = class_pattern.findall(dart_content)

    # Dictionary to store the result
    result = {}

    for class_name, class_content in classes:
        # Extract properties from class content
        properties = re.findall(r'final\s+([\w<>?]+)\s+(\w+);', class_content)

        result[class_name] = properties

    return result


def dart_type_to_ts(dart_type):
    mapping = {
        'String': 'string',
        'int': 'number',
        'double': 'number',
        'bool': 'boolean',
    }

    list_match = re.match(r'List<([\w<>?]+)>', dart_type)
    if list_match:
        inner_type = dart_type_to_ts(list_match.group(1))
        return f'{inner_type}[]'

    # Handle nullable types
    if dart_type.endswith('?'):
        dart_type = dart_type[:-1]
        ts_type = mapping.get(dart_type, dart_type + "Dto")
        return f"{ts_type}"

    return mapping.get(dart_type, dart_type + "Dto")


def generate_ts_properties(properties):
    ts_props = []
    for dart_type, prop_name in properties:
        ts_type = dart_type_to_ts(dart_type)
        ts_prop = f"""
    @ApiProperty({{
        description: 'Description for {prop_name}',
        type: '{ts_type}', 
        nullable: true,
    }})
    readonly {prop_name}: {ts_type};
"""
        ts_props.append(ts_prop)
    return ''.join(ts_props)


def generate_ts_dto(classes_and_properties):
    dtos = []

    # If there are any classes, then we add the import statement
    if classes_and_properties:
        dtos.append("import { ApiProperty } from '@nestjs/swagger';\n")

    for class_name, properties in classes_and_properties.items():
        ts_props = generate_ts_properties(properties)
        dto = f"""
export class {class_name}Dto {{{ts_props}
}}
"""
        dtos.append(dto)
    return ''.join(dtos)


def generate_dto_file_from_dart(dart_filepath, output_filepath):
    try:
        # Ensure the Dart file exists
        if not os.path.exists(dart_filepath):
            print(f"Error: Dart file not found: {dart_filepath}")
            return

        with open(dart_filepath, 'r') as dart_file:
            dart_content = dart_file.read()
            classes_and_properties = extract_classes_and_properties(dart_content)
            ts_content = generate_ts_dto(classes_and_properties)

            # Ensure the directory exists before trying to write to it
            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

            with open(output_filepath, 'w') as ts_file:
                ts_file.write(ts_content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
