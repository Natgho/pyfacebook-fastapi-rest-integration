# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 15.03.2022
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.exceptions import FacebookError
from fastapi.logger import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FacebookApi(metaclass=Singleton):
    def __init__(self, my_app_id,
                 my_app_secret,
                 my_access_token,
                 ad_account_id):
        FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
        self.my_account: AdAccount = AdAccount(ad_account_id)

    def get_campaigns(self):
        try:
            campaigns = self.my_account.get_campaigns(fields=[Campaign.Field.name, Campaign.Field.objective])
        except FacebookError as e:
            logger.error(e)
            return e
        return {
            row['id']: {"id": row['id'],
                        "name": row['name'],
                        "objective": row['objective']} for row in campaigns
        }

    def create_campaign(self, name='Conversions Campaign Sezer(API)', objective='REACH'):
        fields = [
        ]
        params = {
            Campaign.Field.name: name,
            Campaign.Field.special_ad_categories: [],
            Campaign.Field.objective: objective
        }
        try:
            campaign = self.my_account.create_campaign(fields=fields, params=params)
        except FacebookError as e:
            logger.error(e)
            return e
        return campaign

    def get_add_sets(self):
        fields = [
            AdSet.Field.id,
            AdSet.Field.name,
            AdSet.Field.daily_budget,
            AdSet.Field.campaign,
            AdSet.Field.bid_amount,
            AdSet.Field.billing_event,
            AdSet.Field.optimization_goal,
            AdSet.Field.targeting
        ]
        try:
            add_sets = self.my_account.get_ad_sets(fields=fields)
        except FacebookError as e:
            logger.error(e)
            return e
        return {
            row['id']: {
                'id': row['id'],
                'name': row['name'],
                'bid_amount': row['bid_amount'],
                'billing_event': row['billing_event'],
                'campaign': {
                    'id': row['id']
                },
                'daily_budget': row['daily_budget'],
                'optimization_goal': row['optimization_goal'],
                'targeting': {
                    'age_max': row['targeting']['age_max'],
                    'age_min': row['targeting']['age_min'],
                    "geo_locations": {
                        "countries": [country for country in
                                      row['targeting']['geo_locations']['countries']] if 'countries' in dict(
                            row['targeting']['geo_locations']).keys() else None
                    }
                }
            } for row in add_sets
        }

    def create_add_set(self, name,
                       daily_budget,
                       start_time,
                       end_time,
                       campaign_id,
                       bid_amount,
                       billing_event,
                       optimization_goal,
                       targeting,
                       status
                       ):
        fields = [
        ]
        params = {
            'name': name,
            'start_time': start_time,
            'end_time': end_time,
            'daily_budget': daily_budget,
            'campaign_id': campaign_id,
            'bid_amount': bid_amount,
            'billing_event': billing_event,
            'optimization_goal': optimization_goal,
            'targeting': targeting,
            'status': status
        }

        try:
            tmp_ad_set = self.my_account.create_ad_set(fields=fields, params=params)
        except FacebookError as e:
            logger.error(e)
            tmp_ad_set = None
        return tmp_ad_set

    def get_creative_ads(self):
        fields = [
            AdCreative.Field.id,
            AdCreative.Field.name,  # Gucci AdCreative for Link Ad.
            AdCreative.Field.title,  # Shop Luxury Gucci Collection for Women Online | Ounass UAE
            AdCreative.Field.body,  # https://www.ounass.ae/designers/gucci
            AdCreative.Field.image_url,  # https://ibb.co/pP9hNwV
        ]
        params = {
        }
        try:
            creative_ads = self.my_account.get_ad_creatives(fields, params)
        except FacebookError as e:
            logger.error(e)
            return e
        return {
            row['id']: {
                'id': row.get('id'),
                'name': row.get('name'),
                'title': row.get('title'),
                'body': row.get('body'),
                'image_url': row.get('image_url'),
            } for row in creative_ads
        }

    def create_creative_ad(self, creative_link_message, creative_link, page_id, creative_name, creative_image):
        fields = [
            AdCreative.Field.name,
            AdCreative.Field.title,
            AdCreative.Field.body,
            AdCreative.Field.image_url,
            AdCreative.Field.place_page_set_id
        ]
        params = {
            'name': creative_name,
            'object_story_spec': {
                'page_id': page_id,
                'picture': creative_image,
                'link_data': {
                    'message': creative_link_message,
                    'link': creative_link
                }
            }

        }
        try:
            tmp_creative_ad = self.my_account.create_ad_creative(fields, params)
        except FacebookError as e:
            logger.error(e)
            return e
        return tmp_creative_ad

    def get_adset_insight(self, ad_set_id):
        fields = [
            'impressions',
        ]
        params = {
            'breakdown': 'publisher_platform',
        }
        try:
            insights = AdSet(ad_set_id).get_insights(fields=fields, params=params)
        except FacebookError as e:
            logger.error(e)
            return e
        return insights

    def get_creative_ads_insight(self, creative_ad_id):
        fields = [
        ]
        params = {
            'ad_format': 'MOBILE_BANNER'
        }
        try:
            insight = AdCreative(creative_ad_id).get_previews(fields, params)
        except FacebookError as e:
            logger.error(e)
            return e
        return {creative_ad_id: insight[0]['body']}
