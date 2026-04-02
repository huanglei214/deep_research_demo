import os
from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.tools import tool
from langchain_tavily import TavilySearch
from src.models.chat_model import chat_model


class Context(TypedDict):
    user_role: str


tavily_search = TavilySearch(max_results=5, topic="general")


@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """根据用户角色生成系统提示。"""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "你是一个有帮助的助手。"

    if user_role == "expert":
        return f"{base_prompt} 提供详细的技术响应。"
    elif user_role == "beginner":
        return f"{base_prompt} 简单解释概念，避免使用行话。"

    return base_prompt


@tool
def web_search(query: str) -> str:
    """根据查询词执行网页搜索并返回精简后的结果摘要。"""
    if not os.getenv("TAVILY_API_KEY"):
        return "TAVILY_API_KEY 未设置，无法执行 web_search。"

    result = tavily_search.invoke({"query": query})
    answer = result.get("answer")
    results = result.get("results", [])

    if not results and not answer:
        return "未找到相关搜索结果。"

    sections: list[str] = []
    if answer:
        sections.append(f"摘要：{answer}")

    for index, item in enumerate(results[:5], start=1):
        title = item.get("title", "无标题")
        url = item.get("url", "")
        content = item.get("content", "")
        sections.append(f"{index}. {title}\n链接：{url}\n内容：{content}")

    return "\n\n".join(sections)


agent = create_agent(
    model=chat_model,
    tools=[web_search],
    middleware=[user_role_prompt],
    context_schema=Context,
)

# 系统提示将根据上下文动态设置
result = agent.invoke(
    {"messages": [{"role": "user", "content": "解释机器学习"}]},
    context={"user_role": "expert"},
)
print(result)
