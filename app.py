import streamlit as st
import pandas as pd

from logic.detection import (
    detect_campaign_anomaly,
    detect_creative_fatigue,
)

from logic.scoring import (
    calculate_campaign_scores,
    calculate_creative_scores,
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Performance Campaign Copilot",
    page_icon="◉",
    layout="wide",
)


# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.html("""
<style>

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(74, 108, 247, 0.07),
                transparent 30%
            ),
            #0b0f14;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Header */

    .product-eyebrow {
        color: #7f8a99;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .product-title {
        color: #f5f7fa;
        font-size: 36px;
        line-height: 1.1;
        font-weight: 750;
        letter-spacing: -0.03em;
        margin-bottom: 7px;
    }

    .product-subtitle {
        color: #8c96a5;
        font-size: 15px;
        margin-bottom: 24px;
    }

    /* Overview */

    .overview-card {
        background: #11171f;
        border: 1px solid #202a36;
        border-radius: 13px;
        padding: 16px 18px;
        min-height: 90px;
    }

    .overview-label {
        color: #7f8a99;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .06em;
    }

    .overview-value {
        color: #f5f7fa;
        font-size: 25px;
        font-weight: 750;
        margin-top: 4px;
    }

    .overview-note {
        color: #66717f;
        font-size: 11px;
        margin-top: 1px;
    }

    /* Recommendation container */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #10161d;
        border: 1px solid #202a36 !important;
        border-radius: 15px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]
    > div {
        padding-top: 5px;
        padding-bottom: 5px;
    }

    .rec-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 18px;
    }

    .rec-badges {
        display: flex;
        gap: 7px;
        margin-bottom: 9px;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: .04em;
    }

    .platform-badge {
        background: #19212b;
        border: 1px solid #273342;
        color: #aab4c0;
    }

    .urgent {
        background: rgba(248, 81, 73, .12);
        border: 1px solid rgba(248, 81, 73, .28);
        color: #ff7b72;
    }

    .high {
        background: rgba(210, 153, 34, .12);
        border: 1px solid rgba(210, 153, 34, .25);
        color: #e3b341;
    }

    .medium {
        background: rgba(88, 166, 255, .12);
        border: 1px solid rgba(88, 166, 255, .25);
        color: #79c0ff;
    }

    .watch {
        background: rgba(139, 148, 158, .12);
        border: 1px solid rgba(139, 148, 158, .25);
        color: #a5acb5;
    }

    .rec-title {
        color: #f4f7fa;
        font-size: 22px;
        font-weight: 750;
        letter-spacing: -.015em;
        margin-bottom: 2px;
    }

    .rec-type {
        color: #7f8a99;
        font-size: 12px;
    }

    .priority-score {
        color: #f5f7fa;
        font-size: 27px;
        font-weight: 750;
        text-align: right;
    }

    .priority-caption {
        color: #66717f;
        font-size: 9px;
        text-align: right;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .impact-pill {
        display: inline-block;
        margin-top: 8px;
        color: #c2cad4;
        background: #151d26;
        border: 1px solid #263240;
        padding: 5px 9px;
        border-radius: 8px;
        font-size: 11px;
    }

    /* Compact metrics */

    .metric-row {
        display: flex;
        gap: 8px;
        margin: 14px 0 14px 0;
    }

    .mini-metric {
        background: #0d131a;
        border: 1px solid #1c2631;
        border-radius: 8px;
        padding: 7px 10px;
        min-width: 115px;
    }

    .mini-label {
        color: #66717f;
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: .07em;
    }

    .mini-value {
        color: #dce3eb;
        font-size: 14px;
        font-weight: 700;
        margin-top: 1px;
    }

    /* Recommendation text */

    .section-label {
        color: #7f8a99;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: .07em;
        text-transform: uppercase;
        margin-top: 11px;
        margin-bottom: 2px;
    }

    .section-text {
        color: #d6dde5;
        font-size: 13px;
        line-height: 1.45;
    }

    .action-box {
        background: rgba(74, 108, 247, .07);
        border: 1px solid rgba(74, 108, 247, .22);
        border-radius: 9px;
        padding: 10px 12px;
        margin-top: 13px;
        margin-bottom: 7px;
    }

    .action-title {
        color: #8ea5ff;
        font-size: 10px;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-bottom: 3px;
    }

    .action-text {
        color: #e4e9ef;
        font-size: 13px;
        line-height: 1.45;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 8px;
        font-weight: 700;
        min-height: 36px;
        font-size: 13px;
    }

    /* Filters */

    div[role="radiogroup"] {
        gap: 6px;
    }

    div[role="radiogroup"] label {
        background: #11171f;
        border: 1px solid #202a36;
        padding: 5px 11px;
        border-radius: 999px;
    }

</style>
""")


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def get_priority_label(score):
    if score >= 80:
        return "Urgent"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Watch"


def get_priority_class(score):
    if score >= 80:
        return "urgent"
    elif score >= 60:
        return "high"
    elif score >= 40:
        return "medium"
    else:
        return "watch"


def get_explanation(recommendation):

    if recommendation["type"] == "Campaign Performance Anomaly":

        cpl_change = (
            (
                recommendation["current_cpl"]
                - recommendation["baseline_cpl"]
            )
            / recommendation["baseline_cpl"]
        ) * 100

        what_happened = (
            f'CPL increased by {cpl_change:.1f}% '
            f'from ${recommendation["baseline_cpl"]:.0f} '
            f'to ${recommendation["current_cpl"]:.0f}.'
        )

        why_it_matters = (
            f'At the current performance level, this campaign has '
            f'approximately ${recommendation["excess_spend"]:,.0f} '
            f'in estimated excess spend compared with its baseline.'
        )

        recommended_action = (
            "Review the campaign before scaling further and identify "
            "which part of the funnel is driving the CPL increase."
        )

    else:

        ctr_decline = (
            (
                recommendation["baseline_ctr"]
                - recommendation["current_ctr"]
            )
            / recommendation["baseline_ctr"]
        ) * 100

        cpl_change = (
            (
                recommendation["current_cpl"]
                - recommendation["baseline_cpl"]
            )
            / recommendation["baseline_cpl"]
        ) * 100

        what_happened = (
            f'CTR declined by {ctr_decline:.1f}% while CPL '
            f'increased by {cpl_change:.1f}%. '
            f'Frequency has reached {recommendation["frequency"]:.1f}.'
        )

        why_it_matters = (
            f'The combination of declining engagement and rising cost '
            f'indicates creative fatigue. Estimated excess spend is '
            f'${recommendation["excess_spend"]:,.0f}.'
        )

        recommended_action = (
            "Review this creative for replacement or refresh and compare "
            "delivery with the strongest active creative."
        )

    return (
        what_happened,
        why_it_matters,
        recommended_action,
    )


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "tasks" not in st.session_state:
    st.session_state.tasks = []


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

campaigns = pd.read_csv("data/campaigns.csv")
creatives = pd.read_csv("data/creatives.csv")

recommendations = []


# --------------------------------------------------
# CAMPAIGN RECOMMENDATIONS
# --------------------------------------------------

for _, row in campaigns.iterrows():

    if detect_campaign_anomaly(row):

        scores = calculate_campaign_scores(row)

        recommendations.append({
            "platform": row["platform"],
            "name": row["campaign_name"],
            "type": "Campaign Performance Anomaly",
            "priority": scores["priority"],
            "severity": scores["severity"],
            "impact": scores["impact"],
            "confidence": scores["confidence"],
            "excess_spend": scores["excess_spend"],
            "current_cpl": row["current_cpl"],
            "baseline_cpl": row["baseline_cpl"],
        })


# --------------------------------------------------
# CREATIVE RECOMMENDATIONS
# --------------------------------------------------

for _, row in creatives.iterrows():

    if detect_creative_fatigue(row):

        scores = calculate_creative_scores(row)

        recommendations.append({
            "platform": row["platform"],
            "name": row["creative_name"],
            "type": "Creative Fatigue",
            "priority": scores["priority"],
            "severity": scores["severity"],
            "impact": scores["impact"],
            "confidence": scores["confidence"],
            "excess_spend": scores["excess_spend"],
            "current_ctr": row["current_ctr"],
            "baseline_ctr": row["baseline_ctr"],
            "current_cpl": row["current_cpl"],
            "baseline_cpl": row["baseline_cpl"],
            "frequency": row["frequency"],
        })


recommendations.sort(
    key=lambda item: item["priority"],
    reverse=True,
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.html("""
<div class="product-eyebrow">Morning performance scan</div>

<div class="product-title">
    Performance Copilot
</div>

<div class="product-subtitle">
    Know what needs your attention before opening Google Ads or Meta.
</div>
""")


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

urgent_count = sum(
    1 for rec in recommendations
    if rec["priority"] >= 80
)

total_excess_spend = sum(
    rec["excess_spend"]
    for rec in recommendations
)

approved_count = len(
    st.session_state.tasks
)


overview1, overview2, overview3, overview4 = st.columns(4)

with overview1:
    st.html(f"""
    <div class="overview-card">
        <div class="overview-label">
            Needs attention
        </div>

        <div class="overview-value">
            {len(recommendations)}
        </div>

        <div class="overview-note">
            Recommendations found
        </div>
    </div>
    """)

with overview2:
    st.html(f"""
    <div class="overview-card">
        <div class="overview-label">
            Urgent
        </div>

        <div class="overview-value">
            {urgent_count}
        </div>

        <div class="overview-note">
            Review first
        </div>
    </div>
    """)

with overview3:
    st.html(f"""
    <div class="overview-card">
        <div class="overview-label">
            Est. excess spend
        </div>

        <div class="overview-value">
            ${total_excess_spend:,.0f}
        </div>

        <div class="overview-note">
            Across detected issues
        </div>
    </div>
    """)

with overview4:
    st.html(f"""
    <div class="overview-card">
        <div class="overview-label">
            Approved
        </div>

        <div class="overview-value">
            {approved_count}
        </div>

        <div class="overview-note">
            Added to task list
        </div>
    </div>
    """)


st.write("")
st.write("")


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

filter_choice = st.radio(
    "Filter recommendations",
    [
        "All",
        "Google",
        "Meta",
        "Urgent",
    ],
    horizontal=True,
    label_visibility="collapsed",
)


if filter_choice == "Google":

    filtered_recommendations = [
        rec for rec in recommendations
        if rec["platform"] == "Google"
    ]

elif filter_choice == "Meta":

    filtered_recommendations = [
        rec for rec in recommendations
        if rec["platform"] == "Meta"
    ]

elif filter_choice == "Urgent":

    filtered_recommendations = [
        rec for rec in recommendations
        if rec["priority"] >= 80
    ]

else:

    filtered_recommendations = recommendations


st.write("")


# --------------------------------------------------
# RECOMMENDATION CARDS
# --------------------------------------------------

for recommendation in filtered_recommendations:

    priority_label = get_priority_label(
        recommendation["priority"]
    )

    priority_class = get_priority_class(
        recommendation["priority"]
    )

    (
        what_happened,
        why_it_matters,
        recommended_action,
    ) = get_explanation(recommendation)

    task_id = (
        f'{recommendation["platform"]}-'
        f'{recommendation["type"]}-'
        f'{recommendation["name"]}'
    )

    already_approved = any(
        task["id"] == task_id
        for task in st.session_state.tasks
    )

    with st.container(border=True):

        st.html(f"""
        <div class="rec-header">

            <div>

                <div class="rec-badges">

                    <span class="badge {priority_class}">
                        {priority_label.upper()}
                    </span>

                    <span class="badge platform-badge">
                        {recommendation["platform"]}
                    </span>

                </div>

                <div class="rec-title">
                    {recommendation["name"]}
                </div>

                <div class="rec-type">
                    {recommendation["type"]}
                </div>

                <div class="impact-pill">
                    ${recommendation["excess_spend"]:,.0f}
                    estimated excess spend
                </div>

            </div>

            <div>

                <div class="priority-score">
                    {recommendation["priority"]}
                </div>

                <div class="priority-caption">
                    Priority score
                </div>

            </div>

        </div>

        <div class="metric-row">

            <div class="mini-metric">
                <div class="mini-label">
                    Severity
                </div>
                <div class="mini-value">
                    {recommendation["severity"]}
                </div>
            </div>

            <div class="mini-metric">
                <div class="mini-label">
                    Impact
                </div>
                <div class="mini-value">
                    {recommendation["impact"]}
                </div>
            </div>

            <div class="mini-metric">
                <div class="mini-label">
                    Confidence
                </div>
                <div class="mini-value">
                    {recommendation["confidence"]}%
                </div>
            </div>

        </div>

        <div class="section-label">
            What happened
        </div>

        <div class="section-text">
            {what_happened}
        </div>

        <div class="section-label">
            Why it matters
        </div>

        <div class="section-text">
            {why_it_matters}
        </div>

        <div class="action-box">

            <div class="action-title">
                Recommended action
            </div>

            <div class="action-text">
                {recommended_action}
            </div>

        </div>
        """)

        button_space, button_col = st.columns(
            [4.6, 1.4],
            vertical_alignment="center",
        )

        with button_col:

            if already_approved:

                st.button(
                    "✓ Added to tasks",
                    key=f"approved-{task_id}",
                    disabled=True,
                    use_container_width=True,
                )

            else:

                if st.button(
                    "Approve & add to tasks",
                    key=f"approve-{task_id}",
                    type="primary",
                    use_container_width=True,
                ):

                    st.session_state.tasks.append({
                        "id": task_id,
                        "name": recommendation["name"],
                        "platform": recommendation["platform"],
                        "type": recommendation["type"],
                        "priority": recommendation["priority"],
                        "status": "To Do",
                    })

                    st.rerun()

    st.write("")


if not filtered_recommendations:

    st.info(
        "No recommendations match this filter."
    )