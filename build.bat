@echo off
echo Building Antimatter Clock...

rem Clean previous builds
rmdir /s /q dist
rmdir /s /q build

rem Run PyInstaller with the spec file
pyinstaller clock.spec

echo Build complete! Executable is in the dist folder.
pause