def detect_campaign_anomaly(row):
    cpl_change = (
        row["current_cpl"] - row["baseline_cpl"]
    ) / row["baseline_cpl"]

    enough_spend = (
        row["current_spend"] >= 1.5 * row["target_cpl"]
    )

    enough_conversions = row["current_conversions"] >= 3

    return (
        cpl_change >= 0.25
        and enough_spend
        and enough_conversions
    )


def detect_creative_fatigue(row):
    if row["impressions"] < 5000:
        return False

    if row["frequency"] < 3:
        return False

    ctr_decline = (
        row["baseline_ctr"] - row["current_ctr"]
    ) / row["baseline_ctr"]

    cpl_increase = (
        row["current_cpl"] - row["baseline_cpl"]
    ) / row["baseline_cpl"]

    return ctr_decline >= 0.20 or cpl_increase >= 0.20