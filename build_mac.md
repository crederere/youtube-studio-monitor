# 맥(macOS)에서 Python 앱 빌드하기

## 방법 1: 기존 스크립트 사용 (권장)

맥에서 터미널을 열고:

```bash
# 실행 권한 부여
chmod +x build_mac_linux.sh

# 빌드 실행
./build_mac_linux.sh
```

## 방법 2: 수동 빌드

### 1. PyInstaller 설치
```bash
# Python3와 pip 확인
python3 --version
pip3 --version

# PyInstaller 설치
pip3 install pyinstaller
pip3 install -r requirements.txt
```

### 2. 빌드 실행
```bash
# spec 파일로 빌드
pyinstaller build_config.spec

# 또는 직접 빌드 (once.py 사용)
pyinstaller --onefile --name YouTubeStudioMonitor once.py

# 또는 가벼운 버전 (once_light.py 사용)
pyinstaller --onefile --name YouTubeStudioMonitor_Light once_light.py
```

### 3. 빌드된 파일 확인
```bash
# dist 폴더에 생성됨
ls -la dist/
```

## 맥 앱 번들(.app) 만들기

빌드 후 .app 파일로 만들려면:

```bash
# 앱 번들 구조 생성
mkdir -p YouTubeStudioMonitor.app/Contents/MacOS
mkdir -p YouTubeStudioMonitor.app/Contents/Resources

# 실행 파일 복사
cp dist/YouTubeStudioMonitor YouTubeStudioMonitor.app/Contents/MacOS/

# Info.plist 생성
cat > YouTubeStudioMonitor.app/Contents/Info.plist << 'EOF'
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
</dict>
</plist>
EOF
```

## 문제 해결

### 1. 실행 권한 에러
```bash
chmod +x dist/YouTubeStudioMonitor
```

### 2. 보안 경고 (macOS Gatekeeper)
- 시스템 환경설정 > 보안 및 개인정보 보호 > 일반
- "다음에서 다운로드한 앱 허용" 확인
- 또는 터미널에서: `xattr -d com.apple.quarantine YouTubeStudioMonitor.app`

### 3. M1/M2 맥에서 Intel 앱 실행
- Rosetta 2가 자동으로 설치됨
- 네이티브 ARM 빌드를 원하면:
```bash
pyinstaller --target-arch arm64 build_config.spec
```

## 빌드 옵션

### 경량 버전 (once_light.py)
크롬 자동화 없이 토큰만 입력:
```bash
pyinstaller --onefile --name YouTubeStudioMonitor_Light once_light.py
```

### 디버그 모드
문제 해결용:
```bash
pyinstaller --onefile --debug all --name YouTubeStudioMonitor_Debug once.py
```

## 배포

빌드된 파일은 Python이 설치되지 않은 다른 맥에서도 실행 가능합니다:
1. `dist/YouTubeStudioMonitor` 또는 `YouTubeStudioMonitor.app` 복사
2. 실행 권한 확인
3. 더블클릭으로 실행