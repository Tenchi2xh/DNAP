@echo off

del /s *.pyc *.pyo 2> NUL
for /d /r %%x in (__pycache__) do @if exist "%%x" rmdir /s /q "%%x" 2> NUL
rmdir /s /q build dist 2> NUL
