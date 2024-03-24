import os
import re
import inflection

from src.jobs.dto_to_service_and_controller import generate_service_file
from src.jobs.dart_model_to_dto import generate_dto_file_from_dart
from src.jobs.model_to_repository import modelToRepository
from src.jobs.template import create_file_from_template
from src.jobs.test_model import testModel
from src.services.file_service import get_dartgen_path, getModelClassName, camel_case, getModelPathName


def modelToService(working_path, model_path):
    print('modelToService called')

    ClassName = getModelClassName(model_path)
    class_name = getModelPathName(model_path)
    className = inflection.camelize(ClassName, False)

    base = get_dartgen_path()

    class_template = f'{base}/src/templates/lib/service.txt'
    test_class_template = f'{base}/src/templates/test/service_test.txt'

    repo_output_path = f'{working_path}/lib/service/{class_name}_service.dart'
    repo_test_output_path = f'{working_path}/test/service/{class_name}_service_test.dart'

    create_class_result = create_file_from_template(
        class_template,
        repo_output_path,
        ClassName,
        className,
        class_name,
    )

    create_test_class_result = create_file_from_template(
        test_class_template,
        repo_test_output_path,
        ClassName,
        className,
        class_name,
    )

    return create_class_result, create_test_class_result


def modelToApiService(working_path, model_path):
    print('modelToService called')

    ClassName = getModelClassName(model_path)
    class_name = getModelPathName(model_path)
    className = inflection.camelize(ClassName, False)

    base = get_dartgen_path()

    class_template = f'{base}/src/templates/lib/server_service.txt'

    repo_output_path = f'{working_path}/lib/service/{class_name}_service.dart'

    create_class_result = create_file_from_template(
        class_template,
        repo_output_path,
        ClassName,
        className,
        class_name,
    )

    return create_class_result
