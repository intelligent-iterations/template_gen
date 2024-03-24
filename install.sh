rm -rf /Users/joselara/python_projects/dart_gen/dist/tempgen
pyinstaller --paths venv/lib/python3.10/site-packages/ --name tempgen src/main.py
echo 'y'
pyinstaller tempgen.spec
echo 'y'