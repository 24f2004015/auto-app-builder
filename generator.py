# generator.py
import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_app(brief, attachments=[]):
    """
    Generate minimal app code and README using LLM.
    Returns dict: filename -> content
    """
    prompt = f"""
Build a minimal web app that follows this brief:
{brief}

Include HTML, CSS, JS. Provide code files in a JSON dictionary: filename -> content.
Also include a professional README.md describing setup, usage, code, license.
"""

    for att in attachments:
        prompt += f"\nAttachment {att['name']}: {att['url'][:100]}... (truncated)"

    response = openai.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_content = response.choices[0].message.content.strip()
    try:
        start = raw_content.index("{")
        end = raw_content.rindex("}") + 1
        json_text = raw_content[start:end]
        code_files = json.loads(json_text)
    except Exception as e:
        print("Error parsing LLM output:", e)
        code_files = {
            "index.html": "<h1>Error generating app</h1>",
            "README.md": "# Error generating app"
        }
    return code_files
