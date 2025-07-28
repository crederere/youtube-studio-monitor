@echo off
echo YouTube Studio Monitor - Windows 빌드 시작
echo ================================================

:: 가상환경 생성 및 활성화
echo [1/6] 가상환경 설정 중...
python -m venv build_env
call build_env\Scripts\activate.bat

:: 필요한 패키지 설치
echo [2/6] 의존성 설치 중...
python -m pip install --upgrade pip
pip install pyinstaller
pip install -r requirements.txt

:: 기존 빌드 파일 정리
echo [3/6] 기존 빌드 파일 정리 중...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

:: PyInstaller로 빌드
echo [4/6] PyInstaller로 빌드 중...
pyinstaller build_config.spec

:: 빌드 결과 확인
echo [5/6] 빌드 결과 확인 중...
if exist "dist\YouTubeStudioMonitor.exe" (
    echo ✅ 빌드 성공!
    echo 실행 파일: dist\YouTubeStudioMonitor.exe
    echo 파일 크기:
    dir "dist\YouTubeStudioMonitor.exe"
) else (
    echo ❌ 빌드 실패!
    pause
    exit /b 1
)

:: 정리
echo [6/6] 정리 중...
deactivate
rmdir /s /q build_env

echo.
echo 🎉 빌드 완료!
echo 실행 파일 위치: %cd%\dist\YouTubeStudioMonitor.exe
echo.
echo 사용법:
echo 1. dist\YouTubeStudioMonitor.exe 를 원하는 폴더에 복사
echo 2. 더블클릭으로 실행
echo 3. Chrome이 자동으로 열리면 YouTube Studio에 로그인
echo.
pause 