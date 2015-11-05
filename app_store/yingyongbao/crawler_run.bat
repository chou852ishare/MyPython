@echo off
setlocal enabledelayedexpansion

rem #ids = xrange(1049137, 2233259)
set size=39500 
for /l %%i in (1049000,39500,2194500) do (
    set /a si=%%i+1
    set /a ei=%%i+%size% 
    start /b python crawler_anzhi_paral.py !si! !ei!
)