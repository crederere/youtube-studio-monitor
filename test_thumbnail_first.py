#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from once import YouTubeStudioMonitor
from datetime import datetime
import time

def create_thumbnail_first_test_data():
    """썸네일 첫 번째 열 테스트 데이터"""
    
    # 기본 비디오 데이터
    basic_video_data = [
        {
            'videoId': 'RLe5T6Fn3YQ',
            'title': '썸네일 테스트 - 브이로그',
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
            'title': '썸네일 테스트 - 먹방',
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

def test_thumbnail_first():
    """썸네일 첫 번째 열 테스트"""
    
    print("🎯 썸네일 첫 번째 열 + 큰 행 높이 테스트")
    print("=" * 70)
    
    # 테스트 데이터 생성
    analytics_data = create_thumbnail_first_test_data()
    print(f"✅ {len(analytics_data)}개 썸네일 테스트 데이터 생성됨")
    
    # YouTubeStudioMonitor 인스턴스 생성
    monitor = YouTubeStudioMonitor()
    
    try:
        # 썸네일 첫 번째 열 엑셀 파일 생성
        excel_filename = "THUMBNAIL_FIRST_test.xlsx"
        print(f"\n📊 썸네일 첫 번째 열 엑셀 생성 중...")
        print(f"   파일명: {excel_filename}")
        
        monitor.save_simple_analytics_excel(analytics_data, excel_filename)
        
        print(f"\n🎉 썸네일 첫 번째 열 테스트 완료!")
        print(f"📂 생성된 파일: {excel_filename}")
        print(f"\n🔍 확인 사항:")
        print(f"   1. 썸네일이 첫 번째 열(A열)에 있는가?")
        print(f"   2. 썸네일 이미지가 잘리지 않고 완전히 보이는가?")
        print(f"   3. 행 높이가 썸네일에 맞게 더 커졌는가?")
        print(f"   4. 썸네일 컬럼 너비가 충분한가?")
        print(f"   5. 비디오 URL 하이퍼링크가 제대로 작동하는가?")
        print(f"   6. 다른 모든 데이터가 올바른 위치에 있는가?")
        
        print(f"\n📋 새로운 컬럼 순서:")
        print(f"   A: 썸네일 (크게)")
        print(f"   B: 비디오 ID")
        print(f"   C: 제목")
        print(f"   D: 공개상태")
        print(f"   E: 길이")
        print(f"   F: 생성일")
        print(f"   G: 게시일")
        print(f"   H-P: 조회수, 좋아요, 댓글, 노출수, 클릭률, 애널리틱스조회수, 시청시간, 평균시청시간, 평균조회율")
        print(f"   Q: 비디오 URL (하이퍼링크)")
        
    except Exception as e:
        print(f"❌ 썸네일 첫 번째 열 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_thumbnail_first() 