@echo off
setlocal EnableDelayedExpansion
set argCount=0

SET mypath=%~dp0
SET line=python3 %mypath:~0,-1%\src\wrapper.py

for %%x in (%*) do (
    SET line=!line! "\%%x" 
 )

echo %line%

%line%

pause