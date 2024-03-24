from src.services.file_service import read_file, save_file
from src.services.class_service import parse_class_definition


def enhanceModel(path):
    content = read_file(path)
    class_sections = content.strip().split("class")[1:]  # Ignore leading part before first class
    results = [parse_class_definition("class " + class_section) for class_section in class_sections]  # Parse each class
    dart_code = "import 'package:equatable/equatable.dart';\n\n"
    dart_code += "\n".join([enhanceDartModel(*result) for result in results])  # Join all code sections
    save_file(path, dart_code)
    print(f"Successfully written to {path}")


def enhanceDartModel(class_name, class_variables):
    output = ""  # Initialize the output variable
    output += f"class {class_name} extends Equatable {{\n"

    # Generate constructor
    output += f"  {class_name}({{"
    for var_type, var_name in class_variables:
        output += f"required this.{var_name}, "
    output = output[:-2]  # Remove the trailing comma and space
    output += "});\n\n"

    # Generate class variables
    for var_type, var_name in class_variables:
        output += f"  final {var_type}? {var_name};\n"

    # Generate Equatable implementation
    output += "\n  @override\n  List<Object?> get props => ["
    for _, var_name in class_variables[:-1]:
        output += f"{var_name}, "
    output += f"{class_variables[-1][1]}];\n"

    # Generate toJson method
    output += "\n  Map<String, dynamic> toJson() {\n    return {"
    for var_type, var_name in class_variables:
        if "List<" in var_type:
            base_type = var_type.replace("List<", "").replace(">", "")
            if is_primitive(base_type):
                output += f"'{var_name}': {var_name}, "
            else:
                output += f"'{var_name}': {var_name}?.map((e) => e.toJson()).toList(), "
        elif is_primitive(var_type):
            output += f"'{var_name}': {var_name}, "
        else:
            output += f"'{var_name}': {var_name}?.toJson(), "
    output = output[:-2]  # Remove the trailing comma and space
    output += "};\n  }\n"

    # Generate fromJson factory method
    # Generate fromJson factory method
    output += f"\n  factory {class_name}.fromJson(Map<String, dynamic> map) {{\n"
    output += f"    return {class_name}("
    for var_type, var_name in class_variables:
        if "List<" in var_type:
            base_type = var_type.replace("List<", "").replace(">", "")
            if is_primitive(base_type):
                output += f"{var_name}: List<{base_type}>.from(map['{var_name}']??[]), "
            else:
                output += f"{var_name}: (map['{var_name}'] as List<dynamic>).map((e) => {base_type}.fromJson(e)).toList(), "
        elif is_primitive(var_type):
            output += f"{var_name}: map['{var_name}'], "
        else:
            output += f"{var_name}: {var_type}.fromJson(map['{var_name}']??{{}}), "
    output = output[:-2]  # Remove the trailing comma and space
    output += ");\n  }\n"

    # Generate copyWith method
    output += f"\n  {class_name} copyWith({{"
    for var_type, var_name in class_variables:
        output += f"{var_type}? {var_name}, "
    output = output[:-2]  # Remove the trailing comma and space
    output += f"}}) {{\n    return {class_name}("
    for _, var_name in class_variables:
        output += f"{var_name}: {var_name} ?? this.{var_name}, "
    output = output[:-2]  # Remove the trailing comma and space
    output += ");\n  }\n"

    # Generate exampleJson method
    output += "\n static Map<String, dynamic> exampleJson() {\n    return {"
    for var_type, var_name in class_variables:
        if is_primitive(var_type):
            default_value = get_default_value(var_type)
        else:
            default_value = f"{var_type}.exampleJson()"
        output += f"'{var_name}': {default_value}, "
    output = output[:-2]  # Remove the trailing comma and space
    output += "};\n  }\n"

    # Exampel

    output += """
bool match(Map map){
    final model = toJson();
    final keys = model.keys.toList();
    
    for(final query in map.entries){
      try{
        final trueValue = model[query.key];
        final exists  = trueValue == query.value;
        if(exists){
          return true;
        }
      }catch(e){
        return false;
      }
    }
    return false;
}
    """.strip()

    output += f"\n\nstatic {class_name} example()=> {class_name}.fromJson({class_name}.exampleJson());"

    # Close class definition
    output += "}\n"

    return output


def get_default_value(var_type):
    if var_type == "String":
        return '""'
    elif var_type == "int":
        return "0"
    elif var_type == "double":
        return "0.0"
    elif var_type == "bool":
        return "false"
    elif var_type == "List<String>":
        return "['example']"
    elif "List<int>" in var_type:
        return "[0]"
    elif "List<double>" in var_type:
        return "[0.0]"
    elif "List<bool>" in var_type:
        return "[false]"
    else:
        return "{}"


def is_primitive(var_type):
    primitive_types = ["String", "int", "double", "bool", "List<String>", "List<int>", "List<bool>", "List<double>"]
    return var_type in primitive_types
