import os
import time
import gradio as gr
from openai import OpenAI
from openai.types.beta import Thread
from openai.types.beta.threads import Run, ThreadMessage, MessageContentText
from openai.pagination import SyncCursorPage


def submit_message(
    client: OpenAI,
    assistant_id: str,
    thread: Thread,
    user_message: str
):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def create_thread_and_run(
    client: OpenAI,
    assistant_id: str,
    user_input: str
):
    thread = client.beta.threads.create()
    run = submit_message(client, assistant_id, thread, user_input)
    return thread, run


def wait_on_run(
    client: OpenAI,
    run: Run,
    thread: Thread
):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(0.5)
    return run


def get_response(
    client: OpenAI,
    thread: Thread
):
    return client.beta.threads.messages.list(
        thread_id=thread.id,
        order="asc"
    )


def get_text(
    messages: SyncCursorPage[ThreadMessage]
) -> str:
    result = ""
    for m in messages:
        if isinstance(m.content, list) \
                and isinstance(m.content[0], MessageContentText):
            result = m.content[0].text.value
    return result


client = None
thread = None


def gradio_io(text: str, history: list) -> str:
    global client
    global thread
    if client is None:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if thread is None:
        thread, run = create_thread_and_run(
            client,
            os.environ.get("OPENAI_ASSISTANT_ID", ""),
            text
        )
    else:
        texts = []
        for h in history:
            if isinstance(h, list):
                texts.append("\n".join(h))
            else:
                texts.append(h)
        texts.append(text)
        run = submit_message(
            client,
            os.environ.get("OPENAI_ASSISTANT_ID", ""),
            thread,
            "\n".join(texts)
        )
    run = wait_on_run(client, run, thread)
    result = get_text(get_response(client, thread))
    return result


def main():
    demo = gr.ChatInterface(gradio_io)
    demo.launch(
        share=bool(
            os.environ.get("APP_SHARE", False)
        ),
        server_name=os.environ.get("APP_HOST", "0.0.0.0")
        if os.environ.get("APP_HOST") else None,
        server_port=int(
            os.environ.get("APP_PORT", 8080)
        ),
        auth=(
            os.environ.get("APP_USER", ""),
            os.environ.get("APP_PASSWORD", "")
        )
        if os.environ.get("APP_USER") and os.environ.get("APP_PASSWORD")
        else None
    )


print("Loanching App...")

main()
