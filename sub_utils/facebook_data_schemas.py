# Created by Sezer BOZKIR<admin@sezerbozkir.com> at 15.03.2022
from pydantic import BaseModel


class CampaignItem(BaseModel):
    name: str
    objective: str


class AdsetItem(BaseModel):
    name: str
    start_time: str
    end_time: str
    daily_budget: str
    campaign_id: str
    bid_amount: str
    billing_event: str
    optimization_goal: str
    targeting: dict
    status: str


class CreativeAdItem(BaseModel):
    creative_link_message: str
    creative_link: str
    page_id: str
    creative_name: str
    creative_image: str

