from fastapi import FastAPI, Body
from starlette.responses import RedirectResponse

from sub_utils.facebook_utils import FacebookApi
from sub_utils.facebook_data_schemas import CampaignItem, AdsetItem, CreativeAdItem
from sub_utils.mock_datas import mock_campaign, mock_ad_set, mock_creative_campaign
from config import settings
import logging

logging.basicConfig(level=logging.WARN)
app = FastAPI(title='Use-Case Facebook Integration',
              description='This integration purpose is just use-case sample.',
              version='0.1',
              contact={
                  "name": "Sezer Bozkir",
                  "url": "https://sezerbozkir.com/",
                  "email": "admin@sezerbozkir.com",
              })


@app.get("/", include_in_schema=False)
async def root():
    response = RedirectResponse(url="/docs")
    return response


api = FacebookApi(my_app_id=settings.my_app_id,
                  my_app_secret=settings.my_app_secret,
                  my_access_token=settings.my_access_token,
                  ad_account_id=settings.ad_account_id)


@app.get("/campaign", tags=["Campaign"])
async def get_campaigns():
    return api.get_campaigns()


@app.post("/campaign", tags=["Campaign"])
async def add_campaign(campaign_details: CampaignItem = Body(mock_campaign)):
    resp = api.create_campaign(**campaign_details.dict())
    return resp


@app.get("/addset", tags=["Adset"])
async def get_adsets():
    return api.get_add_sets()


@app.post("/addset", tags=["Adset"])
async def add_adsets(ad_set_details: AdsetItem = Body(mock_ad_set)):
    return api.create_add_set(**ad_set_details.dict())


@app.get("/creative_ads", tags=["AdCreative"])
async def get_creative_ads():
    return api.get_creative_ads()


@app.post("/creative_ads", tags=["AdCreative"])
async def create_creative_ads(creative_ad_details: CreativeAdItem = Body(mock_creative_campaign)):
    return api.create_creative_ad(**creative_ad_details.dict())


@app.get("/insight/adset/{ad_set_id}", tags=["Insight API"])
async def get_ad_set_insights(ad_set_id: int):
    """
    Sample Adset for testing: 120330000104414509
    """
    insights = api.get_adset_insight(str(ad_set_id))
    # https://developers.facebook.com/docs/graph-api/reference/ad-campaign/insights/#example
    mock_response = {
        "data": [],
        "paging": {},
        "summary": {}
    }
    # if data response is empty, it will be mocked. 120330000104414509
    return insights if insights else mock_response


@app.get("/insight/creative_ad/{creative_ad_id}", tags=["Insight API"])
async def get_creative_add_insights(creative_ad_id: int):
    """
    Sample CreativeAdd ID for testing: 120330000104440509
    """
    insight = api.get_creative_ads_insight(str(creative_ad_id))
    # https://developers.facebook.com/docs/graph-api/reference/ad-campaign/insights/#example
    # if data response is empty, it will be mocked. 120330000104440509
    return insight
