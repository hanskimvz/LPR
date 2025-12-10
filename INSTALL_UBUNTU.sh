#!/bin/bash
# Ubuntu 20.04 자동 설치 스크립트
# 차량 번호판 인식 시스템 (LPR)

set -e  # 오류 발생 시 중단

echo "=========================================="
echo "  LPR 시스템 설치 스크립트 (Ubuntu 20.04)"
echo "=========================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 시스템 업데이트
echo -e "${YELLOW}[1/5] 시스템 업데이트 중...${NC}"
sudo apt update
sudo apt upgrade -y

# 2. Python 및 개발 도구 설치
echo -e "${YELLOW}[2/5] Python 및 개발 도구 설치 중...${NC}"
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential

# 3. OpenCV 의존성 설치
echo -e "${YELLOW}[3/5] OpenCV 의존성 설치 중...${NC}"
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev

# 4. Python 버전 확인
echo -e "${YELLOW}[4/5] Python 버전 확인...${NC}"
python3 --version

# 5. 가상환경 생성
echo -e "${YELLOW}[5/5] 가상환경 생성 중...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}가상환경이 이미 존재합니다. 삭제하고 다시 생성합니다.${NC}"
    rm -rf venv
fi

python3 -m venv venv

echo ""
echo -e "${GREEN}✓ 시스템 패키지 설치 완료!${NC}"
echo ""
echo "다음 단계:"
echo "  1. 가상환경 활성화:"
echo -e "     ${GREEN}source venv/bin/activate${NC}"
echo ""
echo "  2. Python 패키지 설치 (CPU 버전 - Python 3.8 호환):"
echo -e "     ${GREEN}pip install --upgrade pip && \\${NC}"
echo -e "     ${GREEN}pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1 && \\${NC}"
echo -e "     ${GREEN}pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu && \\${NC}"
echo -e "     ${GREEN}pip install easyocr opencv-python-headless numpy Pillow scipy${NC}"
echo ""
echo "  3. 실행:"
echo -e "     ${GREEN}python main.py --image test.jpg${NC}"
echo ""
echo -e "${GREEN}설치가 완료되었습니다!${NC}"

