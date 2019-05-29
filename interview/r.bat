@echo off
set file=perfect_number.py

if "%1" == "-d" (
    python -m pdb %file%
    goto end
)
python %file%

:end
