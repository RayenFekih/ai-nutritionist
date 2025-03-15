from src.ai_nutritionist.graph.graph import graph


def stream_graph_updates(user_input: str):
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": "2"}},
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()


if __name__ == "__main__":

    while True:
        # try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
