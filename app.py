import streamlit as st
import pandas as pd
from openai import OpenAI

from logic.detection import (
    detect_campaign_anomaly,
    detect_creative_fatigue,
)

from logic.scoring import (
    calculate_campaign_scores,
    calculate_creative_scores,
)


# -----------------------------
# Priority label
# -----------------------------

def get_priority_label(score):
    if score >= 80:
        return "Urgent"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Watch"


# -----------------------------
# Recommendation explanation
# -----------------------------

def get_explanation(recommendation):

    # Campaign anomaly
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
            f'Estimated excess spend is '
            f'${recommendation["excess_spend"]:,.0f}.'
        )

        recommended_action = (
            "Review the campaign and investigate what is driving "
            "the increase in CPL before increasing spend."
        )

    # Creative fatigue
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
            f'Frequency is {recommendation["frequency"]:.1f}.'
        )

        why_it_matters = (
            f'The creative shows signs of fatigue with an '
            f'estimated excess spend of '
            f'${recommendation["excess_spend"]:,.0f}.'
        )

        recommended_action = (
            "Review the creative and consider replacing or "
            "refreshing it."
        )

    return (
        what_happened,
        why_it_matters,
        recommended_action,
    )


# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="Performance Campaign Copilot",
    layout="wide",
)

st.title("Performance Campaign Copilot")
st.caption("Your prioritized campaign recommendations")


# -----------------------------
# Temporary Task List
# -----------------------------

if "tasks" not in st.session_state:
    st.session_state.tasks = []


# -----------------------------
# Load demo data
# -----------------------------

campaigns = pd.read_csv("data/campaigns.csv")
creatives = pd.read_csv("data/creatives.csv")

recommendations = []


# -----------------------------
# Campaign recommendations
# -----------------------------

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


# -----------------------------
# Creative recommendations
# -----------------------------

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


# -----------------------------
# Highest priority first
# -----------------------------

recommendations.sort(
    key=lambda item: item["priority"],
    reverse=True,
)


# -----------------------------
# Show recommendations
# -----------------------------

for recommendation in recommendations:

    with st.container(border=True):

        priority_label = get_priority_label(
            recommendation["priority"]
        )

        # Recommendation title
        st.subheader(recommendation["name"])

        # Priority label
        st.write(
            f'**{priority_label} · '
            f'Priority {recommendation["priority"]}**'
        )

        # Platform + type
        st.write(
            f'**{recommendation["platform"]} · '
            f'{recommendation["type"]}**'
        )

        # Scores
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Priority",
            recommendation["priority"],
        )

        col2.metric(
            "Severity",
            recommendation["severity"],
        )

        col3.metric(
            "Impact",
            recommendation["impact"],
        )

        col4.metric(
            "Confidence",
            recommendation["confidence"],
        )

        # Explanation
        what_happened, why_it_matters, recommended_action = (
            get_explanation(recommendation)
        )

        st.markdown("#### What happened")
        st.write(what_happened)

        st.markdown("#### Why it matters")
        st.write(why_it_matters)

        st.markdown("#### Recommended action")
        st.write(recommended_action)

        # Estimated financial impact
      

        # Unique ID for the task
        task_id = (
            f'{recommendation["platform"]}-'
            f'{recommendation["type"]}-'
            f'{recommendation["name"]}'
        )

        # Check if already approved
        already_approved = any(
            task["id"] == task_id
            for task in st.session_state.tasks
        )

        # Approve button
        if already_approved:

            st.success(
                "Approved · Added to Task List"
            )

        else:

            if st.button(
                "Approve",
                key=f"approve-{task_id}",
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
if st.button("Test AI connection"):
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    response = client.responses.create(
        model="gpt-6-luna",
        input="Reply with exactly: AI connection works"
    )

    st.success(response.output_text)