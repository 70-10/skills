# 型の設計

型はリポジトリごとに一から決める。種類のファイルの「型の候補」は出発点にすぎない。決めたことは、すべて `schema.yaml` のどこかのキーに入る。各節の見出しの右に、対応するキーを書いた。schema.yaml に知らないキーや綴りの違うキーがあると、`context.py` は schema の誤りとして止まる（終了コード 2）。

## 1. 何に答えられるようにするか

種類のファイルの「よく問われること」と、調査で見つけた実際の問いを並べる。問いごとに「どのページを読めば答えられるか」を言えるまで、型を足したり削ったりする。答えられない問いが残ったら、型が足りないか、その問いは置き場の受け持ちではない。

## 2. ディレクトリと type（`dirs`）

ディレクトリは更新の仕方で分ける（[principles.md](principles.md)「置き場の形」）。`protocol` には次のどれかを書く。今は人が読むための印で、`context.py` は使っていない。

| protocol | 書き方 | 例 |
| --- | --- | --- |
| `overwrite` | 中身を書き換える | システム、用語 |
| `append-only` | 書き換えず、覆ったら後継のページを立てる | 決定、先例 |
| `status` | `status` が進み、決着したら結果のページを指す | 未決の論点 |

1 つのディレクトリに、複数の type を置いてよい（`types: [system, term]`）。どのディレクトリにも属さないページは `unknown-dir`、ディレクトリに置けない type のページは `unknown-type` で FAIL になる。

## 3. 1 ページか、束ねるか（`collections` `people`）

状態・後継・固有の出典を持たないもの（人物、短い用語）は、1 ファイルに束ねる。

- 束ねるファイルは `collections` に、bundle からの相対パスと type を書く。置き場所はどこでもよい（ディレクトリの外でもよい）
- 束ねるファイルにも frontmatter が要り、`common.required` のキーと、決めた type を持たせる。type が違えば `unknown-type` になる
- 項目は `## <id> <見出しの残り>` の形で書く。`<id>` は見出しの最初の語で、後ろに続ける語とは半角スペースで区切る
- 束ねるファイルは、どこからもリンクされていなくても `orphan` にならない
- 人物を束ねたファイルを `people` に指定すると、そこにある id だけが `human:<id>` として使える

## 4. キー（`common` `types` `enums` `date_keys` `person_keys` `source_kinds`）

- **全ページに要るもの**: `type` `title` `description` `sources` を `common.required` に入れる
- **あってよいもの**: `aliases` `tags` `generated` `verified` `stale_after` `status` `superseded_by` `supersedes` `related` `rendered_in` など。`common.optional` か `types.<type>.optional` に無いキーは、audit が FAIL にする。キーを足すときは、先に schema.yaml を直す
- **type ごとに要るもの**: `types.<type>.required`。担当が替わると失われるもの（選んだ理由・見送った案・崩れる条件）から選ぶ
- **語彙**: `enums`（全体）と `types.<type>.enums`（その type だけ）。同じキーがあれば type の方を使う
- **日付**: `date_keys` のキーは `YYYY-MM-DD` で、暦にある日付でなければ FAIL
- **確認の印**: `verified` は `{by: human:<id>, at: YYYY-MM-DD}` の形でなければ FAIL。形の合わないものは `--report` で未確認に数える
- **人物**: `person_keys` の値と `verified.by` は `human:<id>` の形で書く。形が違うか、`people` のファイルに無ければ FAIL。`person_keys` を使うなら `people` は必須。`<id>` は、本人を一意に指せる短い英数字にする（アカウント名など）
- **ページどうしの参照**: `superseded_by` `supersedes` `related` と本文のリンクは、そのページからの相対パスで書く。`/` で始めるとリポジトリのルートから解く（GitHub での見え方と同じ）。`related` は本文のリンクと同じに扱われ、リンク切れと `orphan` の判定に数えられる。コードブロックやインラインコードの中のリンクは数えない

### 出典（`sources`）

各ページは、元の資料を 1 件以上指す。形は `{kind, resource}` にする。

- `resource` は、リポジトリのルートからのパスそのもの（行番号などの位置を付けない）か URL。位置を残したいときは、別のキー（`at` など）に書く。取り込み漏れの判定は、このパスの一致で見る
- `kind` の語彙（議事録・文書・会話・コードなど）は種類に合わせて決め、`source_kinds` に並べると audit が語彙の外を FAIL にする
- 会話から得た事実は `kind: conversation`、`resource: conversation:YYYY-MM-DD` のように書く
- 推測しか根拠が無い事実は、ページにせず、ユーザーに確かめる

## 5. 本文の節（`types.<type>.sections`）

必須にした節の見出し（`## <名前>`）が無ければ、audit が FAIL にする。節は「担当が替わると失われるもの」を書かせるために使い、数は 2〜4 にとどめる。

## 6. ファイル名と長さ（`filename` `max_body_lines`）

ファイル名の正規表現と、本文の行数の上限を決める。上限を超えると WARN になる。長いページは、元の資料へのリンクに置き換える合図。

## 7. 取り込み漏れ（`inflows` `deferred`）

資料の入り口のファイルを、リポジトリのルートからの glob で `inflows` に書く（例: `meeting-minutes/*.md`）。どのページの `sources[].resource` からも、本文のリンクや `related` からも指されていないファイルは、audit が `inflow` で FAIL にする。

- 初回の取り込みで後回しにしたファイルは、`deferred` に glob かパスで書く。これは FAIL ではなく `deferred` の WARN になり、取り込んだら自動で消える。取り込み終えたら `deferred` から外す
- 取り込む価値が無いと判断したファイルは、`deferred` に入れず、`inflows` の glob から外れるようにする

## 8. 正の置き場

事実の種類ごとに、正がどこにあるか（この置き場・元の文書・Issue・外部）を表にする。表は、生成するローカル skill の SKILL.md に書く。人が読む文書と同じ事実を持つときは、どちらを正にするかを決める。置き場を正にして文書へ写すなら、文書側の節を `rendered_in` に書く。

## 9. 分からないことの行き先

自分が分かっていないこと（情報の場所、仕様の理由、誰に聞くか）は、置き場の未決の論点に混ぜない（[principles.md](principles.md)「手入れ」）。リポジトリに Issue などの仕組みがあればそこへ、無ければ報告に挙げてユーザーに渡す。

## 10. 起きやすい設計の失敗

- 「何についてか」でディレクトリを細かく分け、更新の仕方が混ざる
- 人物や用語を 1 人 1 ページにして、ページが膨らむ
- 必須キーを増やしすぎて、AI が空欄を推測で埋める
- `stale_after` を全ページに付ける
