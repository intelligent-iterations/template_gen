import os
import inflection
from src.services.class_service import getSimpleClass


def createModel(name, workingPath):
    modelPath = os.path.join(workingPath, "lib", "model")
    testPath = os.path.join(workingPath, "test", "model")
    
    os.makedirs(modelPath, exist_ok=True)
    os.makedirs(testPath, exist_ok=True)
    
    print(f"Model to be created with name {name}")
    
    snakeName = inflection.underscore(name)
    uppercaseCamelCase = inflection.camelize(name, uppercase_first_letter=True)

    filePath = os.path.join(modelPath, f"{snakeName}.dart")

    with open(filePath, "w") as file:
        file.write(getSimpleClass(uppercaseCamelCase))    
    
    print("Success")
    
    return filePath
