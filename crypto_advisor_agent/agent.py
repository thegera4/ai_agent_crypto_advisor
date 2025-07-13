import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
import requests

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
headers = {"Accept": "application/json", "x-cg-demo-api-key": COINGECKO_API_KEY}


def get_deepseek_model(model_name: str = "deepseek/deepseek-chat") -> LiteLlm:
    """Utility function that returns a LiteLlm model instance for DeepSeek.
    Args:
        model_name (str): The name of the DeepSeek model to use. Defaults to "deepseek/deepseek-chat".
    Returns:
        LiteLlm: An instance of the LiteLlm model configured with the specified model name and API key.
    """
    return LiteLlm(model=model_name, api_key=DEEPSEEK_API_KEY,)


def get_current_value() -> dict:
    """Agent tool that calls COINGECKO API and returns the current value my cryptocurrencies.

    Returns:
        dict: status and result or error msg.
    """
    base_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum,pepe,popcat,bitcoin,shiba-inu,neiro-3",
        "vs_currencies": "mxn"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {"status": "success", "result": data}
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail += f" - Response: {e.response.text}"
            except:
                pass
        return {"status": "error", "error_message": error_detail}


def get_historical_data() -> dict:
    """
    Agent tool that retrieves historical data for my cryptocurrencies.

    Returns:
        dict: status and result or error msg.
    """
    base_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "mxn",
        "ids": "ethereum,pepe,popcat,bitcoin,shiba-inu,neiro-3",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": True
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {"status": "success", "result": data}
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail += f" - Response: {e.response.text}"
            except:
                pass
        return {"status": "error", "error_message": error_detail}


def get_analysis() -> dict:
    """
    Agent tool that analyzes the historical data of my cryptocurrencies and provides insights.
    Returns:
        dict: status and result or error msg.
    """
    pass


def get_investment_strategy() -> dict:
    """
    Agent tool that provides an investment strategy based on the current conditions and historical data.

    Returns:
        dict: status and result or error msg.
    """
    pass


root_agent = Agent(
    name="crypto_advisor_agent",
    model=get_deepseek_model(),
    description="Agent to provide information about certain cryptocurrencies, analyze trends, answer general questions"
                " about cryptocurrencies, and provide a good investment strategy.",
    instruction="""
        You are an expert in cryptocurrency analysis and investment strategies.
        You can provide information about the current value of cryptocurrencies, analyze trends, 
        and answer general questions about cryptocurrencies.
        If you don't have the information requested, you should respond with an error message.
        You can also provide investment strategies based on the current market conditions.
        If you are asked about a specific cryptocurrency, you should provide its current value.
        If you are asked about a general question, you should provide a detailed answer based on your knowledge.
        If you are asked about an investment strategy, you should provide a detailed strategy based on the 
        current market conditions and historical data.
        If you are asked something that is not related to cryptocurrencies, you should respond with an error message.
    """,
    tools=[get_current_value, get_historical_data],
)