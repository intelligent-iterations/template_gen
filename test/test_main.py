import os

from src.jobs.create_model import createModel
from src.jobs.enchance_model import enhanceModel
from src.jobs.model_to_repository import modelToRepository
from src.jobs.run_test import primitiveClass, primitiveClassEnhanced, primitiveRepoTestExample
from src.services.file_service import save_file, read_file


def test_model_enhancement():
    print(
    'started test'
    )
    working_path = os.getcwd()

    tempPath = f'{working_path}/temp/'
    className = 'Jose'
    pathName = 'jose.dart'

    model_path = createModel(className, working_path)
    print(f'model created in {model_path}')  # Print statements are okay in tests, but they're not assertions

    save_file(model_path, primitiveClass)

    repo, repo_test = modelToRepository(working_path, model_path)

    assert  repo_test.strip() == primitiveRepoTestExample.strip()

