# YouTube Studio Monitor - 빌드 가이드

YouTube Studio에서 비디오 데이터와 애널리틱스를 자동으로 수집하는 크로스 플랫폼 도구입니다.

## ✨ 특징

- **크로스 플랫폼**: Windows, macOS, Linux 모두 지원
- **파이썬 불필요**: 빌드된 실행 파일은 파이썬 설치 없이 실행 가능
- **자동 수집**: 브라우저의 실제 API 요청을 감지하여 완전한 데이터 수집
- **다중 탭 지원**: 노출수, CTR, 조회수, 시청시간 등 모든 애널리틱스 데이터 수집
- **엑셀 출력**: 썸네일 이미지가 포함된 완전한 엑셀 파일 생성

## 🛠 빌드 방법

### 사전 요구사항

각 플랫폼에서 Python 3.8+ 이 설치되어 있어야 합니다.

### Windows에서 빌드

```cmd
# 1. 프로젝트 폴더로 이동
cd "youtube studio data crawl"

# 2. 빌드 스크립트 실행
build_windows.bat

# 3. 결과물 확인
# dist\YouTubeStudioMonitor.exe 파일이 생성됨
```

### macOS에서 빌드

```bash
# 1. 프로젝트 폴더로 이동
cd "youtube studio data crawl"

# 2. 빌드 스크립트 실행 권한 부여
chmod +x build_mac_linux.sh

# 3. 빌드 스크립트 실행
./build_mac_linux.sh

# 4. 결과물 확인
# dist/YouTubeStudioMonitor 파일이 생성됨
# 옵션으로 YouTubeStudioMonitor.app 번들도 생성 가능
```

### Linux에서 빌드

```bash
# 1. 프로젝트 폴더로 이동
cd "youtube studio data crawl"

# 2. 빌드 스크립트 실행 권한 부여
chmod +x build_mac_linux.sh

# 3. 빌드 스크립트 실행
./build_mac_linux.sh

# 4. 결과물 확인
# dist/YouTubeStudioMonitor 파일이 생성됨
```

## 📦 배포용 패키지 구성

빌드 완료 후 다음과 같이 배포할 수 있습니다:

### Windows용 배포
```
YouTubeStudioMonitor_Windows/
├── YouTubeStudioMonitor.exe    # 실행 파일
├── 사용법.txt                  # 사용 설명서
└── README.txt                  # 간단한 설명
```

### macOS용 배포
```
YouTubeStudioMonitor_macOS/
├── YouTubeStudioMonitor        # 실행 파일 (터미널용)
├── YouTubeStudioMonitor.app/   # 앱 번들 (더블클릭용)
├── 사용법.txt                  # 사용 설명서
└── README.txt                  # 간단한 설명
```

### Linux용 배포
```
YouTubeStudioMonitor_Linux/
├── YouTubeStudioMonitor        # 실행 파일
├── install.sh                  # 설치 스크립트 (선택사항)
├── 사용법.txt                  # 사용 설명서
└── README.txt                  # 간단한 설명
```

## 🚀 사용 방법 (최종 사용자용)

### 1. Chrome 설치 확인
- Google Chrome이 설치되어 있어야 합니다
- Chrome이 없으면 [여기](https://www.google.com/chrome/)에서 다운로드

### 2. 프로그램 실행

**Windows:**
```cmd
YouTubeStudioMonitor.exe
```

**macOS:**
```bash
# 터미널에서:
./YouTubeStudioMonitor

# 또는 Finder에서:
YouTubeStudioMonitor.app 더블클릭
```

**Linux:**
```bash
./YouTubeStudioMonitor
```

### 3. 데이터 수집 과정

1. **Chrome 자동 실행**: 프로그램이 Chrome을 디버그 모드로 실행
2. **로그인**: 원하는 Google 계정으로 YouTube Studio에 로그인
3. **채널 선택**: YouTube Studio에서 수집할 채널 선택
4. **수집 시작**: 터미널에서 엔터 키를 누르면 자동 수집 시작
5. **결과 확인**: 완료 후 엑셀 파일이 현재 폴더에 생성됨

## 🔧 고급 설정

### Chrome 포트 변경
기본 포트(9222)가 사용 중인 경우:
```python
# once.py 파일 수정
monitor = YouTubeStudioMonitor(chrome_port=9223)
```

### 수집 시간 조정
```python
# once.py 파일의 start_monitoring 호출 부분 수정
monitor.start_monitoring(600)  # 10분으로 연장
```

## 📋 파일 구조

```
프로젝트/
├── once.py                     # 메인 소스코드
├── requirements.txt            # 파이썬 의존성
├── build_config.spec           # PyInstaller 설정
├── build_windows.bat           # Windows 빌드 스크립트
├── build_mac_linux.sh          # macOS/Linux 빌드 스크립트
├── README_BUILD.md             # 이 파일
└── dist/                       # 빌드 결과물 폴더
    └── YouTubeStudioMonitor*   # 실행 파일
```

## ❓ 문제 해결

### 빌드 실패
1. Python 3.8+ 설치 확인
2. 의존성 설치: `pip install -r requirements.txt`
3. PyInstaller 설치: `pip install pyinstaller`

### 실행 파일 실행 실패
1. Chrome 설치 확인
2. 바이러스 백신 소프트웨어 예외 처리
3. 관리자 권한으로 실행 시도

### macOS 보안 경고
```bash
# Gatekeeper 허용
sudo spctl --add YouTubeStudioMonitor
xattr -dr com.apple.quarantine YouTubeStudioMonitor
```

### Chrome 찾을 수 없음 오류
- Chrome이 설치되어 있는지 확인
- 비표준 경로에 설치된 경우 소스코드에서 경로 추가

## 📞 지원

문제가 발생하면 다음을 확인해주세요:

1. **로그 파일**: 실행 중 생성되는 에러 메시지
2. **시스템 정보**: OS 버전, Chrome 버전
3. **실행 환경**: 관리자 권한, 방화벽 설정

## 📝 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제공됩니다.
YouTube의 이용약관을 준수하여 사용해주세요. 