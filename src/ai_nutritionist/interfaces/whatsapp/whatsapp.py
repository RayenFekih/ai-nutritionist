import logging
import os

import httpx
from fastapi import APIRouter, Request, Response
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from ai_nutritionist.graph import graph_builder
from ai_nutritionist.settings import settings

logger = logging.getLogger(__name__)


whatsapp_router = APIRouter()


WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")


@whatsapp_router.api_route("/whatsapp_response", methods=["GET", "POST"])
def whatsapp_handler(request: Request) -> Response:
    """Handles incoming messages and status updates from the WhatsApp Cloud API."""

    if request.method == "GET":
        params = request.query_params
        if params.get("hub.verify_token") == os.getenv("WHATSAPP_VERIFY_TOKEN"):
            return Response(content=params.get("hub.challenge"), status_code=200)
        return Response(content="Verification token mismatch", status_code=403)

    try:
        data = request.json()
        change_value = data["entry"][0]["changes"][0]["value"]
        if "messages" in change_value:
            message = change_value["messages"][0]
            from_number = message["from"]
            session_id = from_number

            # Get user message and handle different message types
            content = ""
            content = message["text"]["body"]

            # Process message through the graph agent
            with SqliteSaver.from_conn_string(
                settings.SHORT_TERM_MEMORY_DB_PATH
            ) as short_term_memory:
                graph = graph_builder.compile(checkpointer=short_term_memory)
                graph.invoke(
                    {"messages": [HumanMessage(content=content)]},
                    {"configurable": {"thread_id": session_id}},
                )

                # Get the workflow type and response from the state
                output_state = graph.aget_state(
                    config={"configurable": {"thread_id": session_id}}
                )

            response_message = output_state.values["messages"][-1].content

            success = send_response(from_number, response_message, "text")

            if not success:
                return Response(content="Failed to send message", status_code=500)

            return Response(content="Message processed", status_code=200)

        elif "statuses" in change_value:
            return Response(content="Status update received", status_code=200)

        else:
            return Response(content="Unknown event type", status_code=400)

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return Response(content="Internal server error", status_code=500)


def send_response(
    from_number: str,
    response_text: str,
) -> bool:
    """Send response to user via WhatsApp API."""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    json_data = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "type": "text",
        "text": {"body": response_text},
    }

    print(headers)
    print(json_data)

    with httpx.Client() as client:
        response = client.post(
            f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages",
            headers=headers,
            json=json_data,
        )

    return response.status_code == 200
