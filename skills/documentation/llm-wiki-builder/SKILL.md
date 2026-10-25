---
name: llm-wiki-builder
description: リポジトリに、AI エージェント向けの知識の置き場（LLM wiki。`projectcontext/` や `orgcontext/` などの `<kind>context/`）と、それを運用するリポジトリローカルの skill を新しく作り、初回の取り込みまで行う。種類と型はリポジトリごとに決め、型は schema.yaml に書き、index の生成と監査は同梱のスクリプトを写して使う。「このリポジトリに LLM wiki を作りたい」「projectcontext を導入したい」「経緯や前提を AI に持たせたい」「wiki の型を見直したい」と言われたときに使う。
---

# llm-wiki-builder

コードや文書を読むだけでは分からない「なぜそうなっているか」「何がもう決まっているか」は、関わった人の頭の中に残りがちである。それを出典と一緒にページへ書き出し、AI が探して引けるようにしたものを、ここでは「コンテキスト」と呼ぶ。

この skill は、対象のリポジトリに次の 3 つを作る。作ったあとの運用は、生成したローカル skill が受け持つ。

- `<kind>context/`: ページ・`schema.yaml`・`index.md`・`tools/context.py`（この skill の [scripts/context.py](scripts/context.py) の写し）
- `.claude/skills/<repo>-<kind>-context/`: 読み方と書き方を決めたローカル skill
- `CLAUDE.md`（または `AGENTS.md`）への短い追記

生成物はリポジトリの中だけで完結させる。`~/.claude/` の下は参照しない。ほかの人が clone しても動くようにするため。

## 最初に読むもの

- [references/principles.md](references/principles.md): LLM wiki の原則
- [references/context-kinds/README.md](references/context-kinds/README.md): 種類の見分け方
- [references/generated-skill.md](references/generated-skill.md): 生成するものの中身

## 起動の分岐

- 「LLM wiki とは」のような質問なら、答えて終わる
- 対象のリポジトリにすでに `*context/` とそれを扱う skill があれば、「[既存の bundle を見直すとき](#既存の-bundle-を見直すとき)」へ進む
- どちらでもなければ、下の手順で作る

## 手順

### 1. 調べる

対象のリポジトリを読み、繰り返し問われる事実と、その事実の入り口（議事録・文書・Issue・会話など）を洗い出す。ファイルはまだ作らない。調べる観点は [references/workflow-details.md](references/workflow-details.md) の「調査」にある。リポジトリの外にある入り口は推測せず、ユーザーに聞く。

### 2. 種類を決める

[context-kinds/README.md](references/context-kinds/README.md) の見分け方で候補を絞り、根拠と一緒に示してユーザーに選んでもらう。1 つのリポジトリに置く種類は 1 つにする。決めたら、その種類のファイルを読む。

### 3. 型を設計する

[references/ontology-design.md](references/ontology-design.md) に沿って、ディレクトリ・type・必須キー・語彙・集合ファイル・流入源・人物の参照先を決める。決めた内容は `schema.yaml` のキーにそのまま対応させる。雛形は [assets/schema.example.yaml](assets/schema.example.yaml)。

### 4. 設計の承認を取る

種類・型の設計・作るファイルの一覧をユーザーに見せて、承認を取る。型は後から変えにくいので、承認を取るのはここだけにする。見せる内容は [workflow-details.md](references/workflow-details.md) の「承認」にある。

### 5. 生成する

[generated-skill.md](references/generated-skill.md) に沿って、`schema.yaml`・`tools/context.py`・ローカル skill・`CLAUDE.md` への追記を作る。`context.py` は書き換えずに写す。リポジトリごとの違いは `schema.yaml` だけに書く。

作ったら、ページの無い状態で `context.py index` と `audit` を実行し、FAIL が 0 であることを確かめる。入り口のファイルがすでにあれば、この時点ではすべて `deferred` に書いておく。また、壊したページを一時的に置いて、ローカル skill に「FAIL になる」と書いた検査が実際に FAIL になることも確かめる。実行の仕方（`uv` か Python か）は [generated-skill.md](references/generated-skill.md) の「context.py」にある。

### 6. 初回の取り込み

生成したローカル skill の書き方の手順どおりに、既存の資料からページを起こす。手順どおりに書けない箇所があれば、それはローカル skill の欠陥なので、先にローカル skill を直す。

- 量が多いときは、重要なものから取り込む。取り込んだファイルは `deferred` から外し、残りは `deferred` に残して「未取り込み」として報告する
- `verified` は付けない（人が確かめた印なので）
- 最後に index → audit を実行し、FAIL を 0 にする（`deferred` の WARN は残ってよい）

### 7. 報告する

commit と push はしない。報告する内容は [workflow-details.md](references/workflow-details.md) の「報告」にある。件数は `audit --report` の出力から写し、手で数えない。

### 8. 確認を手伝う（ユーザーが望んだときだけ）

人に確かめたいこと（空欄・食い違い・同じ人物かどうか）を、選択肢の形で数件ずつ聞く。回答は出典として足してから反映する。承認されたページには、ユーザーの指示として `verified` を代わりに書く。

## 既存の bundle を見直すとき

既存の `schema.yaml`・ローカル skill・`git log -- <kind>context/` を読み、運用の実態をつかむ。そのうえで、見直し案（型の追加や統合、検査の追加、手順の欠陥の修正）を手順 4 と同じ形で見せる。

- 今の作りがこの skill と違っていても、欠陥と決めつけない。残すか合わせるかを選択肢で示す
- 型を変えるときは、既存ページの移し方とリンクの張り替えも案に入れる
- 既存の bundle に、この skill の `context.py` が無い場合（独自のスクリプトで動いている場合など）は、置き換えるかどうかも選択肢に入れる
