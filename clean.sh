find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ -o -name .DS_Store \) -prune -exec rm -rf {} +
rm -rf build dist
