import time

import streamlit as st

from ai_nutritionist.memory.vector_store import get_vector_store


def typewriter_effect(message, container, speed=0.03):
    """Displays message letter by letter in a given Streamlit container."""
    typed_text = ""
    for letter in message:
        typed_text += letter
        container.markdown(typed_text)
        time.sleep(speed)


def get_memories() -> dict[str, str]:
    vector_store = get_vector_store()
    return vector_store.get_all_memories()


def delete_memory(memory_id):
    """Delete a memory from session state and rerun."""
    st.session_state.memories.pop(memory_id, None)
    vector_store = get_vector_store()
    vector_store.delete_memory(memory_id)
    st.rerun()
