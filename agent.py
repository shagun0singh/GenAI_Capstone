import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from tools import predict_price, get_market_data
from groq import Groq


class AgentState(TypedDict):
    input: dict
    price: float
    market_data: str
    advice: str


def predict_step(state):
    price = predict_price(state["input"])
    return {"price": price}


def retrieve_step(state):
    try:
        inp = state["input"]
        query = f"{inp['propertyType']} property with {inp['bedrooms']} bedrooms, {inp['tenure']} tenure, investment potential and risks"
        market_data = get_market_data(query)
        
        # Fallback if RAG returns no specific data
        if not market_data or len(market_data.strip()) < 10:
            market_data = "No specific local market trends found for this query. Use general real estate principles."
            
        return {"market_data": market_data}
    except Exception as e:
        print(f"Error in retrieval step: {e}")
        return {"market_data": "Retrieval service temporarily unavailable. Proceed with general advisory."}


def advise_step(state):
    price = state["price"]
    market_data = state["market_data"]
    inp = state["input"]

    prompt = f"""You are a professional real estate advisor. Based on the following information, provide a structured advisory report.

Property Details:
- Location: ({inp['latitude']}, {inp['longitude']})
- Bedrooms: {inp['bedrooms']}, Bathrooms: {inp['bathrooms']}
- Floor Area: {inp['floorAreaSqM']} sqm, Living Rooms: {inp['livingRooms']}
- Tenure: {inp['tenure']}, Type: {inp['propertyType']}

Predicted Price: £{price:,.2f}

Market Insights (from knowledge base):
{market_data}

Provide your analysis in EXACTLY this format:

**Price Evaluation:**
[State whether the predicted price seems cheap, fair, or expensive for this type of property, and explain why]

**Investment Advice:**
[Provide 2-3 specific investment recommendations based on the property details and market data]

**Risk Factors:**
[List 2-3 specific risks the buyer should consider]

CRITICAL INSTRUCTION: Keep your response concise and practical. Base your advice ONLY on the market insights provided above. If the provided market insights are insufficient or do not contain relevant facts, clearly state your uncertainty. Do NOT guess, assume, or hallucinate information not present in the market insights."""

    try:
        # Securely fetch the API key from the environment variable (or Streamlit Secrets)
        # On Streamlit Cloud, you configure this in your App Settings > Secrets
        api_key = os.environ.get("GROQ_API_KEY") or getattr(st, 'secrets', {}).get("GROQ_API_KEY")
        if not api_key:
            return {"advice": "⚠️ Error: GROQ_API_KEY is missing. Please check your .env file or Streamlit Secrets."}
            
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful real estate advisor. Be concise and practical."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        advice = response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower():
            advice = "⚠️ Rate limit exceeded on AI Advisor. Please wait a few moments and try again."
        elif "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
            advice = "⚠️ Authentication error: Invalid GROQ_API_KEY. Please verify your credentials."
        else:
            advice = f"⚠️ AI Advisor is temporarily offline: {error_msg}"

    return {"advice": advice}


def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("predict", predict_step)
    graph.add_node("retrieve", retrieve_step)
    graph.add_node("advise", advise_step)
    graph.add_edge(START, "predict")
    graph.add_edge("predict", "retrieve")
    graph.add_edge("retrieve", "advise")
    graph.add_edge("advise", END)
    return graph.compile()


def run_agent(input_data):
    agent = build_agent()
    initial_state = {"input": input_data, "price": 0.0, "market_data": "", "advice": ""}
    return agent.invoke(initial_state)
