@echo off
chcp 65001 >nul
echo ====================================
echo Excel数据问答系统 - 启动脚本
echo ====================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)
echo [√] Python环境正常

echo.
echo [2/3] 检查依赖包...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [!] 依赖包未安装，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖包安装失败
        pause
        exit /b 1
    )
) else (
    echo [√] 依赖包已安装
)

echo.
echo [3/3] 创建测试数据...
if not exist "test_data" (
    python test_data.py
)

echo.
echo ====================================
echo 启动服务器...
echo ====================================
echo.
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.

python app.py

pause
