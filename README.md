# AI Marketing Campaign Analyst

An AI-powered marketing analytics agent built with Python, Streamlit, and Anthropic Claude.

## Features
- Upload campaign performance data using CSV files
- Calculate ROAS, CPA, and conversion rate
- Compare campaign performance across platforms
- Simulate budget reallocations using historical ROAS
- Generate AI-powered insights and recommendations

## Technology
Python, Pandas, Streamlit, Anthropic Claude API, Claude tool use

## How to Run
1. Install dependencies: `pip install streamlit pandas anthropic python-dotenv`
2. Configure your `ANTHROPIC_API_KEY` environment variable.
3. Run: `python3 -m streamlit run marketing_app.py`
4. Upload a campaign CSV and ask the agent a question.

## Limitations
Budget simulations assume historical ROAS remains constant. Results are hypothetical scenarios, not causal forecasts or guaranteed outcomes.

## Project Status
Working MVP — portfolio project.