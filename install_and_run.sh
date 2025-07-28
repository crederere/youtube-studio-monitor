#!/bin/bash

echo "🚀 YouTube Studio Monitor 설치 및 실행"
echo "=========================================="

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3이 설치되지 않았습니다."
    echo "다음 중 하나의 방법으로 Python을 설치해주세요:"
    echo ""
    echo "macOS:"
    echo "  brew install python3"
    echo "  또는 https://www.python.org/downloads/ 에서 설치"
    echo ""
    echo "Linux:"
    echo "  sudo apt install python3 python3-pip  (Ubuntu/Debian)"
    echo "  sudo yum install python3 python3-pip  (CentOS/RHEL)"
    echo ""
    exit 1
fi

echo "✅ Python3 발견: $(python3 --version)"

# pip 설치 확인
if ! command -v pip3 &> /dev/null; then
    echo "pip3을 설치하는 중..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        python3 -m ensurepip --upgrade
    else
        # Linux
        sudo apt update && sudo apt install python3-pip
    fi
fi

echo "✅ pip3 준비 완료"

# 가상환경 생성 (선택사항이지만 권장)
echo "📦 가상환경 설정 중..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
echo "📋 필요한 라이브러리 설치 중..."
pip install -r requirements.txt

# 프로그램 실행
echo "🎯 YouTube Studio Monitor 실행 중..."
echo "=========================================="
python3 once.py

# 실행 완료 후 안내
echo ""
echo "🎉 실행 완료!"
echo ""
echo "다음에 실행할 때는:"
echo "  source venv/bin/activate"
echo "  python3 once.py"
echo ""
echo "또는 이 스크립트를 다시 실행:"
echo "  ./install_and_run.sh" 