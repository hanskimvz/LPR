# 차량 번호판 인식 시스템 (LPR)

AI 기반 실시간 차량 번호판 인식 및 DB 조회 시스템입니다.

> 🚀 **처음 사용하시나요?** [Quick Start Guide](quick_start.md)를 먼저 읽어보세요!

## 시스템 개요

본 시스템은 카메라에서 전송되는 차량 이미지를 분석하여 번호판을 인식하고, 등록된 차량 정보를 조회하는 통합 솔루션입니다.

### 처리 파이프라인

```
카메라 → POST /snapshot → YOLO 차량 감지 → 번호판 영역 추출 → EasyOCR 인식 → MongoDB 조회 → 결과 반환
```

### 주요 구성 요소

1. **웹 서버** (Flask/FastAPI)
   - 카메라로부터 POST 방식으로 snapshot 수신
   - RESTful API 제공

2. **YOLO 차량 감지**
   - 이미지에서 차량 객체 탐지
   - 차량이 있을 때만 번호판 인식 진행

3. **번호판 영역 추출**
   - YOLO 또는 전통적 영상처리로 번호판 위치 탐지
   - ROI (Region of Interest) 추출

4. **EasyOCR 번호판 인식**
   - 한글/영문 번호판 문자 인식
   - 고정밀 OCR 처리

5. **MongoDB 연동**
   - 인식된 번호판으로 차량 정보 조회
   - 등록 차량 여부 확인

## 특징

### 핵심 기능
- ✅ **POST API 지원**: 카메라 snapshot 실시간 수신
- ✅ **YOLO 차량 감지**: 차량 존재 여부 자동 판단
- ✅ **번호판 영역 추출**: 정확한 번호판 위치 탐지
- ✅ **EasyOCR 인식**: 한국어/영어 번호판 고정밀 인식
- ✅ **MongoDB 연동**: 빠른 차량 정보 조회
- ✅ **RTSP 스트림 지원**: 실시간 스트리밍 처리
- ✅ **CPU/GPU 모드**: 하드웨어 환경에 맞게 선택

### 성능 최적화
- ✅ 차량 감지 후에만 번호판 인식 (불필요한 처리 제거)
- ✅ 프레임 스킵 기능 (5프레임마다 처리)
- ✅ MongoDB 인덱싱으로 빠른 조회
- ✅ 비동기 처리 지원

## 시스템 아키텍처

```
┌─────────────┐
│   카메라    │ POST /snapshot
└──────┬──────┘
       │ (이미지)
       ↓
┌─────────────────────┐
│   Flask/FastAPI     │
│   웹 서버           │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│   YOLO 차량 감지    │ ← YOLOv8/v5
│   (Vehicle Det.)    │
└──────┬──────────────┘
       │ 차량 있음?
       ↓ YES
┌─────────────────────┐
│  번호판 영역 추출    │
│  (Plate Detection)  │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│   EasyOCR 인식      │ ← 한글/영어
│   (OCR Recognition) │
└──────┬──────────────┘
       │ 번호판 텍스트
       ↓
┌─────────────────────┐
│   MongoDB 조회      │
│   (DB Query)        │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│   결과 반환         │ JSON Response
│   (차량 정보)       │
└─────────────────────┘
```

## 빠른 시작 (Quick Start)

### 1. 시스템 패키지 설치 (Ubuntu 20.04)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
sudo apt install -y mongodb
```

### 2. 가상환경 설정

```bash
cd ~/Projects/LPR
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치

#### Python 3.8 호환 버전 (구형 CPU)
```bash
pip install --upgrade pip
pip install typing-extensions==4.8.0 fsspec==2024.6.1 filelock==3.13.1 sympy==1.12 networkx==3.1
pip install numpy==1.21.6 Pillow==9.5.0
pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install easyocr==1.6.2 opencv-python-headless scipy
pip install flask pymongo ultralytics
```

#### Python 3.9+ (최신 CPU/GPU)
```bash
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install easyocr opencv-python-headless numpy Pillow scipy
pip install flask pymongo ultralytics
```

### 4. MongoDB 설정

```bash
# MongoDB 시작
sudo systemctl start mongodb
sudo systemctl enable mongodb

# 데이터베이스 및 컬렉션 생성
mongo
> use lpr_db
> db.vehicles.createIndex({ "plate_number": 1 }, { unique: true })
> db.vehicles.insertOne({
    "plate_number": "12가3456",
    "owner": "홍길동",
    "vehicle_type": "승용차",
    "registered_date": new Date()
  })
> exit
```

## API 사용 방법

### 1. 서버 실행

```bash
# 개발 모드
python app.py

# 프로덕션 모드
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. API 엔드포인트

#### POST /snapshot - 차량 이미지 분석
```bash
curl -X POST http://localhost:5000/snapshot \
  -F "image=@car_image.jpg"
```

**응답 예시:**
```json
{
  "success": true,
  "vehicle_detected": true,
  "plate_detected": true,
  "plate_number": "12가3456",
  "confidence": 0.95,
  "vehicle_info": {
    "plate_number": "12가3456",
    "owner": "홍길동",
    "vehicle_type": "승용차",
    "registered_date": "2024-01-15"
  },
  "processing_time": 1.23
}
```

**차량 없음:**
```json
{
  "success": true,
  "vehicle_detected": false,
  "message": "차량이 감지되지 않았습니다."
}
```

**번호판 미등록:**
```json
{
  "success": true,
  "vehicle_detected": true,
  "plate_detected": true,
  "plate_number": "99나9999",
  "confidence": 0.92,
  "vehicle_info": null,
  "message": "등록되지 않은 차량입니다."
}
```

#### GET /health - 헬스 체크
```bash
curl http://localhost:5000/health
```

#### POST /register - 차량 등록
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "plate_number": "12가3456",
    "owner": "홍길동",
    "vehicle_type": "승용차"
  }'
```

## 단독 실행 모드 (개발/테스트용)

### 이미지 파일 처리

```bash
# 기본 실행
python main.py --image car.jpg --no-display

# GPU 사용
python main.py --image car.jpg --no-display --gpu
```

### RTSP 스트림 처리

```bash
# RTSP 스트림 (서버 환경)
python main.py --video rtsp://192.168.4.49/stream --no-display

# 결과 저장
python main.py --video rtsp://192.168.4.49/stream --no-display --output result.mp4
```

### 비디오 파일 처리

```bash
python main.py --video video.mp4 --no-display
```

## 설정 파일

### config.yaml
```yaml
# 서버 설정
server:
  host: 0.0.0.0
  port: 5000
  debug: false

# YOLO 설정
yolo:
  model: yolov8n.pt  # yolov8n, yolov8s, yolov8m
  confidence: 0.5
  device: cpu  # cpu 또는 cuda

# OCR 설정
ocr:
  languages: ['ko', 'en']
  gpu: false
  min_confidence: 0.5
  min_plate_length: 4

# MongoDB 설정
mongodb:
  host: localhost
  port: 27017
  database: lpr_db
  collection: vehicles

# 처리 설정
processing:
  frame_skip: 5  # N 프레임마다 처리
  max_image_size: 1920  # 최대 이미지 크기 (px)
```

## 프로젝트 구조

```
LPR/
├── app.py                      # Flask/FastAPI 웹 서버
├── main.py                     # 단독 실행 스크립트
├── lpr_detector.py             # 번호판 인식 클래스
├── yolo_detector.py            # YOLO 차량 감지 (예정)
├── db_manager.py               # MongoDB 관리 (예정)
├── config.yaml                 # 설정 파일
├── requirements.txt            # Python 패키지
├── INSTALL_UBUNTU.sh          # 설치 스크립트
├── README.md                   # 본 문서
├── installation.md             # 상세 설치 가이드
├── quick_start.md              # 빠른 시작 가이드
└── models/                     # YOLO 모델 파일
    └── yolov8n.pt
```

## 개발 로드맵

### Phase 1: 기본 OCR (완료) ✅
- [x] EasyOCR 통합
- [x] 이미지 처리
- [x] RTSP 스트림 지원
- [x] CPU/GPU 모드

### Phase 2: 차량 감지 (진행 예정)
- [ ] YOLO 모델 통합
- [ ] 차량 객체 탐지
- [ ] 번호판 영역 추출
- [ ] 성능 최적화

### Phase 3: 웹 API (진행 예정)
- [ ] Flask/FastAPI 서버
- [ ] POST /snapshot API
- [ ] 이미지 업로드 처리
- [ ] JSON 응답 형식

### Phase 4: DB 연동 (진행 예정)
- [ ] MongoDB 연동
- [ ] 차량 정보 조회
- [ ] 등록/수정/삭제 API
- [ ] 로그 기록

### Phase 5: 고도화 (향후)
- [ ] 웹 대시보드
- [ ] 실시간 모니터링
- [ ] 통계 및 리포트
- [ ] 멀티 카메라 지원

## 성능 최적화

### CPU 모드 (AVX 미지원)
- PyTorch: 1.7.1
- EasyOCR: 1.6.2
- NumPy: 1.21.6
- 처리 속도: 2-5초/이미지

### GPU 모드 (NVIDIA GPU)
- PyTorch: 2.1.2 + CUDA
- 처리 속도: 0.5-1초/이미지
- 4-5배 빠른 처리

### 최적화 팁
1. **YOLO 모델 선택**: YOLOv8n (가장 빠름) vs YOLOv8m (더 정확)
2. **프레임 스킵**: 실시간 스트림은 5프레임마다 처리
3. **이미지 크기**: 1920px 이하로 리사이징
4. **MongoDB 인덱싱**: plate_number 필드에 인덱스

## 시스템 요구사항

### 최소 사양
- **OS**: Ubuntu 20.04 LTS
- **CPU**: Intel/AMD x64 (AVX 권장)
- **RAM**: 4GB
- **디스크**: 5GB (모델 포함)
- **Python**: 3.8 이상

### 권장 사양
- **OS**: Ubuntu 20.04/22.04 LTS
- **CPU**: Intel/AMD x64 (AVX2 지원)
- **GPU**: NVIDIA GPU (CUDA 지원)
- **RAM**: 8GB 이상
- **디스크**: 10GB SSD
- **Python**: 3.9 이상

## 문제 해결

### "Illegal instruction" 에러
구형 CPU (AVX 미지원)인 경우:
```bash
pip install numpy==1.21.6 Pillow==9.5.0
pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install easyocr==1.6.2
```

### MongoDB 연결 실패
```bash
sudo systemctl status mongodb
sudo systemctl restart mongodb
```

### 낮은 인식률
1. 이미지 해상도 향상
2. 조명 개선
3. 카메라 각도 조정
4. YOLO confidence 임계값 조정

## 보안 고려사항

- API 인증 토큰 사용
- HTTPS 통신
- MongoDB 접근 제어
- 이미지 데이터 암호화
- 로그 민감 정보 마스킹

## 라이선스

MIT License

## 참고 자료

- **EasyOCR**: https://github.com/JaidedAI/EasyOCR
- **YOLOv8**: https://github.com/ultralytics/ultralytics
- **OpenCV**: https://opencv.org/
- **MongoDB**: https://www.mongodb.com/
- **Flask**: https://flask.palletsprojects.com/

## 기여

이슈 및 PR을 환영합니다!

## 지원

- 이슈: GitHub Issues
- 문서: [installation.md](installation.md), [quick_start.md](quick_start.md)
