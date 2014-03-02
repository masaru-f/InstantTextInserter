call build_clean.bat

python setup.py py2exe
rmdir /s /q .\build

xcopy .\license .\dist\license /I
xcopy .\for_dist\snippet .\dist\snippet /I
copy .\for_dist\readme.txt .\dist\readme.txt
copy .\for_dist\hotkey.ini .\dist\hotkey.ini
ren .\dist\entrypoint.exe iti.exe

python -c "import os; import selfinfo; os.rename('dist',selfinfo.PROGRAM_NAME + selfinfo.VERSION)"
pause
