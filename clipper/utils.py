import requests
from bs4 import BeautifulSoup
import json

def fetch_text_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator='\n', strip=True)
    return text

def clip_prod(url):
    page_text = fetch_text_from_url(url)

    if page_text:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"{page_text}\n\nReturn a JSON with keys: product_name, member_price, actual_price, description, and supplier."
                    }
                ],
            })
        )

        # Extract and print just the JSON content inside the code block
        try:
            assistant_content = response.json()['choices'][0]['message']['content']
            if assistant_content.startswith("```json"):
                json_str = assistant_content.strip("```json").strip("```").strip()
                parsed = json.loads(json_str)
                return json.dumps(parsed, indent=2, ensure_ascii=False)
            else:
                return
        except Exception as e:
            return
