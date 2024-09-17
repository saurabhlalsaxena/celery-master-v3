from celery_app import app
import requests
from langserve import RemoteRunnable
import asyncio

# @app.task
# def perplexity_clone_api_task(main_url: str, user_message: str, query_id: str):
#     api_url = f"{main_url}/api/v1/search/invoke/"
#     inputs = {
#         "query": user_message,
#         "thread_id": query_id
#     }
#     headers = {
#         'accept': 'application/json',
#     }
#     try:
#         result = requests.post(api_url, headers=headers, json={"input": inputs})
#         result.raise_for_status()
        
#         data = result.json()
#         ai_response = data['output']['answer']
        
#         return {"answer": ai_response}
#     except requests.RequestException as e:
#         return {"answer": f"Error: {str(e)}"}

@app.task(name='perplexity_clone_api')
async def perplexity_clone_api(main_url: str, user_message: str, query_id: str):
    api_url = f"{main_url}/api/v1/search"
    inputs = {
        "query": user_message,
        "thread_id": query_id
    }
    remote_runnable = RemoteRunnable(api_url)
    try:
        response = await remote_runnable.ainvoke(input=inputs)
    except:
        response = {'answer':"API call failed"}

    return response# Add more tasks as needed
