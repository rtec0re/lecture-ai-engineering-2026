# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：エージェントは一般論でなく、用語集検索ツールで知識を探るようになった
- `--trace` で見えたツール呼び出し（ツール名と引数）：
    - search_glossary({'query': 'LoRA'})
    - search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：2回
- 追加したツールと、docstring に書いた説明：
    - make_quiz()
    - docstring:
    """指定した回の用語から 1つを選び、確認問題と答えを返す。

    「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
    """

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：

### 取り組んだレベル

基礎

### やったこと

#### 1. 以下のファイル内容の変更
- `app/agent.py`
- `app/tools.py`

##### 変更した内容

一度に1か所だけ変更した。

agent.py 変更後：
- 回の内容を聞かれたら get_lecture_summary を使う。
を削除した。
INSTRUCTIONS = """\
あなたはAIエンジニアリング講座（AIE2026）の学習支援エージェントです。
- 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。
- 用語集に見つからないことは、推測で断定せず「用語集にはない」と伝える。
- 回答の最後に、関係する回（第N回）を示す。
- 宿題の答えそのものは書かず、考え方のヒントで導く。
"""

変更した理由：
- get_lecture_summary を使わないようになるか確認する

tools.py 変更後：
- get_lecture_summary() のdocstring に
類似要点は1つにまとめ、簡潔にする。
を追加した。
"""指定した回（1始まりの整数）の講義の要点を返す。

「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
類似要点は1つにまとめ、簡潔にする。
"""

##### 実行した質問

- "第3回では何を学ぶ？"

---

### 結果（`--trace` の出力や比較）

#### agent.py 変更前の `--trace` 出力

[model] gemini-3.5-flash-lite
第3回では「AIエージェント」をテーマに学びます。

主な内容は以下の通りです：
- **AIエージェントの基本構造**：「モデル ＋ ループ ＋ ツール」の組み合わせで目的を達成する仕組みの理解
- **ツールとエージェントループ**：LLMがツールを呼び出す仕組み、ツールの説明文の重要性、ループによるコスト（応答時間や料金）への影響
- **ハーネスとフレームワーク**：PiやPydantic AIなどを活用したエージェント開発、TestModelを使った効率的なテスト
- **安全性**：ガードレールやHuman-in-the-loop（人の確認）の重要性

（関連する回：第3回）

--- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント

## この回のねらい

- AIエージェントの基本構造が「モデル＋ループ＋ツール」であることを理解する
- Pydantic AIで、ツールを使う学習支援エージェントを自分で作り、動かす

## 要点

1.…
[usage] RunUsage(cost=Decimal('0.0008075'), details={'text_prompt_tokens': 1250}, input_text_tokens=1250, input_tokens=1250, output_tokens=173, requests=2, tool_calls=1)

#### agent.py 変更後の `--trace` 出力

[model] gemini-3.5-flash-lite
第3回では**「AIエージェント」**について学びます。

主な内容は以下の通りです：

* **AIエージェントの基本構造**：「モデル ＋ ループ ＋ ツール」の組み合わせで目的を達成する仕組みを理解する。
* **ツールとツールの説明文**：LLMがどのようにツールを選び、引数を決定するのか、説明文の重要性を学ぶ。
* **エージェントループのコスト**：LLMを複数回呼び出すことによる、時間・料金・レート制限への影響を理解する。
* **ハーネスとフレームワーク**：Pydantic AI や Pi などのハーネス・フレームワークを用いた具体的なエージェント開発を学ぶ。
* **ガードレールとHuman-in-the-loop**：安全なエージェント運用のための、権限制御や人の確認の挟み方を学ぶ。

（関連回：第3回）

--- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント

## この回のねらい

- AIエージェントの基本構造が「モデル＋ループ＋ツール」であることを理解する
- Pydantic AIで、ツールを使う学習支援エージェントを自分で作り、動かす

## 要点

1.…
[usage] RunUsage(cost=Decimal('0.0009035'), details={'text_prompt_tokens': 1220}, input_text_tokens=1220, input_tokens=1220, output_tokens=215, requests=2, tool_calls=1)

#### tools.py 変更前の `--trace` 出力
[model] gemini-3.5-flash-lite
第3回では「AIエージェント」をテーマに学びます。

主な内容は以下の通りです：
- **AIエージェントの基本構造**：「モデル ＋ ループ ＋ ツール」の組み合わせで目的を達成する仕組みの理解
- **ツールとエージェントループ**：LLMがツールを呼び出す仕組み、ツールの説明文の重要性、ループによるコスト（応答時間や料金）への影響
- **ハーネスとフレームワーク**：PiやPydantic AIなどを活用したエージェント開発、TestModelを使った効率的なテスト
- **安全性**：ガードレールやHuman-in-the-loop（人の確認）の重要性

（関連する回：第3回）

--- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント

## この回のねらい

- AIエージェントの基本構造が「モデル＋ループ＋ツール」であることを理解する
- Pydantic AIで、ツールを使う学習支援エージェントを自分で作り、動かす

## 要点

1.…
[usage] RunUsage(cost=Decimal('0.0008075'), details={'text_prompt_tokens': 1250}, input_text_tokens=1250, input_tokens=1250, output_tokens=173, requests=2, tool_calls=1)

#### tools.py 変更後の `--trace` 出力
[model] gemini-3.5-flash-lite
第3回では「**AIエージェント**」について学びます。

### 主な内容
- **AIエージェントの基本構造**：「モデル ＋ ループ ＋ ツール」の組み合わせで目的を達成する仕組みを理解します。
- **ツールとハーネス**：LLMが自ら判断してツールを呼び出す仕組みや、PiやPydantic AIなどのフレームワークを活用したエージェント開発を学びます。
- **ガードレールとHuman-in-the-loop**：取り消しにくい操作に対する安全対策や人の確認の挟み方を扱います。
- **演習**：用語集を検索できる学習支援エージェントを実際に動かしたり、ツールを追加したりする体験をします。

（関連回：第3回）

--- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント

## この回のねらい

- AIエージェントの基本構造が「モデル＋ループ＋ツール」であることを理解する
- Pydantic AIで、ツールを使う学習支援エージェントを自分で作り、動かす

## 要点

1.…
[usage] RunUsage(cost=Decimal('0.0008478'), details={'text_prompt_tokens': 1276}, input_text_tokens=1276, input_tokens=1276, output_tokens=186, requests=2, tool_calls=1)

#### 3. ツール呼び出しの比較

| 比較項目 | agent.py 変更前 | agent.py 変更後 | tools.py 変更前 | tools.py 変更後 |
|---|---|---|---|---|
| ツールの呼ばれ方 | --- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント | --- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント | --- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント | --- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # 第3回 AIエージェント |
| ツールの呼び出し回数 | 2 | 2 | 2 | 2 |
| ツールに渡された引数 | {'lecture': 3} | {'lecture': 3} | {'lecture': 3} | {'lecture': 3} |

#### 4. 回答の変化

##### agent.py
- 要点の表示の仕方が変わった。
- 内容は同じ。

##### tools.py
- 要点の個数が減った。
- 内容が圧縮され、文章量が少なくなった。
- 体言止めを使用した。

---

### 気づき・疑問

気づいたこと：

- ツールの呼ばれ方・呼び出し回数・引数は変更前後で変化なし
- 回答は変更前後で、tools.py の変更に鍵って、要点の個数と文章量が減った。
- 指示または docstring の変更が、エージェントの動作に与えた影響：
    - 変更によって同じ内容でも表示に微妙な差異が出た。
    - 簡潔にという表現も、体言止めという形式で対応していた。

疑問：
- 差異が生まれる変更の仕方が知りたい