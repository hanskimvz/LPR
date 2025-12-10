# 빠른 시작 가이드 (Quick Start) - Ubuntu 20.04

5분 안에 차량 번호판 인식 시스템을 실행해보세요! 🚀

## 전제 조건

- Ubuntu 20.04 LTS
- 인터넷 연결 필요 (모델 다운로드용)
- sudo 권한 (시스템 패키지 설치용)

---

## Ubuntu 20.04 설치 가이드

### 1단계: 시스템 패키지 설치

터미널을 열고 다음 명령어를 실행하세요:

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 및 필수 도구 설치
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential

# OpenCV 의존성 설치
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
```

설치 시간: 약 2-3분

### 2단계: 프로젝트 폴더로 이동

```bash
cd ~/Projects/LPR
# 또는 실제 프로젝트 경로로 이동
```

### 3단계: 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```

성공하면 `(venv)`가 프롬프트 앞에 표시됩니다:
```
(venv) user@ubuntu:~/Projects/LPR$
```

### 4단계: Python 패키지 설치

**CPU 버전 (권장 - GPU 없어도 OK!):**

```bash
pip install --upgrade pip && \
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1 && \
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu && \
pip install easyocr opencv-python-headless numpy Pillow scipy
```

설치 시간: 약 3-5분

**참고**: Ubuntu 20.04의 기본 Python 3.8과 호환되는 버전을 사용합니다.

**GPU 버전 (NVIDIA GPU가 있는 경우):**

```bash
# NVIDIA 드라이버 확인
nvidia-smi

# GPU 버전 설치 (Python 3.8 호환)
pip install --upgrade pip && \
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1 && \
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118 && \
pip install easyocr opencv-python-headless numpy Pillow scipy
```

### 5단계: 테스트 실행

차량 번호판이 있는 이미지를 준비하고:

```bash
# 기본 실행 (CPU 모드)
python main.py --image test.jpg

# GPU 사용 (GPU가 있는 경우)
python main.py --image test.jpg --gpu
```

처음 실행 시 EasyOCR이 모델을 자동으로 다운로드합니다 (약 100MB, 1-2분 소요)

---

## 사용 예제

### 이미지에서 번호판 인식

```bash
python main.py --image car_image.jpg
```

### 비디오에서 번호판 인식

```bash
python main.py --video video.mp4
```

결과 저장:
```bash
python main.py --video video.mp4 --output result.mp4
```

### 웹캠으로 실시간 인식 (웹캠 있는 경우)

```bash
python main.py --video 0
```

종료하려면 `ESC` 키를 누르세요.

---

## 완료! 🎉

프로그램이 잘 실행되나요? 축하합니다!

이제 다음을 확인해보세요:
- **[README.md](README.md)** - 전체 기능 및 사용법
- **[installation.md](installation.md)** - 상세 설치 가이드 및 문제 해결

---

## 자주하는 실수 (Ubuntu 20.04)

### ❌ "python3: command not found"

**해결**: Python 설치
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version  # 확인
```

### ❌ "No module named 'venv'"

**해결**: python3-venv 패키지 설치
```bash
sudo apt install -y python3-venv
python3 -m venv venv
```

### ❌ pip install 시 "error: command 'gcc' failed"

**해결**: 빌드 도구 설치
```bash
sudo apt install -y build-essential python3-dev
pip install --upgrade pip
# 다시 패키지 설치 시도
```

### ❌ "libGL.so.1: cannot open shared object file"

**해결**: OpenCV 의존성 설치
```bash
sudo apt install -y libgl1-mesa-glx libglib2.0-0
```

또는 headless 버전 사용:
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

### ❌ "Permission denied" 오류

**해결**: 권한 문제
```bash
# 파일 실행 권한 추가
chmod +x main.py

# 또는 python3로 직접 실행
python3 main.py --image test.jpg

# venv 폴더 권한 수정
sudo chown -R $USER:$USER ~/Projects/LPR/
```

### ❌ pip install 시 "Permission denied"

**해결**: 가상환경 사용 (sudo 사용 금지!)
```bash
# 가상환경 활성화 확인
source venv/bin/activate

# 프롬프트에 (venv)가 있는지 확인
# 있으면 sudo 없이 설치
pip install <패키지명>
```

### ❌ 이미지를 찾을 수 없음

**해결**: 파일 경로 확인
```bash
# 현재 폴더의 파일 목록 확인
ls

# 전체 경로 사용
python main.py --image ~/Pictures/car.jpg

# 또는 파일을 프로젝트 폴더로 복사
cp ~/Pictures/car.jpg .
python main.py --image car.jpg
```

### ❌ Display 관련 오류 (서버 환경)

**해결**: headless 모드 또는 X11 forwarding
```bash
# 방법 1: opencv-python-headless 사용
pip uninstall opencv-python
pip install opencv-python-headless

# 방법 2: X11 forwarding (SSH 사용 시)
ssh -X user@server

# 방법 3: 가상 디스플레이 사용
sudo apt install -y xvfb
xvfb-run python main.py --image test.jpg
```

### ❌ 메모리 부족 오류

**해결**: 
```bash
# 메모리 사용량 확인
free -h

# 다른 프로세스 종료
top  # q로 종료

# 스왑 메모리 늘리기 (선택사항)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 가상환경 관리

### 비활성화

작업이 끝나면:
```bash
deactivate
```

### 다음에 다시 사용

```bash
cd ~/Projects/LPR
source venv/bin/activate
```

### 자동 활성화 설정 (편리!)

`.bashrc`에 별칭 추가:
```bash
echo "alias lpr='cd ~/Projects/LPR && source venv/bin/activate'" >> ~/.bashrc
source ~/.bashrc

# 이제 'lpr' 명령으로 바로 시작!
lpr
```

---

## 성능 팁

### CPU vs GPU 비교

- **CPU 모드**: 이미지당 2-5초 (대부분의 경우 충분)
- **GPU 모드**: 이미지당 0.5-1초 (4-5배 빠름)

### GPU 사용하려면?

1. NVIDIA 드라이버 확인:
```bash
nvidia-smi
```

2. GPU 버전 설치 (위의 4단계 GPU 버전 참고)

3. 실행 시 `--gpu` 옵션 추가:
```bash
python main.py --image test.jpg --gpu
```

---

## 추가 도움말

### 서버 환경 (헤드리스)에서 실행

GUI 없는 서버에서는:
```bash
# opencv-python-headless 사용
pip install opencv-python-headless

# 결과를 파일로 저장만 하고 화면에 표시 안 함
# (코드 수정 필요 또는 주석 처리)
```

### 여러 이미지 일괄 처리

```bash
# 간단한 스크립트
for img in ~/images/*.jpg; do
    python main.py --image "$img"
done
```

### 로그 파일 저장

```bash
python main.py --image test.jpg 2>&1 | tee output.log
```

---

## 도움이 필요한가요?

더 자세한 내용은 [installation.md](installation.md)의 "문제 해결" 섹션을 참고하세요!

**행운을 빕니다!** 🚀
