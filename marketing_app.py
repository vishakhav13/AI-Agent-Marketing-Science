
import streamlit as st
import pandas as pd
import anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Marketing Analyst", layout="wide")

st.title("AI Marketing Campaign Analyst")
st.write("Upload your campaign data to analyze marketing performance.")

uploaded_file = st.file_uploader(
    "Upload your marketing campaign CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Campaign data uploaded successfully!")
    st.subheader("Campaign Performance Data")
    st.dataframe(df)
    
    if st.button("Analyze Campaigns with AI"):
        with st.spinner("Claude is analyzing your campaigns..."):
            client = anthropic.Anthropic()

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=900,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        You are a senior marketing measurement analyst.

                        Analyze this campaign data:
                        {df.to_csv(index=False)}

                        Identify:
                        1. The strongest direct-response campaign.
                        2. Campaigns that need investigation.
                        3. Three practical recommendations.

                        Consider campaign objectives and
                        attribution limitations.
                        Do not invent missing information.
                        Keep your report concise.
                        """
                    }
                ]
            )

        st.subheader("AI Campaign Analysis")
        st.write(response.content[0].text)

def calculate_campaign_metrics(df):
    results = df.copy()

    results["ROAS"] = (
        results["Revenue"] / results["Spend"]
    )

    results["CPA"] = (
        results["Spend"] / results["Conversions"]
    )

    results["CVR"] = (
        results["Conversions"] / results["Clicks"] * 100
    )

    return results

if uploaded_file is not None:
    metrics = calculate_campaign_metrics(df)

    st.subheader("Calculated Campaign Metrics")
    st.dataframe(
        metrics[["Platform", "Campaign", "ROAS", "CPA", "CVR"]]
    )

campaign_tools = [
    {
        "name": "calculate_campaign_metrics",
        "description": (
            "Calculate ROAS, CPA, and conversion rate "
            "for the uploaded marketing campaigns."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

campaign_tools.append({
    "name": "simulate_budget_reallocation",
    "description": (
        "Simulate moving marketing budget from one campaign "
        "to another using historical ROAS. "
        "Returns a hypothetical revenue change, not a forecast."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "from_campaign": {
                "type": "string",
                "description": "Campaign losing budget"
            },
            "to_campaign": {
                "type": "string",
                "description": "Campaign receiving budget"
            },
            "amount": {
                "type": "number",
                "description": "Budget amount to move"
            }
        },
        "required": [
            "from_campaign",
            "to_campaign",
            "amount"
        ]
    }
})





import anthropic

 


def simulate_budget_reallocation(df, from_campaign, to_campaign, amount):
    campaign_names = (
        df["Platform"].astype(str).str.strip()
        + " "
        + df["Campaign"].astype(str).str.strip()
    )

    source = df[
        (df["Campaign"].astype(str).str.casefold() == from_campaign.casefold())
        | (campaign_names.str.casefold() == from_campaign.casefold())
    ]

    target = df[
        (df["Campaign"].astype(str).str.casefold() == to_campaign.casefold())
        | (campaign_names.str.casefold() == to_campaign.casefold())
    ]

    if source.empty or target.empty:
        return {"error": "Campaign not found"}

    source = source.iloc[0]
    target = target.iloc[0]

    if amount <= 0 or amount > source["Spend"]:
        return {"error": "Invalid reallocation amount"}

    source_roas = source["Revenue"] / source["Spend"]
    target_roas = target["Revenue"] / target["Spend"]

    revenue_lost = amount * source_roas
    revenue_gained = amount * target_roas

    return {
        "from_campaign": from_campaign,
        "to_campaign": to_campaign,
        "budget_moved": amount,
        "new_source_budget": float(source["Spend"] - amount),
        "new_target_budget": float(target["Spend"] + amount),
        "estimated_revenue_lost": float(revenue_lost),
        "estimated_revenue_gained": float(revenue_gained),
        "estimated_net_revenue_change": float(revenue_gained - revenue_lost),
        "assumption": "Historical ROAS stays constant. This is a scenario, not a forecast."
    }

def ask_claude_with_tools(question, df):
    client = anthropic.Anthropic()

    messages = [
        {"role": "user", "content": question}
    ]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        tools=campaign_tools,
        messages=messages
    )

    while response.stop_reason == "tool_use":
        messages.append({
            "role": "assistant",
            "content": response.content
        })

        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                if block.name == "calculate_campaign_metrics":
                    metrics = calculate_campaign_metrics(df)

                    result = metrics[
                        ["Platform", "Campaign", "ROAS", "CPA", "CVR"]
                    ].to_json(orient="records")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
                elif block.name == "simulate_budget_reallocation":
                    result = simulate_budget_reallocation(
                        df,
                        **block.input
                    )

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })


        messages.append({
            "role": "user",
            "content": tool_results
        })

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            tools=campaign_tools,
            messages=messages
        )

    return "\n".join(
    block.text for block in response.content
    if block.type == "text"
)

if uploaded_file is not None:
    st.subheader("Ask Your AI Marketing Agent")

    question = st.text_input(
        "What would you like to know about your campaigns?",
        placeholder="Which campaign has the highest ROAS?"
    )

    if st.button("Ask AI Agent"):
        if question.strip():
            with st.spinner("AI agent is analyzing your campaigns..."):
                answer = ask_claude_with_tools(question, df)

            st.markdown(answer)
        else:
            st.warning("Please enter a question.")
















