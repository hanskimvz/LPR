# 차량 번호판 인식 시스템 (LPR)

EasyOCR을 사용한 한국 차량 번호판 인식 시스템입니다.

> 🚀 **처음 사용하시나요?** [Quick Start Guide](quick_start.md)를 먼저 읽어보세요!

## 특징

- ✅ EasyOCR 기반 고정밀 문자 인식
- ✅ 한국어 및 영문 번호판 지원
- ✅ 이미지 및 비디오 처리 지원
- ✅ 실시간 웹캠 인식 지원
- ✅ CPU 모드로 동작 (GPU 없어도 OK!)
- ✅ GPU 가속 지원 (선택사항)
- ✅ 자동 이미지 전처리 (노이즈 제거, 대비 향상)

## 빠른 시작 (Quick Start) - Ubuntu 20.04

### 방법 1: 자동 설치 스크립트 (추천!) 🚀

```bash
chmod +x INSTALL_UBUNTU.sh
./INSTALL_UBUNTU.sh
source venv/bin/activate
pip install --upgrade pip && \
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1 && \
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu && \
pip install easyocr opencv-python-headless numpy Pillow scipy
```

### 방법 2: 수동 설치

#### 1. 시스템 패키지 설치

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
```

#### 2. 가상환경 생성 및 활성화

```bash
cd ~/Projects/LPR  # 프로젝트 폴더로 이동
python3 -m venv venv
source venv/bin/activate
```

#### 3. Python 패키지 설치 (CPU 모드 - 권장)

```bash
pip install --upgrade pip && \
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1 && \
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu && \
pip install easyocr opencv-python-headless numpy Pillow scipy
```

**참고**: Python 3.8 호환 버전을 사용합니다.

#### 4. 실행

```bash
python main.py --image your_image.jpg
```

> 💡 **도움말**  
> - 처음 사용: [quick_start.md](quick_start.md) - Ubuntu 20.04 5분 빠른 시작  
> - 설치 문제: [installation.md](installation.md) - 상세 설치 가이드 및 문제 해결

## 기본 설정

- **기본 모드**: CPU (GPU 없어도 정상 동작)
- **기본 언어**: 한국어 + 영어
- **GPU 사용**: `--gpu` 옵션 추가 시에만 사용

## 사용 방법

### 이미지에서 번호판 인식

```bash
python main.py --image path/to/image.jpg
```

### 비디오에서 번호판 인식

```bash
python main.py --video path/to/video.mp4
```

결과 저장:
```bash
python main.py --video path/to/video.mp4 --output result.mp4
```

### 웹캠으로 실시간 인식

```bash
python main.py --video 0
```

### 추가 옵션

```bash
# GPU 사용 (CUDA 필요)
python main.py --image image.jpg --gpu

# 영어만 인식
python main.py --image image.jpg --lang en

# 한국어 + 영어 + 중국어 인식
python main.py --image image.jpg --lang ko,en,ch_sim
```

## 지원 언어

EasyOCR이 지원하는 모든 언어를 사용할 수 있습니다:
- `ko` - 한국어
- `en` - 영어
- `ch_sim` - 중국어 간체
- `ja` - 일본어
- 등...

전체 목록: https://www.jaided.ai/easyocr/

## 코드 예제

```python
from lpr_detector import LicensePlateDetector

# CPU 모드로 초기화 (기본값)
detector = LicensePlateDetector(languages=['ko', 'en'], gpu=False)

# GPU 모드로 초기화 (CUDA 필요)
# detector = LicensePlateDetector(languages=['ko', 'en'], gpu=True)

# 이미지 처리
results = detector.process_image('car.jpg', show_result=True)

# 결과 출력
for result in results:
    print(f"번호판: {result['text']}")
    print(f"신뢰도: {result['confidence']:.2%}")
```

## 성능 최적화 팁

1. **CPU vs GPU**: 
   - CPU 모드: 이미지당 2-5초 (대부분의 경우 충분)
   - GPU 모드: 이미지당 0.5-1초 (4-5배 빠름)
2. **비디오 처리**: 기본적으로 5프레임마다 처리합니다 (성능 향상).
3. **이미지 크기**: 너무 큰 이미지는 자동으로 리사이징됩니다.
4. **전처리**: 자동으로 노이즈 제거 및 대비 향상을 수행합니다.

## 문제 해결

### 인식률이 낮을 때
1. 이미지 해상도를 높입니다.
2. 번호판이 선명하게 보이도록 촬영합니다.
3. 조명이 충분한 환경에서 촬영합니다.

### 설치 오류

패키지 설치 시 문제가 발생하면 [installation.md](installation.md)의 "문제 해결" 섹션을 참고하세요.

**CPU 버전 PyTorch 설치 (권장 - Python 3.8 호환)**:
```bash
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu
```

**GPU 버전 PyTorch 설치 (CUDA 11.8 - Python 3.8 호환)**:
```bash
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
```

## 시스템 요구사항

- **OS**: Ubuntu 20.04 LTS
- **Python**: 3.8 이상 (Ubuntu 20.04는 기본 3.8 포함)
- **RAM**: 최소 4GB (8GB 권장)
- **GPU**: 선택사항 (NVIDIA GPU + CUDA, 없어도 CPU로 정상 동작)
- **디스크**: 약 2GB (모델 파일 포함)

## 자주 묻는 질문 (FAQ)

**Q: GPU가 없어도 사용할 수 있나요?**  
A: 네! 기본적으로 CPU 모드로 동작하며, 이미지당 2-5초 정도로 충분히 실용적입니다.

**Q: 가상환경(venv)을 꼭 사용해야 하나요?**  
A: 필수는 아니지만 강력히 권장합니다. 다른 프로젝트와 패키지 충돌을 방지할 수 있습니다.

**Q: 처음 실행이 느려요.**  
A: 처음 실행 시 EasyOCR이 인식 모델(약 100MB)을 자동으로 다운로드합니다. 두 번째 실행부터는 빠릅니다.

**Q: GPU를 사용하고 싶어요.**  
A: NVIDIA 드라이버와 CUDA를 설치한 후 `--gpu` 옵션을 추가하세요:
```bash
nvidia-smi  # GPU 확인
python main.py --image test.jpg --gpu
```

**Q: Ubuntu 서버(헤드리스)에서도 동작하나요?**  
A: 네! `opencv-python-headless`를 사용하면 GUI 없이도 동작합니다. (설치 가이드 참고)

## 라이선스

MIT License

## 참고 자료

- EasyOCR: https://github.com/JaidedAI/EasyOCR
- OpenCV: https://opencv.org/

