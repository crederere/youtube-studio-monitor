#!/bin/bash

echo "YouTube Studio Monitor - macOS/Linux 빌드 시작"
echo "================================================"

# 현재 OS 확인
OS=$(uname -s)
echo "현재 OS: $OS"

# 가상환경 생성 및 활성화
echo "[1/6] 가상환경 설정 중..."
python3 -m venv build_env
source build_env/bin/activate

# 필요한 패키지 설치
echo "[2/6] 의존성 설치 중..."
python -m pip install --upgrade pip
pip install pyinstaller
pip install -r requirements.txt

# 기존 빌드 파일 정리
echo "[3/6] 기존 빌드 파일 정리 중..."
rm -rf dist build

# PyInstaller로 빌드
echo "[4/6] PyInstaller로 빌드 중..."
pyinstaller build_config.spec

# 빌드 결과 확인
echo "[5/6] 빌드 결과 확인 중..."
if [ -f "dist/YouTubeStudioMonitor" ]; then
    echo "✅ 빌드 성공!"
    echo "실행 파일: dist/YouTubeStudioMonitor"
    echo "파일 크기:"
    ls -lh dist/YouTubeStudioMonitor
    
    # 실행 권한 부여
    chmod +x dist/YouTubeStudioMonitor
    echo "실행 권한 부여 완료"
else
    echo "❌ 빌드 실패!"
    exit 1
fi

# 정리
echo "[6/6] 정리 중..."
deactivate
rm -rf build_env

echo ""
echo "🎉 빌드 완료!"
echo "실행 파일 위치: $(pwd)/dist/YouTubeStudioMonitor"
echo ""
echo "사용법:"
echo "1. dist/YouTubeStudioMonitor 를 원하는 폴더에 복사"
echo "2. 터미널에서 ./YouTubeStudioMonitor 실행"
echo "3. Chrome이 자동으로 열리면 YouTube Studio에 로그인"
echo ""

# macOS에서 앱 번들로 만들기 (선택사항)
if [ "$OS" = "Darwin" ]; then
    echo "macOS 앱 번들을 생성하시겠습니까? (y/n)"
    read -r response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        echo "macOS 앱 번들 생성 중..."
        
        # 앱 번들 디렉토리 구조 생성
        mkdir -p "YouTubeStudioMonitor.app/Contents/MacOS"
        mkdir -p "YouTubeStudioMonitor.app/Contents/Resources"
        
        # 실행 파일 복사
        cp dist/YouTubeStudioMonitor "YouTubeStudioMonitor.app/Contents/MacOS/"
        
        # Info.plist 생성
        cat > "YouTubeStudioMonitor.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>YouTube Studio Monitor</string>
    <key>CFBundleDisplayName</key>
    <string>YouTube Studio Monitor</string>
    <key>CFBundleIdentifier</key>
    <string>com.youtubemonitor.app</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleExecutable</key>
    <string>YouTubeStudioMonitor</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
EOF
        
        echo "✅ macOS 앱 번들 생성 완료: YouTubeStudioMonitor.app"
        echo "Finder에서 더블클릭으로 실행할 수 있습니다."
    fi
fi

echo "빌드 완료!" 