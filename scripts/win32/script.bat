REM Creer l'installateur de Pyromaths pour Windows
C:
cd "C:\Documents and Settings\jerome\Bureau"
md pyromaths
cd pyromaths
xcopy z:\pyromaths\data data /i /s
xcopy z:\pyromaths\src src /i /s
copy z:\pyromaths\scripts\win32\setup.py .
copy z:\pyromaths\* .
move pyromaths Pyromaths.py
c:\Python26\python.exe setup.py innosetup
copy dist\Pyromaths-*-win32.exe z:\
cd ..
rmdir /s /q pyromaths