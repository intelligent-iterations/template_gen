import os

from src.jobs.create_model import createModel
from src.jobs.enchance_model import enhanceModel
from src.jobs.run_test import primitiveClass, primitiveClassEnhanced
from src.services.file_service import save_file, read_file


def test_model_enhancement():
    workingPath = os.getcwd()

    tempPath = f'{workingPath}/temp/'
    className = 'Jose'
    pathName = 'jose.dart'

    modelPath = createModel(className, workingPath)
    print(f'model created in {modelPath}')  # Print statements are okay in tests, but they're not assertions

    save_file(modelPath, primitiveClass)

    enhanceModel(modelPath)

    readEnchancedModelResult = read_file(modelPath).strip()

    # Use an assert to check your expectation
    assert readEnchancedModelResult == primitiveClassEnhanced.strip(), f"Expection occured. readEnchancedModelResult should have been: {primitiveClassEnhanced}, instead is {readEnchancedModelResult}"
