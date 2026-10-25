# 生成するもの

```
<repo>/
  CLAUDE.md                        # 追記（下の「CLAUDE.md への追記」）
  <kind>context/
    schema.yaml                    # 型・キー・語彙の正
    index.md                       # context.py index が作る。手で書かない
    tools/context.py               # この skill の scripts/context.py をそのまま写す
    <dir>/<page>.md ...
  .claude/skills/<repo>-<kind>-context/
    SKILL.md                       # 読み方・書き方の入り口
    references/authoring.md        # 書き方の詳しい手順
```

`<kind>context/` はリポジトリの直下に置く。`context.py` は bundle の 1 つ上をリポジトリのルートとみなし、`inflows` や `sources[].resource` をそこから解く。

ローカル skill の名前は、既定で `<リポジトリのディレクトリ名>-<kind>-context` にする。個人の `~/.claude/skills/` に同じ名前の skill があると、そちらが優先される。作る前に、自分の環境で名前が重なっていないかを確かめる。ほかの人の環境までは確かめられないので、リポジトリ名を頭に付けて重なりにくくする。

`schema.yaml` は [assets/schema.example.yaml](../assets/schema.example.yaml) から作る。写したら、先頭にある「この skill の references を見よ」というコメントは消す。生成先からは辿れないため。

## context.py

[scripts/context.py](../scripts/context.py) を `<kind>context/tools/` に写す。中身は書き換えない。リポジトリごとの違いは、すべて `schema.yaml` に書く。

```
uv run <kind>context/tools/context.py index            # index.md を作り直す
uv run <kind>context/tools/context.py audit            # FAIL があれば終了コード 1、schema の誤りは 2
uv run <kind>context/tools/context.py audit --report   # 件数・未確認・置き換え済みを JSON で足す
```

`uv` が PyYAML を用意する。`uv` が無い環境では、PyYAML を入れた Python 3.11 以上で `python3 <kind>context/tools/context.py index` のように動かす。どちらで動かすかは手順 4 の承認で決め、ローカル skill と CLAUDE.md の追記に書く。

audit の検査（コード → 直し方）:

| 段階 | コード | 意味 |
| --- | --- | --- |
| FAIL | `frontmatter` | frontmatter が読めない |
| FAIL | `missing-key` / `unknown-key` | 必須キーが無い / schema に無いキーがある |
| FAIL | `unknown-dir` / `unknown-type` | schema に無いディレクトリ / そのディレクトリ（または束ねるファイル）の type と違う |
| FAIL | `enum` / `date` / `filename` | 語彙に無い値（`sources[].kind` を含む） / 日付の形 / ファイル名の規則 |
| FAIL | `missing-section` | 必須の節が無い |
| FAIL | `broken-link` | 本文のリンク・`related`・`sources[].resource` の先が無い（コードの中のリンクは見ない） |
| FAIL | `unknown-person` | 人物の値が `human:<id>` の形でない、または人物のファイルに無い |
| FAIL | `verified` | `verified` が `{by: human:<id>, at: YYYY-MM-DD}` の形でない |
| FAIL | `supersede` | 新旧の片方しか相手を指していない、または status が合わない |
| FAIL | `alias-conflict` | 1 つの名前（題か別名）が 2 つのページを指す |
| FAIL | `inflow` | 入り口のファイルがどこからも参照されていない（取り込み漏れ） |
| FAIL | `index` | index.md が今のページと合わない |
| WARN | `deferred` | `deferred` に書いた、まだ取り込んでいない入り口のファイル |
| WARN | `stale` / `long-body` / `orphan` | `stale_after` を過ぎた / 本文が長い / どこからもリンクされていない |

## CLAUDE.md への追記

短く書く。中身はローカル skill に任せる。

```markdown
## <kind>context

このリポジトリの前提・経緯・決定は `<kind>context/` にある（AI 向けの置き場）。
答える前・作業の前に `/<repo>-<kind>-context` で引き、会話で新しい事実が出たら同じ skill で書く。
```

「新しい事実」の例を 2〜3 個、種類に合わせて添える（project なら「〜に決まった」「〜さんが担当になった」）。

## ローカル skill の SKILL.md

frontmatter の `description` には、読むときと書くときの両方の言い回しを入れる（「〜はどうなった」「〜に決まったので残して」）。本文に書く節は次のとおり。

1. **位置づけ**: 置き場は AI 向けであること。人が読む文書との分担。型の正は `schema.yaml`
2. **型の表**: ディレクトリ × type × 更新の仕方
3. **正の置き場の表**: [ontology-design.md](ontology-design.md) §8 で決めたもの
4. **読み方**: `index.md` の題・別名・要約から当たりを付け、ページを読み、必要ならリンクを 1 段だけたどる。`status` が `superseded` のページは、後継を読む。`verified` の無いページを根拠にするときは、その旨を答えに添える。index に無ければ元の資料から答え、その場でページを起こす
5. **書き方**: `references/authoring.md` へのリンク
6. **自分で書き足してよい範囲**: 会話や作業で分かった事実は、頼まれなくても書く。書かないものは、型や schema の変更（ユーザーに提案する）、`verified` の付与（頼まれて代わりに書く場合を除く）、人が読む文書の書き換え
7. **検査**: 上の audit のコマンドと、コードごとの直し方

## 書き方の手順（references/authoring.md）

1. **重なりの確認**: index を見て、同じ概念のページがあれば新しく作らずに直す
2. **置き場所の判定表**: 何を 1 ページにし、何を束ねたファイルに足し、何を作らないか（会議そのもの、人が読む文書に正がある事実、自分が分かっていないこと）
3. **frontmatter の雛形**: type ごとに、そのまま写して埋められる形にする。`generated` には、書いたときに動いていたモデルと skill の名前を `<モデル>/<skill 名>` の形で入れ、日付を添える。雛形の中ではモデルを `<モデル>` のまま残す。YAML の値に「空白と #」が続く箇所があればコメントと読まれるので、値を引用符でくくる
4. **別名の付け方**: 表記の揺れ・略称・旧名・相手側の呼び方・文字起こしの聞き違い。名前がぶつかったときに、どちらに残すかの決まり
5. **type ごとの決まり**: 種類のファイルの「取り込むときに気を付けること」を、このリポジトリの型に合わせて書く
6. **出典の書き方**: `sources` の `kind` の選び方。`resource` はファイルのパスそのものにし、位置は別のキーに書く（取り込み漏れの判定がパスの一致で見るため）。資料どうしが食い違うときは、両方を出典に挙げ、本文に食い違いを書く
7. **人が読む文書への反映**: `rendered_in` を付けたページを直したら、文書側も直す（直すかどうかをリポジトリの方針で決める）
8. **仕上げ**: index → audit で FAIL を 0 にし、変更をコミットメッセージの案と一緒に報告する。取り込みを後回しにした入り口のファイルは `deferred` に書き、報告に挙げる

## 変更の履歴とコミットメッセージ

- 履歴は `git log -- <kind>context/` と `git log --follow <kind>context/<dir>/<page>.md` で引く。`log.md` は作らない
- コミットメッセージには、意味のある変更（起こしたページ、直した事実、覆った決定）を書く。誤字の修正などは並べない
