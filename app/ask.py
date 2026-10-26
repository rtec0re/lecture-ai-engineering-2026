"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import json
from pathlib import Path

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

HISTORY_PATH = Path(__file__).resolve().parents[1] / "lectures" / "01" / "ask-history.json"

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())

    #Coplilot利用
    if HISTORY_PATH.exists():
        saved_history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        history = [types.Content.model_validate(item) for item in saved_history]
    else:
        history = []

    chat = client.chats.create(
        model=MODEL,
        history=history,
        #config=types.GenerateContentConfig(
        #    temperature=0.0,
        #),
    )

    response = chat.send_message(
        question,
    )

    # 次回起動時に復元できるよう、質問と応答を含む履歴を保存する
    saved_history = [
        item.model_dump(mode="json", exclude_none=True)
        for item in chat.get_history()
    ]
    HISTORY_PATH.write_text(
        json.dumps(saved_history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）

    #   Github Copilotを利用した。
    usage = response.usage_metadata

    if usage is not None:
        print(f"入力トークン数: {usage.prompt_token_count}")
        print(f"出力トークン数: {usage.candidates_token_count}")
        print(f"合計トークン数: {usage.total_token_count}\n")
    else:
        print("usage_metadata は利用できませんでした")

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
