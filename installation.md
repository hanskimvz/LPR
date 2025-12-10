# 설치 가이드 (Installation Guide)

Ubuntu 20.04 기준 차량 번호판 인식 시스템의 상세 설치 방법을 설명합니다.

## 목차
- [시스템 요구사항](#시스템-요구사항)
- [시스템 패키지 설치](#시스템-패키지-설치)
- [가상환경 설정 (venv)](#가상환경-설정-venv)
- [Python 패키지 설치](#python-패키지-설치)
- [설치 확인](#설치-확인)
- [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 필수 요구사항
- **OS**: Ubuntu 20.04 LTS
- **Python**: 3.8 이상 (Ubuntu 20.04는 기본 3.8 포함)
- **RAM**: 최소 4GB (8GB 권장)
- **디스크 공간**: 약 2GB (모델 파일 포함)

### 선택 요구사항
- **GPU**: NVIDIA GPU + CUDA (선택사항, 없어도 CPU로 정상 동작)
- **웹캠**: 실시간 인식을 사용할 경우

---

## 시스템 패키지 설치

Ubuntu 20.04에서 필요한 시스템 패키지를 먼저 설치합니다.

### 1. 시스템 업데이트

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Python 및 개발 도구 설치

```bash
# Python3 및 pip 설치
sudo apt install -y python3 python3-pip python3-venv python3-dev

# 빌드 도구 설치
sudo apt install -y build-essential

# OpenCV 의존성 설치
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
```

### 3. Python 버전 확인

```bash
python3 --version
# Python 3.8.x 이상이어야 합니다
```

---

## 가상환경 설정 (venv)

가상환경을 사용하면 프로젝트별로 독립적인 Python 환경을 유지할 수 있습니다.

### 1. 프로젝트 폴더로 이동

```bash
cd ~/Projects/LPR
# 또는 실제 프로젝트 경로로 이동
```

### 2. 가상환경 생성

```bash
python3 -m venv venv
```

### 3. 가상환경 활성화

```bash
source venv/bin/activate
```

활성화되면 프롬프트 앞에 `(venv)`가 표시됩니다:
```
(venv) user@ubuntu:~/Projects/LPR$
```

### 4. 가상환경 비활성화 (작업 완료 후)

```bash
deactivate
```

### 5. 자동 활성화 설정 (선택사항)

매번 활성화하기 귀찮다면 `.bashrc`에 추가:

```bash
echo "alias lpr='cd ~/Projects/LPR && source venv/bin/activate'" >> ~/.bashrc
source ~/.bashrc

# 이제 어디서나 'lpr' 명령으로 바로 시작!
```

---

## Python 패키지 설치

가상환경을 **활성화한 상태**에서 진행하세요!

### 방법 1: CPU 전용 설치 (GPU 없음) ⭐ 권장

대부분의 경우 CPU 모드로 충분히 빠르게 작동합니다.

```bash
# pip 업그레이드
python -m pip install --upgrade pip

# Python 3.8 호환 의존성 먼저 설치
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1

# CPU 버전 PyTorch 설치 (Python 3.8 호환)
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu

# 나머지 패키지 설치
pip install easyocr opencv-python-headless numpy Pillow scipy

# 또는 opencv-python (GUI가 필요한 경우)
# pip install opencv-python
```

**참고**: 
- Ubuntu 20.04는 Python 3.8이 기본이므로 PyTorch 2.1 버전을 사용합니다.
- Python 3.8 호환을 위해 여러 의존성 버전을 명시합니다 (typing-extensions 4.8.0, fsspec 2024.6.1, filelock 3.13.1, sympy 1.12, networkx 3.1).
- Ubuntu 서버 환경이면 `opencv-python-headless` 사용을 권장합니다.

### 방법 2: GPU 지원 설치 (CUDA 필요)

NVIDIA GPU와 CUDA가 설치되어 있는 경우에만 사용하세요.

#### 2-1. CUDA 설치 확인

```bash
# NVIDIA 드라이버 및 CUDA 버전 확인
nvidia-smi

# CUDA 버전이 표시되면 GPU 사용 가능
```

CUDA가 설치되어 있지 않다면:
```bash
# NVIDIA 드라이버 설치 (Ubuntu 20.04)
sudo apt install -y nvidia-driver-470
sudo reboot

# 재부팅 후 확인
nvidia-smi
```

#### 2-2. GPU 버전 PyTorch 설치

**CUDA 11.8 버전 (Python 3.8 호환):**
```bash
pip install --upgrade pip
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
pip install easyocr opencv-python-headless numpy Pillow scipy
```

**CUDA 12.1 버전 (Python 3.9+ 필요):**
```bash
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install easyocr opencv-python-headless numpy Pillow scipy
```

**참고**: Python 3.8 사용 시 PyTorch 2.1 버전을 사용해야 합니다. 최신 PyTorch는 Python 3.9 이상이 필요합니다.

### 방법 3: 한 줄 설치 스크립트 (추천!)

간편하게 한 번에 설치 (Python 3.8 호환):

```bash
# CPU 버전 (가장 추천 - Python 3.8 호환)
pip install --upgrade pip && \
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1 && \
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu && \
pip install easyocr opencv-python-headless numpy Pillow scipy

# GPU 버전 (CUDA 11.8 - Python 3.8 호환)
pip install --upgrade pip && \
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1 && \
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118 && \
pip install easyocr opencv-python-headless numpy Pillow scipy
```

---

## 설치 확인

### 1. Python 패키지 확인
```bash
pip list
```

다음 패키지들이 설치되어 있어야 합니다:
- easyocr
- opencv-python
- numpy
- Pillow
- torch
- torchvision
- scipy

### 2. 간단한 테스트 실행

```bash
python -c "import easyocr; import cv2; import torch; print('설치 성공!')"
```

오류 없이 "설치 성공!"이 출력되면 정상입니다.

### 3. PyTorch GPU 확인 (GPU 설치 시에만)

```bash
python -c "import torch; print(f'CUDA 사용 가능: {torch.cuda.is_available()}')"
```

---

## 첫 실행 (모델 다운로드)

처음 실행할 때 EasyOCR이 자동으로 인식 모델을 다운로드합니다.

```bash
python main.py --image test.jpg
```

다운로드되는 모델:
- 한국어 인식 모델: ~40MB
- 영어 인식 모델: ~40MB
- 텍스트 탐지 모델: ~35MB

**인터넷 연결이 필요하며**, 모델은 `~/.EasyOCR/model/` 폴더에 저장됩니다.

---

## 문제 해결 (Ubuntu 20.04)

### ❌ "python3: command not found"

Python이 설치되지 않았습니다.

**해결방법**:
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### ❌ "venv: command not found" 또는 가상환경 생성 실패

python3-venv 패키지가 필요합니다.

**해결방법**:
```bash
sudo apt install -y python3-venv
python3 -m venv venv
```

### ❌ pip install 시 "error: command 'gcc' failed"

빌드 도구가 설치되지 않았습니다.

**해결방법**:
```bash
sudo apt install -y build-essential python3-dev
pip install --upgrade pip
# 다시 패키지 설치 시도
```

### ❌ OpenCV 관련 "libGL.so.1: cannot open shared object file"

OpenCV 의존성이 없습니다.

**해결방법**:
```bash
sudo apt install -y libgl1-mesa-glx libglib2.0-0
# 또는 headless 버전 사용
pip uninstall opencv-python
pip install opencv-python-headless
```

### ❌ "No module named 'cv2'" 오류

OpenCV가 제대로 설치되지 않았습니다.

**해결방법**:
```bash
# 시스템 의존성 먼저 설치
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev

# OpenCV 재설치
pip uninstall opencv-python opencv-python-headless
pip install opencv-python-headless
```

### ❌ PyTorch 설치 시 "ERROR: Package 'typing-extensions' requires a different Python"

최신 PyTorch가 Python 버전과 호환되지 않습니다.

**해결방법 (Python 3.8 사용 시)**:
```bash
# Python 3.8 호환 버전 설치 (의존성 포함)
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu
```

**Python 버전 확인**:
```bash
python --version
# Python 3.8.x → PyTorch 2.1 사용
# Python 3.9+ → 최신 PyTorch 사용 가능
```

### ❌ 메모리 부족 오류

RAM이 부족합니다.

**해결방법**:
1. 다른 프로그램 종료
2. 이미지 크기 줄이기
3. 비디오 처리 시 프레임 스킵 간격 늘리기 (코드 수정 필요)

### ❌ "Permission denied" 오류

파일 권한 문제입니다.

**해결방법**:
```bash
# 실행 권한 추가
chmod +x main.py

# 또는 python3로 직접 실행
python3 main.py --image test.jpg

# venv 폴더 권한 문제인 경우
sudo chown -R $USER:$USER venv/
```

### ❌ pip install 시 "Permission denied"

sudo 없이 설치하거나 가상환경을 사용하세요.

**해결방법**:
```bash
# 가상환경 사용 (권장)
source venv/bin/activate
pip install <패키지명>

# 또는 사용자 디렉토리에 설치
pip install --user <패키지명>
```

### ❌ GPU가 인식되지 않음

CUDA 또는 NVIDIA 드라이버 문제입니다.

**해결방법**:

1. **NVIDIA 드라이버 확인:**
```bash
nvidia-smi
# 명령어가 없거나 오류 → 드라이버 설치 필요
```

2. **드라이버 설치 (Ubuntu 20.04):**
```bash
# 추천 드라이버 확인
ubuntu-drivers devices

# 자동 설치
sudo ubuntu-drivers autoinstall

# 또는 특정 버전 설치
sudo apt install -y nvidia-driver-470

# 재부팅 필요
sudo reboot
```

3. **CUDA 버전 확인:**
```bash
nvidia-smi
# 우측 상단에 CUDA Version 표시됨

# PyTorch CUDA 버전과 일치하는지 확인
python -c "import torch; print(torch.version.cuda)"
```

4. **여전히 안 되면 CPU 모드 사용 (충분히 빠름)**

### ❌ EasyOCR 모델 다운로드 실패

인터넷 연결이나 방화벽 문제입니다.

**해결방법**:
1. 인터넷 연결 확인
2. 방화벽/프록시 설정 확인
3. 수동으로 모델 다운로드:
   - https://github.com/JaidedAI/EasyOCR/releases
   - 모델을 `~/.EasyOCR/model/` 폴더에 복사

---

## 패키지 버전 고정 (선택사항)

개발 환경을 그대로 유지하고 싶다면:

```bash
# 현재 설치된 패키지 버전 저장
pip freeze > requirements-lock.txt

# 나중에 똑같은 버전으로 설치
pip install -r requirements-lock.txt
```

---

## 가상환경 삭제

프로젝트를 완전히 제거하고 싶다면:

```bash
# 가상환경 비활성화 (활성화된 경우)
deactivate

# venv 폴더 삭제
rm -rf venv

# EasyOCR 모델 캐시도 삭제 (선택사항)
rm -rf ~/.EasyOCR/
```

---

## 추가 정보

### 가상환경을 매번 활성화하기 귀찮으신가요?

**VS Code (Ubuntu):**
1. `Ctrl + Shift + P`
2. "Python: Select Interpreter" 선택
3. `./venv/bin/python` 선택
4. 이후 VS Code 터미널이 자동으로 가상환경 활성화

**PyCharm (Ubuntu):**
1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing Environment
3. `./venv/bin/python` 선택

**Bash 별칭 사용:**
```bash
# ~/.bashrc에 추가
echo "alias lpr='cd ~/Projects/LPR && source venv/bin/activate'" >> ~/.bashrc
source ~/.bashrc

# 이제 'lpr' 명령으로 바로 시작
```

### CPU vs GPU 성능 비교

- **CPU 모드**: 이미지당 약 2-5초 (충분히 실용적)
- **GPU 모드**: 이미지당 약 0.5-1초 (4-5배 빠름)

대부분의 경우 CPU 모드로도 충분합니다!

---

## 도움이 필요하신가요?

문제가 계속되면:
1. Python 버전 확인: `python --version`
2. OS 확인: Windows / Linux / macOS
3. 오류 메시지 전체 복사
4. GitHub Issues에 문의

---

**설치가 완료되었다면 [README.md](README.md)로 돌아가서 사용 방법을 확인하세요!** 🚀

