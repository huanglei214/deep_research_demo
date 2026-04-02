import os

from langchain_openai import ChatOpenAI

chat_model = ChatOpenAI(
    model="ep-20260309171756-fc8tf",
    base_url="https://ark-cn-beijing.bytedance.net/api/v3",
    api_key=os.getenv("ARK_API_KEY"), # 你需要自己设置环境变量
    temperature=0,
)
