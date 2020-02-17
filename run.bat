@echo off
setlocal EnableDelayedExpansion
set argCount=0

SET mypath=%~dp0
SET line=python %mypath:~0,-1%\wrapper.py

for %%x in (%*) do (
    SET line=!line! "\%%x" 
 )

%line%

pause