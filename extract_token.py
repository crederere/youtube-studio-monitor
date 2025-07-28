#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import time
import os
from datetime import datetime

def extract_next_page_token():
    """실제 수집된 JSON에서 nextPageToken 추출"""
    
    print("🔍 실제 JSON 파일에서 nextPageToken 추출 중...")
    
    # 최신 비디오 목록 파일
    latest_file = "youtube_videos_list_20250724_142705.json"
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 원본 전체 응답 확인 (parse_and_save_video_data에서 저장된 구조)
        print(f"📂 파일 구조 확인:")
        for key in data.keys():
            print(f"   • {key}: {type(data[key])}")
        
        # 실제 nextPageToken 찾기
        next_token = None
        
        # 여러 위치에서 nextPageToken 찾기
        if 'nextPageToken' in data:
            next_token = data['nextPageToken']
        elif 'original_response' in data and 'nextPageToken' in data['original_response']:
            next_token = data['original_response']['nextPageToken']
        
        if next_token:
            print(f"✅ nextPageToken 발견: {next_token}")
            return next_token, data
        else:
            print(f"❌ nextPageToken을 찾을 수 없습니다.")
            # 전체 데이터 구조 출력 (디버깅용)
            print(f"전체 키들: {list(data.keys())}")
            return None, data
            
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        return None, None

def get_captured_request_info():
    """캡처된 요청 정보 가져오기"""
    
    print("🔍 캡처된 요청 정보 확인 중...")
    
    # 최신 디버그 파일들 찾기
    debug_files = []
    for file in os.listdir('.'):
        if file.startswith('debug_request_') and file.endswith('.json'):
            debug_files.append(file)
    
    if not debug_files:
        print("❌ 디버그 요청 파일을 찾을 수 없습니다.")
        return None
    
    # 가장 최신 파일 선택
    latest_debug = max(debug_files, key=lambda x: os.path.getmtime(x))
    print(f"📂 최신 디버그 파일: {latest_debug}")
    
    try:
        with open(latest_debug, 'r', encoding='utf-8') as f:
            debug_data = json.load(f)
        
        original_headers = debug_data.get('original_headers', {})
        curl_command = debug_data.get('curl_command', '')
        
        # URL 추출
        url = "https://studio.youtube.com/youtubei/v1/creator/list_creator_videos?alt=json"
        
        # 기본 POST 데이터 추출 (curl 명령어에서)
        if '--data-raw' in curl_command:
            data_start = curl_command.find("--data-raw '") + 12
            data_end = curl_command.find("'", data_start)
            
            if data_start > 11 and data_end > data_start:
                post_data = curl_command[data_start:data_end]
                
                try:
                    base_payload = json.loads(post_data)
                    print(f"✅ 기본 요청 페이로드 추출 완료")
                    return {
                        'url': url,
                        'headers': original_headers,
                        'base_payload': base_payload
                    }
                except json.JSONDecodeError:
                    print(f"❌ POST 데이터 JSON 파싱 실패")
                    return None
        
        print(f"❌ POST 데이터를 찾을 수 없습니다.")
        return None
        
    except Exception as e:
        print(f"❌ 디버그 파일 읽기 오류: {e}")
        return None

def collect_remaining_pages(next_token, request_info, existing_videos):
    """남은 모든 페이지 수집"""
    
    print(f"\n🚀 남은 페이지들 자동 수집 시작!")
    print(f"🎯 시작 토큰: {next_token[:50]}...")
    
    all_videos = existing_videos.copy()  # 기존 비디오들 복사
    page_count = 1  # 이미 첫 페이지는 수집됨
    current_token = next_token
    
    while current_token:
        page_count += 1
        print(f"\n📄 페이지 {page_count} 수집 중...")
        
        # 페이로드에 pageToken 추가
        payload = request_info['base_payload'].copy()
        payload['pageToken'] = current_token
        
        # 요청 전송
        session = requests.Session()
        headers = request_info['headers'].copy()
        
        # 쿠키 설정
        if 'Cookie' in headers:
            cookie_str = headers['Cookie']
            cookies = {}
            for item in cookie_str.split(';'):
                if '=' in item:
                    key, value = item.strip().split('=', 1)
                    cookies[key] = value
            session.cookies.update(cookies)
            print(f"   🍪 쿠키 설정: {len(cookies)}개")
        
        # Content-Length 제거
        headers.pop('Content-Length', None)
        
        try:
            print(f"   📡 API 요청 전송 중...")
            response = session.post(
                request_info['url'], 
                headers=headers, 
                json=payload, 
                timeout=30
            )
            
            print(f"   📨 응답 수신: {response.status_code}")
            
            if response.status_code == 200:
                api_response = response.json()
                
                # 이 페이지의 비디오들 추가
                page_videos = api_response.get('videos', [])
                print(f"   ✅ 페이지 {page_count}: {len(page_videos)}개 비디오 수집")
                
                # 공개 영상만 필터링
                public_videos = []
                for video in page_videos:
                    if video.get('privacy') == 'VIDEO_PRIVACY_PUBLIC':
                        public_videos.append(video)
                
                print(f"   📺 공개 영상: {len(public_videos)}개")
                all_videos.extend(public_videos)
                
                # 다음 페이지 토큰 확인
                current_token = api_response.get('nextPageToken')
                if current_token:
                    print(f"   🔄 다음 페이지 토큰: {current_token[:50]}...")
                else:
                    print(f"   🏁 마지막 페이지 도달!")
                    break
                    
            else:
                print(f"   ❌ 요청 실패: {response.status_code}")
                print(f"   응답: {response.text[:200]}...")
                break
                
        except Exception as e:
            print(f"   ❌ 요청 오류: {e}")
            break
        
        # API 제한 고려
        time.sleep(1)
    
    print(f"\n🎉 전체 수집 완료!")
    print(f"   📄 총 페이지: {page_count}개")
    print(f"   📹 총 공개 비디오: {len(all_videos)}개")
    
    return all_videos, page_count

def save_complete_data(all_videos, page_count):
    """완전한 데이터 저장"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON 저장
    json_filename = f"youtube_videos_COMPLETE_{timestamp}.json"
    complete_data = {
        'collection_method': 'manual_pagination',
        'total_pages_collected': page_count,
        'total_videos': len(all_videos),
        'collected_at': datetime.now().isoformat(),
        'videos': all_videos
    }
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 완전한 데이터 저장:")
    print(f"   📄 JSON: {json_filename}")
    
    return json_filename

def main():
    print("🎯 nextPageToken을 사용한 전체 비디오 수집")
    print("="*70)
    
    # 1단계: nextPageToken 추출
    next_token, existing_data = extract_next_page_token()
    
    if not next_token:
        print(f"❌ nextPageToken을 찾을 수 없어서 진행할 수 없습니다.")
        print(f"💡 브라우저에서 강력 새로고침 후 python once.py를 다시 실행해보세요.")
        return
    
    # 2단계: 캡처된 요청 정보 가져오기
    request_info = get_captured_request_info()
    
    if not request_info:
        print(f"❌ 캡처된 요청 정보를 찾을 수 없습니다.")
        return
    
    # 3단계: 기존 비디오들 가져오기
    existing_videos = existing_data.get('videos', [])
    print(f"📋 기존 수집된 공개 비디오: {len(existing_videos)}개")
    
    # 4단계: 남은 페이지들 수집
    complete_videos, total_pages = collect_remaining_pages(
        next_token, request_info, existing_videos
    )
    
    # 5단계: 완전한 데이터 저장
    if len(complete_videos) > len(existing_videos):
        saved_file = save_complete_data(complete_videos, total_pages)
        
        print(f"\n🎉 미션 완료!")
        print(f"   📈 기존: {len(existing_videos)}개 → 최종: {len(complete_videos)}개")
        print(f"   📂 완전한 파일: {saved_file}")
        print(f"\n💡 이제 이 데이터로 애널리틱스 수집을 시작할 수 있습니다!")
    else:
        print(f"⚠️ 추가로 수집된 비디오가 없습니다.")

if __name__ == "__main__":
    main() 