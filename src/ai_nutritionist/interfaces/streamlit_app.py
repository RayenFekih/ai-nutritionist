import streamlit as st

from ai_nutritionist.graph.graph import graph
from ai_nutritionist.interfaces import get_memories, typewriter_effect

if "memories" not in st.session_state:
    st.session_state.memories = get_memories()

with st.sidebar:
    thread_id = st.text_input(
        ":grey-background[Chat Session Name]", value="001", key="thread_id")
    st.title("Memories")

    # Display stored memories
    for memory in st.session_state.memories:
        st.markdown(f"- {memory}")

    # Refresh button
    if st.button("Refresh Memories"):
        st.session_state.memories = get_memories()
        st.rerun()

st.title("Nutritionist Chatbot 🍎💬")
st.caption("This chatbot is under developement")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I'm your AI Nutritionist—here to help you eat smarter and feel better. How can I assist you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = graph.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        {"configurable": {"thread_id": thread_id}}
    )
    msg = response["messages"][-1].content

    with st.chat_message("assistant"):
        container = st.empty()
        typewriter_effect(msg, container)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})
