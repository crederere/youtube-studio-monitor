#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from once import YouTubeStudioMonitor
from datetime import datetime
import time

def create_complete_test_data():
    """완전한 테스트 데이터 (기본 정보 + 애널리틱스)"""
    
    # 기본 비디오 데이터
    basic_video_data = [
        {
            'videoId': 'RLe5T6Fn3YQ',
            'title': '2021년 9월 18일 여행 브이로그',
            'privacy': 'VIDEO_PRIVACY_PUBLIC',
            'status': 'VIDEO_STATUS_PROCESSED',
            'lengthSeconds': '720',
            'timeCreatedSeconds': str(int(time.time() - 86400 * 30)),
            'timePublishedSeconds': str(int(time.time() - 86400 * 25)),
            'public_viewCount': '1500',
            'public_likeCount': '89',
            'public_commentCount': '23',
            'thumbnailDetails': {
                'thumbnails': [
                    {'url': 'https://img.youtube.com/vi/RLe5T6Fn3YQ/maxresdefault.jpg', 'width': 1920, 'height': 1080}
                ]
            }
        },
        {
            'videoId': 'oRWchhS6OqM',
            'title': '한강에서 치킨 먹방',
            'privacy': 'VIDEO_PRIVACY_PUBLIC',
            'status': 'VIDEO_STATUS_PROCESSED',
            'lengthSeconds': '900',
            'timeCreatedSeconds': str(int(time.time() - 86400 * 7)),
            'timePublishedSeconds': str(int(time.time() - 86400 * 5)),
            'public_viewCount': '2300',
            'public_likeCount': '156',
            'public_commentCount': '45',
            'thumbnailDetails': {
                'thumbnails': [
                    {'url': 'https://img.youtube.com/vi/oRWchhS6OqM/maxresdefault.jpg', 'width': 1920, 'height': 1080}
                ]
            }
        }
    ]
    
    # 애널리틱스 데이터
    analytics_data = []
    for video in basic_video_data:
        video_analytics = {
            'video_id': video['videoId'],
            'video_title': video['title'],
            'collected_at': datetime.now().isoformat(),
            'basic_video_info': video,
            'analytics_data': {
                'reach_viewers': {
                    'api_type': 'get_screen',
                    'response_data': {
                        'cards': [
                            {
                                'keyMetricCardData': {
                                    'keyMetricTabs': [
                                        {
                                            'primaryContent': {
                                                'metric': 'VIDEO_THUMBNAIL_IMPRESSIONS',
                                                'total': 1500 if video['videoId'] == 'RLe5T6Fn3YQ' else 2800
                                            }
                                        },
                                        {
                                            'primaryContent': {
                                                'metric': 'VIDEO_THUMBNAIL_IMPRESSIONS_VTR',
                                                'total': 8.5 if video['videoId'] == 'RLe5T6Fn3YQ' else 12.3
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                'interest_viewers': {
                    'api_type': 'get_cards',
                    'response_data': {
                        'cards': [
                            {
                                'keyMetricCardData': {
                                    'keyMetricTabs': [
                                        {
                                            'primaryContent': {
                                                'metric': 'EXTERNAL_VIEWS',
                                                'total': int(video['public_viewCount'])
                                            }
                                        },
                                        {
                                            'primaryContent': {
                                                'metric': 'EXTERNAL_WATCH_TIME',
                                                'total': 450000 if video['videoId'] == 'RLe5T6Fn3YQ' else 780000
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                'audienceRetentionHighlightsCardData': {
                                    'videosData': [
                                        {
                                            'videoId': video['videoId'],
                                            'metricTotals': {
                                                'avgViewDurationMillis': 45000 if video['videoId'] == 'RLe5T6Fn3YQ' else 67000,
                                                'avgPercentageWatched': 0.65 if video['videoId'] == 'RLe5T6Fn3YQ' else 0.78,
                                                'views': int(video['public_viewCount'])
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
        analytics_data.append(video_analytics)
    
    return analytics_data

def test_final_version():
    """최종 버전 테스트"""
    
    print("🎯 최종 수정 버전 테스트 시작")
    print("=" * 70)
    
    # 테스트 데이터 생성
    analytics_data = create_complete_test_data()
    print(f"✅ {len(analytics_data)}개 완전한 테스트 데이터 생성됨")
    
    # YouTubeStudioMonitor 인스턴스 생성
    monitor = YouTubeStudioMonitor()
    
    try:
        # 통합 애널리틱스 엑셀 파일 생성
        excel_filename = "FINAL_youtube_analytics_test.xlsx"
        print(f"\n📊 통합 애널리틱스 엑셀 생성 중...")
        print(f"   파일명: {excel_filename}")
        
        monitor.save_simple_analytics_excel(analytics_data, excel_filename)
        
        print(f"\n🎉 최종 테스트 완료!")
        print(f"📂 생성된 파일: {excel_filename}")
        print(f"\n🔍 확인 사항:")
        print(f"   1. 썸네일 이미지가 실제로 엑셀에 들어갔는가?")
        print(f"   2. 비디오 URL이 클릭 가능한 하이퍼링크인가?") 
        print(f"   3. 공개 상태가 한글로 표시되는가?")
        print(f"   4. 날짜가 한국어 형식인가?")
        print(f"   5. 단일 시트만 존재하는가?")
        print(f"   6. 기본 정보 + 애널리틱스가 모두 포함되어 있는가?")
        
    except Exception as e:
        print(f"❌ 최종 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_final_version() 