@echo off
chcp 65001 >nul
title Иркутская область 3D карта

echo ========================================
echo   3D карта Иркутской области (CesiumJS)
echo ========================================
echo.

:: Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo Скачайте и установите Python с python.org
    echo Не забудьте отметить "Add Python to PATH"
    echo.
    pause
    exit /b
)

:: Проверка наличия Streamlit
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Установка необходимых библиотек...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
)

:: Проверка наличия main.py
if not exist "main.py" (
    echo ❌ Ошибка: файл main.py не найден!
    echo.
    echo Убедитесь, что вы запускаете этот bat-файл
    echo в той же папке, где находится main.py
    echo.
    echo Текущая папка: %CD%
    echo.
    pause
    exit /b
)

:: Запуск
echo.
echo 🌐 Открытие браузера...
timeout /t 2 /nobreak >nul
start http://localhost:8501

echo 🚀 Запуск сервера...
echo.
echo Для остановки сервера нажмите Ctrl+C
echo.
python -m streamlit run main.py

pause