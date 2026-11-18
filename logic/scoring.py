def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def calculate_priority(impact, severity, confidence):
    priority = (
        impact * 0.45
        + severity * 0.35
        + confidence * 0.20
    )

    return round(priority, 1)


def calculate_campaign_scores(row):
    # 1. Severity
    cpl_increase = (
        row["current_cpl"] - row["baseline_cpl"]
    ) / row["baseline_cpl"]

    severity = clamp(
        (cpl_increase / 0.75) * 100
    )

    # 2. Impact
    expected_spend = (
        row["current_conversions"]
        * row["baseline_cpl"]
    )

    excess_spend = max(
        0,
        row["current_spend"] - expected_spend
    )

    impact = clamp(
        (
            excess_spend
            / (10 * row["target_cpl"])
        ) * 100
    )

    # 3. Confidence
    spend_score = clamp(
        (
            row["current_spend"]
            / (10 * row["target_cpl"])
        ) * 100
    )

    conversion_score = clamp(
        (row["current_conversions"] / 10) * 100
    )

    confidence = (
        spend_score * 0.5
        + conversion_score * 0.5
    )

    # 4. Priority
    priority = calculate_priority(
        impact,
        severity,
        confidence
    )

    return {
        "severity": round(severity, 1),
        "impact": round(impact, 1),
        "confidence": round(confidence, 1),
        "priority": priority,
        "excess_spend": round(excess_spend, 2),
    }
def calculate_creative_scores(row):
        ctr_decline = (
            row["baseline_ctr"] - row["current_ctr"]
        ) / row["baseline_ctr"]

        cpl_increase = (
            row["current_cpl"] - row["baseline_cpl"]
        ) / row["baseline_cpl"]

        ctr_score = clamp(
            (ctr_decline / 0.40) * 100
        )

        cpl_score = clamp(
            (cpl_increase / 0.50) * 100
        )

        frequency_score = clamp(
            ((row["frequency"] - 3) / 3) * 100
        )

        severity = (
            ctr_score * 0.40
            + cpl_score * 0.40
            + frequency_score * 0.20
        )

        expected_spend = (
            row["current_conversions"]
            * row["baseline_cpl"]
        )

        excess_spend = max(
            0,
            row["current_spend"] - expected_spend
        )

        impact = clamp(
            (
                excess_spend
                / (10 * row["target_cpl"])
            ) * 100
        )

        impression_score = clamp(
            (row["impressions"] / 15000) * 100
        )

        frequency_confidence = clamp(
            (row["frequency"] / 4) * 100
        )

        confidence = (
            impression_score * 0.5
            + frequency_confidence * 0.5
        )

        priority = calculate_priority(
            impact,
            severity,
            confidence
        )

        return {
            "severity": round(severity, 1),
            "impact": round(impact, 1),
            "confidence": round(confidence, 1),
            "priority": priority,
            "excess_spend": round(excess_spend, 2),
        }