from deerflow.client import DeerFlowClient


def main():
    """运行最小 DeerFlowClient 示例。"""
    client = DeerFlowClient(thinking_enabled=False)
    # result = client.chat("请用一句话介绍 DeerFlow harness 的作用")
    # print(result)

    for event in client.stream("hello"):
        print(event.type, event.data)


if __name__ == "__main__":
    main()
