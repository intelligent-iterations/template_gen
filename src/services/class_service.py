def getSimpleClass (name):
    return f"class {name}" + "{\n\n}"


def getTestClass(name, path):
    lines = [
        "import 'package:flutter_test/flutter_test.dart';",
        f"import '../../{path}';",
        "",
        "void main() async {",
        f"  group('{name}', () {{",
        "    test('parseSample', () {",
        f"      var exampleJson = {name}.exampleJson();",
        f"      var parse = {name}.fromJson(exampleJson);",
        "    });",
        "    test('parseEmpty', () {",
        f"      var emptyWorks = {name}.fromJson({{}});",  # Escaping {}
        "    });",
        "  });",
        "}"
    ]
    return "\n".join(lines)


def parse_class_definition(class_definition):
    class_definition = class_definition.strip()  # Remove leading/trailing whitespace
    lines = class_definition.split("\n")
    class_name = lines[0].strip().split()[1].split("{")[0]  # Split on whitespace

    properties = []
    for line in lines[1:-1]:  # Exclude first and last lines
        line = line.strip()
        if line != "":
            parts = line.split(" ")
            var_type = parts[0]
            var_name = parts[1].rstrip(";")
            properties.append((var_type, var_name))

    return class_name, properties


  
