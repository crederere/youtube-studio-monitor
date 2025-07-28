#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import requests
import time
from datetime import datetime

def check_existing_data_for_pagination():
    """기존 수집된 데이터에서 nextPageToken 확인"""
    
    print("🔍 기존 데이터에서 nextPageToken 확인 중...")
    
    # 최신 JSON 파일들 찾기
    json_files = []
    for file in os.listdir('.'):
        if file.startswith('youtube_videos_list_') and file.endswith('.json'):
            json_files.append(file)
    
    if not json_files:
        print("❌ 비디오 목록 JSON 파일을 찾을 수 없습니다.")
        return None, None
    
    # 가장 최신 파일 선택
    latest_file = max(json_files, key=lambda x: os.path.getmtime(x))
    print(f"📂 최신 파일: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # original_response_keys 확인
        original_keys = data.get('original_response_keys', [])
        print(f"📋 원본 응답 키들: {original_keys}")
        
        # 첫 번째 비디오 확인
        videos = data.get('videos', [])
        total_videos = data.get('total_videos', len(videos))
        
        print(f"📊 현재 상태:")
        print(f"   • 수집된 비디오: {len(videos)}개")
        print(f"   • 총 비디오: {total_videos}개")
        
        if len(videos) > 0:
            first_video = videos[0]
            last_video = videos[-1]
            
            print(f"📹 첫 번째 비디오: {first_video.get('title', 'N/A')[:40]}...")
            print(f"📹 마지막 비디오: {last_video.get('title', 'N/A')[:40]}...")
        
        # 페이지네이션 추정
        if len(videos) % 25 == 0 or len(videos) % 30 == 0:
            print(f"⚠️ 페이지 크기가 정확히 {len(videos)}개 → 더 많은 비디오가 있을 가능성 높음!")
            return True, latest_file
        elif len(videos) < 50:
            print(f"✅ 아마도 모든 비디오가 수집된 것 같습니다.")
            return False, latest_file
        else:
            print(f"🤔 애매한 상황입니다. 확인이 필요할 수 있습니다.")
            return None, latest_file
            
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        return None, None

def check_debug_files_for_next_token():
    """디버그 파일에서 nextPageToken 확인"""
    
    print("\n🔍 디버그 파일에서 nextPageToken 확인 중...")
    
    # 최신 디버그 요청 파일들 찾기
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
        
        # curl 명령어에서 POST 데이터 확인
        curl_command = debug_data.get('curl_command', '')
        
        if '--data-raw' in curl_command:
            # POST 데이터 추출
            data_start = curl_command.find("--data-raw '") + 12
            data_end = curl_command.find("'", data_start)
            
            if data_start > 11 and data_end > data_start:
                post_data = curl_command[data_start:data_end]
                
                try:
                    payload = json.loads(post_data)
                    page_token = payload.get('pageToken')
                    
                    if page_token:
                        print(f"✅ 페이지 토큰 발견: {page_token[:50]}...")
                        print(f"🎯 이는 첫 번째 페이지가 아닌 요청임을 의미합니다!")
                        return page_token
                    else:
                        print(f"ℹ️ 페이지 토큰 없음 → 첫 번째 페이지 요청")
                        return None
                        
                except json.JSONDecodeError:
                    print(f"❌ POST 데이터 JSON 파싱 실패")
                    return None
        else:
            print(f"❌ POST 데이터를 찾을 수 없습니다.")
            return None
            
    except Exception as e:
        print(f"❌ 디버그 파일 읽기 오류: {e}")
        return None

def suggest_next_steps():
    """다음 단계 제안"""
    
    print(f"\n" + "="*80)
    print(f"🎯 전체 비디오 수집을 위한 다음 단계")
    print(f"="*80)
    
    print(f"\n📋 **방법 1: 브라우저에서 새로고침**")
    print(f"   1. 🌐 현재 열린 Chrome의 YouTube Studio로 이동")
    print(f"   2. 📺 '콘텐츠' 페이지에서 **Ctrl+F5** (강력 새로고침)")
    print(f"   3. 🔄 페이지가 완전히 다시 로드되면 python once.py 재실행")
    print(f"   4. ✅ 이번에는 모든 페이지가 자동으로 수집될 것입니다!")
    
    print(f"\n📋 **방법 2: 수동으로 추가 페이지 수집**")
    print(f"   1. 🌐 YouTube Studio 콘텐츠 페이지에서 스크롤 다운")
    print(f"   2. ⬇️ 새로운 비디오들이 로드될 때까지 계속 스크롤")
    print(f"   3. 🔄 새 API 요청이 발생하면 python once.py가 자동 감지")
    print(f"   4. ✅ 새로 로드된 비디오들도 자동으로 수집됨")
    
    print(f"\n⚡ **추천 방법: 강력 새로고침**")
    print(f"   지금 바로 Chrome에서:")
    print(f"   1. YouTube Studio 콘텐츠 페이지 이동")
    print(f"   2. **Ctrl+Shift+R** 또는 **Ctrl+F5** 눌러서 강력 새로고침")
    print(f"   3. python once.py 다시 실행")
    
    print(f"\n💡 **왜 이런 일이 생겼나요?**")
    print(f"   • 브라우저 캐시로 인해 이미 로드된 데이터는 새 API 요청을 하지 않음")
    print(f"   • 강력 새로고침하면 캐시 무시하고 모든 데이터를 다시 요청")
    print(f"   • 개선된 코드는 이제 모든 페이지를 자동으로 순차 수집")

def main():
    print("📊 페이지네이션 상태 확인")
    print("="*60)
    
    # 기존 데이터 확인
    has_more, latest_file = check_existing_data_for_pagination()
    
    # 디버그 파일 확인
    next_token = check_debug_files_for_next_token()
    
    # 결론 및 제안
    if has_more or next_token:
        print(f"\n🎯 **결론: 더 많은 비디오가 있을 가능성이 높습니다!**")
        suggest_next_steps()
    elif has_more is False:
        print(f"\n✅ **결론: 아마도 모든 비디오가 수집된 것 같습니다.**")
        print(f"하지만 확실하지 않다면 강력 새로고침을 한 번 시도해보세요.")
    else:
        print(f"\n🤔 **결론: 불확실합니다.**")
        suggest_next_steps()

if __name__ == "__main__":
    main() 