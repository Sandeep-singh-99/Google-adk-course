from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

from google.genai import types


def input_guardrail(
    callback_context: CallbackContext,
    llm_request: LlmRequest
):

    blocked_keyword = "BLOCK"

    if not llm_request.contents:
        return None

    last_user_message = ""

    for content in reversed(llm_request.contents):

        if content.role == "user" and content.parts:

            last_user_message = " ".join(
                part.text or ""
                for part in content.parts
            )

            break

    if blocked_keyword in last_user_message.upper():

        callback_context.state["request_blocked"] = True

        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="Sorry, this request was blocked."
                    )
                ]
            )
        )

    # Allow the model call
    return None