import time

from ai_nutritionist.memory.vector_store import get_vector_store


def typewriter_effect(message, container, speed=0.03):
    """Displays message letter by letter in a given Streamlit container."""
    typed_text = ""
    for letter in message:
        typed_text += letter
        container.markdown(typed_text)
        time.sleep(speed)


def get_memories():
    vector_store = get_vector_store()
    return vector_store.get_all_memories()
