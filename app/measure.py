"""モデルの応答時間とトークン数を計測して記録する。"""

import argparse
from datetime import datetime
from pathlib import Path
from time import perf_counter

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

LOG_PATH = (
    Path(__file__).resolve().parents[1]
    / "lectures"
    / "01"
    / "perf_log.md"
)
DEFAULT_QUESTION = "LoRAとは何ですか？"


def measure(question: str) -> str | None:
    client = genai.Client(api_key=get_api_key())

    # API呼び出しにかかった時間を計測する
    start_time = perf_counter()
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
    )
    elapsed_seconds = perf_counter() - start_time

    usage = response.usage_metadata
    if usage is None:
        prompt_tokens = "取得不可"
        output_tokens = "取得不可"
        total_tokens = "取得不可"
    else:
        prompt_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_tokens = usage.total_token_count

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    escaped_question = question.replace("|", r"\|").replace("\n", "<br>")

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    is_new_log = not LOG_PATH.exists() or LOG_PATH.stat().st_size == 0

    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        if is_new_log:
            log_file.write(
                "# モデル計測ログ\n\n"
                "| 記録日時 | モデル | 質問 | 応答時間 (秒) "
                "| 入力トークン数 | 出力トークン数 | 合計トークン数 |\n"
                "|---|---|---|---:|---:|---:|---:|\n"
            )

        log_file.write(
            f"| {timestamp} | {MODEL} | {escaped_question} "
            f"| {elapsed_seconds:.3f} | {prompt_tokens} "
            f"| {output_tokens} | {total_tokens} |\n"
        )

    print(f"応答時間: {elapsed_seconds:.3f} 秒")
    if usage is None:
        print("トークン数: 利用できませんでした")
    else:
        print(f"入力トークン数: {prompt_tokens}")
        print(f"出力トークン数: {output_tokens}")
        print(f"合計トークン数: {total_tokens}")

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="モデルの応答時間とトークン数を計測する"
    )
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")

    try:
        print(measure(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()