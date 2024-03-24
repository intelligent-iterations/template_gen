import os
import re
import inflection

from src.jobs.template import create_file_from_template
from src.services.file_service import get_dartgen_path, getModelClassName, camel_case, getModelPathName


# Returns:
# create_repo_result
# create_repo_test_result
def modelToRepository(working_path, model_path):
    print(f"modelToRepository: called with:")

    ClassName = getModelClassName(model_path)
    class_name = getModelPathName(model_path)
    className = inflection.camelize(ClassName, False)

    base = get_dartgen_path()

    repo_template_path = f'{base}/src/templates/lib/repository.txt'
    repo_test_template_path = f'{base}/src/templates/test/repository_test.txt'

    repo_output_path = f'{working_path}/lib/repository/{class_name}_repository.dart'
    repo_test_output_path = f'{working_path}/test/repository/{class_name}_repository_test.dart'

    create_repo_result = create_file_from_template(
        repo_template_path,
        repo_output_path,
        ClassName,
        className,
        class_name,
    )

    create_repo_test_result = create_file_from_template(
        repo_test_template_path,
        repo_test_output_path,
        ClassName,
        className,
        class_name,
    )

    return create_repo_result, create_repo_test_result



