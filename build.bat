@echo off
pyinstaller --onefile --icon=src/assets/icon.ico --name=PHE_FlipOptimizer src/main.py
echo.
echo 打包完成！
pause