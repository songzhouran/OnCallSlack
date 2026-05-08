from playwright.sync_api import sync_playwright
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import random

load_dotenv()
llm_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

CHANNEL_URL = os.getenv("CHANNEL_URL")

processed = set()


def ask_ai(text):

    response = llm_client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content":
                    "You are a concise Slack assistant."
            },
            {
                "role": "user",
                "content": text
            }
        ],

        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="./slack_profile",
        headless=False
    )

    page = context.new_page()

    print("open channel...")

    page.goto(CHANNEL_URL)

    page.wait_for_load_state("domcontentloaded")

    print("channel opened...")

    while True:

        try:

            items = page.locator(
                '[data-qa="virtual-list-item"]'
            )

            count = items.count()
            print("count:", count)

            if count == 0:
                time.sleep(2)
                continue

            latest = None
            text_locator = None

            for i in range(count - 1, -1, -1):

                candidate = items.nth(i)

                candidate_text = candidate.locator(
                    '[data-qa="message-text"]'
                )

                if candidate_text.count() > 0:
                    latest = candidate
                    text_locator = candidate_text

                    break

            if latest is None:
                time.sleep(1)
                continue

            text = text_locator.inner_text().strip()

            sender = ""

            sender_locator = latest.locator(
                '[data-qa="message_sender_name"]'
            )

            if sender_locator.count() > 0:
                sender = sender_locator.inner_text().strip()

            message_key = f"{sender}:{text}"
            print("message_key", message_key)

            if message_key in processed:
                time.sleep(1)
                continue

            processed.add(message_key)

            print(f"\n[{sender}] {text}")

            trigger_words = os.getenv(
                "TRIGGER_WORDS",
                ""
            ).split(",")

            triggered = False

            for word in trigger_words:
                if word.lower() in text.lower():
                    triggered = True
                    break

            if sender.lower() == os.getenv("sender_no_trigger"):
                triggered = False


            if triggered:

                print("AI processing...")

                reply = ask_ai(text)

                print("AI:", reply)

                box = page.locator(
                    'div[role="textbox"]'
                ).last

                box.click()

                page.keyboard.type(
                    reply,
                    delay=random.randint(20, 50)
                )

                time.sleep(
                    random.uniform(0.5, 1.5)
                )

                page.keyboard.press("Enter")

                print("sent")

            time.sleep(
                random.uniform(60, 90)
            )

        except Exception as e:

            print("error:", e)

            time.sleep(10)