import cv2
import easyocr
import numpy as np
from typing import List, Tuple, Optional


class LicensePlateDetector:
    """EasyOCR을 사용한 차량 번호판 인식 클래스"""
    
    def __init__(self, languages: List[str] = ['ko', 'en'], gpu: bool = False):
        """
        Args:
            languages: 인식할 언어 리스트 (기본값: 한국어, 영어)
            gpu: GPU 사용 여부 (기본값: False)
        """
        print("EasyOCR 초기화 중...")
        self.reader = easyocr.Reader(languages, gpu=gpu)
        print(f"EasyOCR 초기화 완료! (GPU: {'사용' if gpu else '미사용'})")
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """이미지 전처리"""
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 노이즈 제거
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # 대비 향상 (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        return enhanced
    
    def detect_license_plate_region(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """번호판 영역 탐지 (간단한 방법)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 에지 검출
        edges = cv2.Canny(gray, 100, 200)
        
        # 윤곽선 찾기
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # 번호판 같은 사각형 찾기
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            if len(approx) == 4:  # 사각형
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)
                
                # 번호판 비율 확인 (대략 2:1 ~ 5:1)
                if 2.0 <= aspect_ratio <= 5.0 and w > 100:
                    return (x, y, w, h)
        
        return None
    
    def recognize_text(self, image: np.ndarray, detail: int = 1) -> List[Tuple[List, str, float]]:
        """
        텍스트 인식
        
        Args:
            image: 입력 이미지
            detail: 0 = 간단한 결과, 1 = 상세한 결과 (기본값)
            
        Returns:
            List of (bbox, text, confidence)
        """
        results = self.reader.readtext(image, detail=detail)
        return results
    
    def filter_plate_number(self, text: str) -> str:
        """번호판 텍스트 필터링 및 정제"""
        # 공백 제거
        text = text.replace(' ', '')
        
        # 특수문자 제거 (한글, 영문, 숫자만 유지)
        filtered = ''.join(c for c in text if c.isalnum() or ord('가') <= ord(c) <= ord('힣'))
        
        return filtered
    
    def process_image(self, image_path: str, show_result: bool = True) -> List[dict]:
        """
        이미지에서 번호판 인식
        
        Args:
            image_path: 이미지 파일 경로
            show_result: 결과를 화면에 표시할지 여부
            
        Returns:
            인식된 번호판 정보 리스트
        """
        # 이미지 로드
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"이미지를 불러올 수 없습니다: {image_path}")
        
        original = image.copy()
        results = []
        
        # 번호판 영역 탐지 시도
        plate_region = self.detect_license_plate_region(image)
        if not results:
            print("번호판 영역을 찾지 못했습니다.")
            return results
        
        if plate_region:
            x, y, w, h = plate_region
            # 여백 추가
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2 * padding)
            h = min(image.shape[0] - y, h + 2 * padding)
            
            plate_image = image[y:y+h, x:x+w]
            
            # 전처리
            processed = self.preprocess_image(plate_image)
            
            # OCR 수행
            ocr_results = self.recognize_text(processed)
            
            for (bbox, text, confidence) in ocr_results:
                if confidence > 0.3:  # 신뢰도 임계값
                    filtered_text = self.filter_plate_number(text)
                    if len(filtered_text) >= 4:  # 최소 4자 이상
                        results.append({
                            'text': filtered_text,
                            'original_text': text,
                            'confidence': confidence,
                            'bbox': bbox,
                            'region': (x, y, w, h)
                        })
                        
                        # 시각화
                        if show_result:
                            cv2.rectangle(original, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(original, filtered_text, (x, y-10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # 전체 이미지에서 OCR 수행 (백업)
        if not results:
            print("번호판 영역을 찾지 못했습니다. 전체 이미지에서 OCR 수행...")
            preprocessed = self.preprocess_image(image)
            ocr_results = self.recognize_text(preprocessed)
            
            for (bbox, text, confidence) in ocr_results:
                if confidence > 0.5:
                    filtered_text = self.filter_plate_number(text)
                    if len(filtered_text) >= 4:
                        results.append({
                            'text': filtered_text,
                            'original_text': text,
                            'confidence': confidence,
                            'bbox': bbox,
                            'region': None
                        })
                        
                        # 시각화
                        if show_result:
                            points = np.array(bbox, dtype=np.int32)
                            cv2.polylines(original, [points], True, (0, 0, 255), 2)
                            cv2.putText(original, filtered_text, tuple(points[0]),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # 결과 표시
        if show_result and len(results) > 0:
            # 이미지 크기 조정 (화면에 맞게)
            height, width = original.shape[:2]
            if width > 1200:
                scale = 1200 / width
                new_width = 1200
                new_height = int(height * scale)
                original = cv2.resize(original, (new_width, new_height))
            
            cv2.imshow('License Plate Recognition', original)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return results
    
    def process_video(self, video_path: str, output_path: Optional[str] = None, show_display: bool = True):
        """
        비디오/RTSP 스트림에서 번호판 인식
        
        Args:
            video_path: 비디오 파일 경로, 웹캠(0), 또는 RTSP URL (rtsp://...)
            output_path: 결과 저장 경로 (선택사항)
            show_display: 화면 표시 여부 (서버 환경에서는 False)
        """
        # RTSP, HTTP 스트림, 웹캠, 또는 파일 경로 처리
        if video_path == '0' or video_path == 0:
            print("웹캠 연결 중...")
            cap = cv2.VideoCapture(0)
        elif video_path.startswith('rtsp://') or video_path.startswith('http://') or video_path.startswith('https://'):
            print(f"스트림 연결 중: {video_path}")
            cap = cv2.VideoCapture(video_path)
            # RTSP 스트림을 위한 버퍼 설정 (지연 감소)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        else:
            print(f"비디오 파일 열기: {video_path}")
            cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"비디오/스트림을 열 수 없습니다: {video_path}")
        
        # 비디오 정보
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps == 0 or fps is None:
            fps = 25  # RTSP 스트림의 경우 기본값
            print(f"FPS를 감지할 수 없어 기본값({fps})을 사용합니다.")
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"스트림 정보: {width}x{height} @ {fps}fps")
        
        # 비디오 작성기
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        process_every_n_frames = 5  # 5프레임마다 처리 (성능 향상)
        last_detected_text = ""
        
        print("스트림 처리 중... (Ctrl+C 또는 ESC 키를 눌러 종료)")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("스트림 읽기 실패 또는 종료")
                    break
                
                frame_count += 1
                
                # N 프레임마다만 처리
                if frame_count % process_every_n_frames == 0:
                    # 번호판 영역 탐지
                    plate_region = self.detect_license_plate_region(frame)
                    
                    if plate_region:
                        x, y, w, h = plate_region
                        plate_image = frame[y:y+h, x:x+w]
                        
                        # 전처리 및 OCR
                        processed = self.preprocess_image(plate_image)
                        ocr_results = self.recognize_text(processed)
                        
                        for (bbox, text, confidence) in ocr_results:
                            if confidence > 0.5:
                                filtered_text = self.filter_plate_number(text)
                                if len(filtered_text) >= 4:
                                    # 결과 표시
                                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                    cv2.putText(frame, filtered_text, (x, y-10),
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                                    
                                    # 새로운 번호판이 감지되면 출력
                                    if filtered_text != last_detected_text:
                                        print(f"Frame {frame_count}: {filtered_text} (신뢰도: {confidence:.2f})")
                                        last_detected_text = filtered_text
                
                # 화면 표시 (show_display가 True일 때만)
                if show_display:
                    cv2.imshow('License Plate Recognition - Video', frame)
                
                # 결과 저장
                if writer:
                    writer.write(frame)
                
                # ESC 키로 종료 (화면 표시 중일 때만)
                if show_display and cv2.waitKey(1) & 0xFF == 27:
                    break
        
        except KeyboardInterrupt:
            print("\n사용자에 의해 중단되었습니다.")
        finally:
            # 정리
            cap.release()
            if writer:
                writer.release()
            if show_display:
                cv2.destroyAllWindows()
            
            print(f"\n스트림 처리 완료! (총 {frame_count} 프레임 처리)")

