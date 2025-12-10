#!/usr/bin/env python3
"""
EasyOCR을 사용한 차량 번호판 인식 시스템
"""

import argparse
import os, time
from lpr_detector import LicensePlateDetector


def main():
    parser = argparse.ArgumentParser(description='차량 번호판 인식 시스템 (EasyOCR)')
    parser.add_argument('--image', type=str, help='인식할 이미지 파일 경로')
    parser.add_argument('--video', type=str, help='인식할 비디오 파일 경로 (웹캠: 0)')
    parser.add_argument('--output', type=str, help='결과 저장 경로 (비디오만 해당)')
    parser.add_argument('--lang', type=str, default='ko,en', 
                       help='인식 언어 (쉼표로 구분, 기본값: ko,en)')
    parser.add_argument('--gpu', action='store_true', help='GPU 사용 (기본값: CPU)')
    parser.add_argument('--no-display', action='store_true', help='이미지 표시 안함 (서버 환경)')
    
    args = parser.parse_args()
    
    # 언어 리스트 생성
    languages = args.lang.split(',')
    
    # 탐지기 초기화
    print("=" * 50)
    print("차량 번호판 인식 시스템 (EasyOCR)")
    print("=" * 50)
    
    detector = LicensePlateDetector(languages=languages, gpu=args.gpu)
    
    # 이미지 처리
    if args.image:
        if not os.path.exists(args.image):
            print(f"오류: 이미지 파일을 찾을 수 없습니다: {args.image}")
            return
        
        print(f"\n이미지 처리 중: {args.image}")
        start_time = time.time()
        results = detector.process_image(args.image, show_result=not args.no_display)
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n처리 시간: {processing_time:.2f}초")
        
        if results:
            print("\n[인식 결과]")
            print("-" * 50)
            for i, result in enumerate(results, 1):
                print(f"{i}. 번호판: {result['text']}")
                print(f"   원본 텍스트: {result['original_text']}")
                print(f"   신뢰도: {result['confidence']:.2%}")
                if result['region']:
                    x, y, w, h = result['region']
                    print(f"   위치: ({x}, {y}) 크기: {w}x{h}")
                print()
        else:
            print("\n번호판을 인식하지 못했습니다.")
    
    # 비디오/스트림 처리
    elif args.video:
        video_path = args.video if args.video != '0' else 0
        
        # RTSP/HTTP 스트림이 아닌 경우에만 파일 존재 여부 확인
        if video_path != 0 and not (isinstance(video_path, str) and 
                                    (video_path.startswith('rtsp://') or 
                                     video_path.startswith('http://') or 
                                     video_path.startswith('https://'))):
            if not os.path.exists(args.video):
                print(f"오류: 비디오 파일을 찾을 수 없습니다: {args.video}")
                return
        
        if video_path == 0:
            print("\n웹캠 모드로 실행 중...")
        elif isinstance(video_path, str) and video_path.startswith('rtsp://'):
            print(f"\nRTSP 스트림 연결 중: {args.video}")
        else:
            print(f"\n비디오 처리 중: {args.video}")
        
        detector.process_video(video_path, args.output, show_display=not args.no_display)
        
        if args.output:
            print(f"\n결과가 저장되었습니다: {args.output}")
    
    else:
        print("\n오류: --image 또는 --video 옵션을 지정해야 합니다.")
        parser.print_help()


if __name__ == '__main__':
    main()

