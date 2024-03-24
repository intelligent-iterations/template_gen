from src.services.class_service import getTestClass
import os

import re


def testModel(workingPath, modelPath):
    print(workingPath)

    # Check if the given path has .dart extension
    if not modelPath.endswith('.dart'):
        print(f"Invalid file extension. Expected '.dart' file but got '{modelPath}'")
        return

    # Extract the class name from the model content
    className = extract_class_name(modelPath)
    fileName = extractFileName(modelPath)

    # Define test file path
    print(f"filename {fileName}")
    testPath = getTestFilePath(workingPath, fileName)

    # Write test file
    relativePath = os.path.relpath(modelPath, workingPath)

    with open(testPath, 'w') as file:
        file.write(getTestClass(className, relativePath))

    print(f"Test file has been created at '{testPath}'")


def getTestFilePath(workingPath, fileName):
    # Create test directory path
    testDirPath = os.path.join(workingPath, "test/model")
    os.makedirs(testDirPath, exist_ok=True)

    print(fileName)
    testFilePath = os.path.join(testDirPath, f"{fileName}_test.dart")

    return testFilePath


def extract_class_name(modelPath):
    with open(modelPath, 'r') as file:
        model_content = file.read()

    match = re.search(r"class (\w+)", model_content)
    if not match:
        print("Failed to extract class name")
        return None
    return match.group(1)


def getTestClass(className, path):
    relativePath = os.path.relpath(path, start='lib/model')

    test_file_content = [
        "import 'package:flutter_test/flutter_test.dart';",
        f"import '../../lib/model/{relativePath}';",
        "",
        "void main() async {",
        f"  group('{className}', () {{",
        "    test('parseSample', () {",
        f"      var exampleJson = {className}.exampleJson();",
        f"      var parse = {className}.fromJson(exampleJson);",
        "    });",
        "    test('parseEmpty', () {",
        f"      var emptyWorks = {className}.fromJson({{}});",
        "    });",
        "    test('query empty', () {",
        f"      var exampleJson = {className}.exampleJson();",
        f"      var parse = {className}.fromJson(exampleJson);",
        "      final emptyShouldBeFalse = parse.match({});",
        f"      final expectedFalse = parse.match({{\"id\":true}});",
        f"      final expectedTrue = parse.match(exampleJson);",
        "      expect(expectedTrue, true);",
        "      expect(emptyShouldBeFalse, false);",
        "      expect(expectedFalse, false);",
        "    });",
        "  });",
        "}"
    ]

    return "\n".join(test_file_content)


def extractFileName(path):
    print(f'extractFileName on {path}')
    filename = os.path.splitext(os.path.basename(path))[0]
    print(f'extractFileName returning {filename}')
    return filename
