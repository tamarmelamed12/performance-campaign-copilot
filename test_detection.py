import pandas as pd

from logic.detection import (
    detect_campaign_anomaly,
    detect_creative_fatigue,
)
from logic.scoring import (
    calculate_campaign_scores,
    calculate_creative_scores,
)
campaigns = pd.read_csv("data/campaigns.csv")
creatives = pd.read_csv("data/creatives.csv")

print("CAMPAIGNS")

for _, row in campaigns.iterrows():
    result = detect_campaign_anomaly(row)
    print(row["campaign_name"], result)
    
    if result:
        scores = calculate_campaign_scores(row)
        print(scores)
    

print("\nCREATIVES")

for _, row in creatives.iterrows():
    result = detect_creative_fatigue(row)
    print(row["creative_name"], result)
    if result:
        scores = calculate_creative_scores(row)
        print(scores)