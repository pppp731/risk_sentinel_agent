@echo off
chcp 65001
cls
echo ==========================================
echo  实时舆情监控系统
echo ==========================================
echo.
echo 正在启动实时监控系统...
echo.
echo 访问地址: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务
echo ==========================================
echo.
python realtime_app.py
pause