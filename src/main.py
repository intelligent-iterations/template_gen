import sys
import os
from src.jobs.create_model import createModel
from src.jobs.enchance_model import enhanceModel
from src.jobs.model_to_module import modelToDto
from src.jobs.test_model import testModel
from src.jobs.model_to_service import modelToService, modelToApiService
from src.jobs.model_to_repository import modelToRepository
from src.jobs.create_view import create_view
from src.jobs.run_test import runTest
from src.jobs.template import template
from src.services.file_service import get_dartgen_path


def main():
    action = sys.argv[1]
    value = sys.argv[2]
    server_path = sys.argv[3] if len(sys.argv) > 3 else None

    # Get the working directory path
    workingPath = os.getcwd()
    if action == "model":
        createModel(value, workingPath)
    elif action == "model-enhance":
        enhanceModel(value)
    elif action == 'model-all':
        print('model-all called')
        if server_path is None:
            print("The 'model-methods' action requires server path as third argument.")
            sys.exit(1)
        enhanceModel(value)
        modelToDto(server_path, value)
        modelToApiService(workingPath, value)
        modelToRepository(workingPath, value)
        testModel(workingPath, value)
    elif action == "model-methods":
        print('model-methods called')
        if server_path is None:
            print("The 'model-methods' action requires server path as third argument.")
            sys.exit(1)
        modelToDto(server_path, value)
        modelToApiService(workingPath, value)
        modelToRepository(workingPath, value)
        testModel(workingPath, value)
    elif action == "model-test":
        testModel(workingPath, value)
    elif action == "model-service":
        modelToService(workingPath, value)
    elif action == "model-repository":
        modelToRepository(workingPath, value)
    elif action == "run-test":
        runTest()

    elif action == "model-generate":
        enhanceModel(value)
        testModel(workingPath, value)
        modelToService(workingPath, value)
        modelToRepository(workingPath, value)

    elif action == "model-generate-view":
        enhanceModel(value)
        testModel(workingPath, value)
        modelToService(workingPath, value)
        modelToRepository(workingPath, value)
        create_view(value)




    elif "template" in action:
        # Get the current script's directory.
        PROJECT_ROOT = get_dartgen_path()

        ClassName = sys.argv[3]

        if action == "template-model":
            path = os.path.join(PROJECT_ROOT, 'src/templates/lib/model.txt')
            print('Templating model not currently supported. Help is appreciated')

        elif action == "template-mode-test":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/test/model_test.txt')
            template(value, ClassName, path)

        elif action == "template-service":
            path = os.path.join(PROJECT_ROOT, 'src/templates/lib/service.txt')
            template(value, ClassName, path)

        elif action == "template-service-test":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/test/service_test.txt')
            template(value, ClassName, path)

        elif action == "template-view":
            path = os.path.join(PROJECT_ROOT, 'src/templates/lib/view.txt')
            template(value, ClassName, path)

        elif action == "template-view-test":
            print(f'Option {action} is currently not supported')

        elif action == "template-view-model":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/lib/view_model.txt')
            template(value, ClassName, path)

        elif action == "template-view-model-test":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/test/view_model_test.txt')
            template(value, ClassName, path)

        elif action == "template-repository":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/lib/repository.txt')
            template(value, ClassName, path)

        elif action == "template-repository-test":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/test/repository_test.txt')
            template(value, ClassName, path)

        elif action == "template-server-service":
            #$ dartgen template-server-controller

            path = os.path.join(
                PROJECT_ROOT, 'src/templates/server/service.txt')
            template(value, ClassName, path)

        elif action == "template-server-controller":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/server/controller.txt')
            template(value, ClassName, path)

        elif action == "template-server-controller-spec":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/server/controller_spec.txt')
            template(value, ClassName, path)

        elif action == "template-server-module":
            path = os.path.join(
                PROJECT_ROOT, 'src/templates/server/module.txt')
            template(value, ClassName, path)


        else:
            print(f"Sorry, unrecognized template action: {action}")

    else:
        print("Sorry, invalid action:", action)

    print('Success!')


if __name__ == "__main__":
    main()
