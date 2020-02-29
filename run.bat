@echo off
setlocal EnableDelayedExpansion

SET mypath=%~dp0
SET line=py -3 %mypath:~0,-1%\src\wrapper.py

for %%x in (%*) do (
    echo %%x
    SET line=!line! %%x
 )

echo %line%

%line%

pause