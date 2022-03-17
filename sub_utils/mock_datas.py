# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 15.03.2022
from datetime import datetime, timedelta
mock_campaign = {
    'name': "Mock data from API (Sezer)",
    'objective': 'REACH'
}
mock_ad_set = {
    'name': 'My first Adset Sezer(API)',
    'daily_budget': '2000',
    'campaign_id': '120330000104075109',
    'start_time': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    'end_time': (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S"),
    'bid_amount': '5',
    'billing_event': 'IMPRESSIONS',
    'optimization_goal': 'REACH',
    'targeting': {
        'geo_locations': {
            'countries': ['AE', 'SA', 'KW']
        },
        'age_min': '20',
        'age_max': '35'
    },
    'status': 'PAUSED',
}

mock_creative_campaign = {
    'creative_link_message': 'try it out',
    'creative_link': 'https://www.ounass.ae/designers/gucci',
    'page_id': '104413048775500',
    'creative_name': 'Gucci AdCreative for Link Ad.',
    'creative_image': 'https://ibb.co/pP9hNwV'
}
