import requests
from bs4 import BeautifulSoup
import json

def fetch_text_from_url(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": url,
    "Connection": "keep-alive",
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
                "model": "openai/chatgpt-4o-latest",
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
