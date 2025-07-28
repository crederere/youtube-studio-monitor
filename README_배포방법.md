# YouTube Studio Monitor - 배포 방법 가이드

## 🎯 배포 옵션 비교

| 방법 | 장점 | 단점 | 권장 대상 |
|------|------|------|-----------|
| **실행 파일 빌드** | 파이썬 불필요, 더블클릭 실행 | 각 플랫폼에서 빌드 필요 | 일반 사용자 |
| **GitHub Actions** | 자동으로 모든 플랫폼 빌드 | GitHub 계정 필요 | 개발자 |
| **파이썬 소스코드** | 별도 빌드 불필요 | 파이썬 설치 필요 | 개발자/고급 사용자 |

## 📦 방법 1: 실행 파일 빌드 (권장)

### ✅ 각 플랫폼에서 직접 빌드

**Windows에서:**
```cmd
build_windows.bat
→ dist\YouTubeStudioMonitor.exe 생성
```

**macOS에서:**
```bash
chmod +x build_mac_linux.sh
./build_mac_linux.sh
→ dist/YouTubeStudioMonitor 생성
→ YouTubeStudioMonitor.app 생성 (옵션)
```

**Linux에서:**
```bash
chmod +x build_mac_linux.sh  
./build_mac_linux.sh
→ dist/YouTubeStudioMonitor 생성
```

### 📁 배포 패키지 구성

```
배포폴더/
├── YouTubeStudioMonitor_Windows/
│   ├── YouTubeStudioMonitor.exe
│   ├── 간단사용법.txt
│   └── README_BUILD.md
├── YouTubeStudioMonitor_macOS/
│   ├── YouTubeStudioMonitor
│   ├── YouTubeStudioMonitor.app/
│   ├── 간단사용법.txt
│   └── README_BUILD.md
└── YouTubeStudioMonitor_Linux/
    ├── YouTubeStudioMonitor
    ├── 간단사용법.txt
    └── README_BUILD.md
```

## 🤖 방법 2: GitHub Actions 자동 빌드

### 설정 방법

1. **GitHub 저장소 생성**
2. **코드 업로드** (`.github/workflows/build.yml` 포함)
3. **Actions 탭에서 수동 실행** 또는 **코드 푸시**

### 사용법

```bash
# 1. GitHub에 푸시
git add .
git commit -m "Add cross-platform build"
git push origin main

# 2. GitHub Actions에서 자동 빌드
# - Windows, macOS, Linux 버전 동시 생성
# - 5-10분 후 Artifacts에서 다운로드 가능

# 3. 배포 패키지 자동 생성
# - YouTubeStudioMonitor_Windows.tar.gz
# - YouTubeStudioMonitor_macOS.tar.gz  
# - YouTubeStudioMonitor_Linux.tar.gz
```

### 장점
- ✅ **무료**: GitHub Actions는 public 저장소에서 무료
- ✅ **자동화**: 코드 변경시 자동 빌드
- ✅ **모든 플랫폼**: Windows, macOS, Linux 동시 빌드
- ✅ **클라우드**: 로컬 환경 불필요

## 🐍 방법 3: 파이썬 소스코드 배포

### 배포 패키지

```
YouTubeStudioMonitor_Source/
├── once.py                    # 메인 소스코드
├── requirements.txt           # 의존성 목록
├── install_and_run.sh         # macOS/Linux용 설치 스크립트
├── install_and_run.bat        # Windows용 설치 스크립트 (추가 필요)
├── 간단사용법.txt
└── README_BUILD.md
```

### 사용법

**macOS/Linux:**
```bash
chmod +x install_and_run.sh
./install_and_run.sh
```

**Windows:**
```cmd
python -m pip install -r requirements.txt
python once.py
```

### 장점
- ✅ **간단**: 별도 빌드 불필요
- ✅ **크기**: 파일 크기 작음
- ✅ **수정 가능**: 소스코드 직접 수정 가능

### 단점
- ❌ **파이썬 필요**: 사용자가 파이썬 설치해야 함
- ❌ **복잡**: 일반 사용자에게는 어려움

## 🎯 권장 배포 전략

### 일반 사용자용 (추천)
```
GitHub Actions 사용
↓
모든 플랫폼 실행파일 자동 생성
↓  
플랫폼별 패키지로 배포
```

### 개발자/고급 사용자용
```
소스코드 + install_and_run.sh
↓
각자 환경에서 직접 실행
```

### 하이브리드 접근
```
배포 페이지에서 두 옵션 모두 제공:
1. 실행파일 다운로드 (일반 사용자)
2. 소스코드 다운로드 (개발자)
```

## 🔧 GitHub Actions 활용 팁

### 수동 빌드 실행
1. GitHub 저장소 → **Actions** 탭
2. **Build YouTube Studio Monitor** 워크플로우 선택
3. **Run workflow** 버튼 클릭

### 릴리즈 태그로 자동 배포
```bash
git tag v1.0.0
git push origin v1.0.0
# → 자동으로 릴리즈 패키지 생성
```

### Artifacts 다운로드
1. 빌드 완료 후 **Artifacts** 섹션에서 다운로드
2. 각 플랫폼별 파일 확인
3. 압축 해제 후 배포

## 📝 배포 체크리스트

- [ ] **모든 플랫폼 테스트** (Windows, macOS, Linux)
- [ ] **Chrome 경로 탐지** 확인
- [ ] **간단사용법.txt** 업데이트
- [ ] **README 파일** 포함
- [ ] **바이러스 검사** (실행파일의 경우)
- [ ] **디지털 서명** (고급 배포시)

---

💡 **추천**: GitHub Actions로 시작해서 자동 빌드 시스템을 구축한 후, 각 플랫폼별 패키지를 배포하는 것이 가장 효율적입니다! 