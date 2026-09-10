# refine verification using Issue #22

Source: https://github.com/70-10/skills/issues/22

Applied the updated `skills/thinking/refine/SKILL.md` to the actual issue body and its empty comment history. The following is a complete proposed body for verification; it has not been approved or published to GitHub. Validation is a manual review of the generated body, not an automated or independent execution test.

## Proposed issue body

### 背景・目的

`refine` は既に委ねた判断と停止条件を要求しているが、委任の列挙漏れの扱い、判断の誤りを検出する完了条件、人の同席なしに評価できる停止条件が明確でない。生成する Issue 本文の形式精度を上げ、後続エージェントが自律的に進める判断と確認が必要な判断を切り分けられるようにする。

例えば、CLI の rename が frontmatter の仕様外のキーを失わせても、正規形のページしか検証しない完了条件はすべて通ってしまう。こうした判断の誤りを、Issue の完了条件で検出できるようにする。

### 対象・制約

`skills/thinking/refine/SKILL.md` に以下を要求する記述を加える。

1. 本文提示前に委ねる判断を洗い出し、漏れなく列挙する。列挙されていない判断は委任されておらず、後続エージェントは決定前に停止して確認する、と生成する本文に明記する。
2. 期待結果や制約を定める判断を反転させると、少なくとも一つの完了条件が不成立になるようにする。どちらでも要件を満たす委任済みの実装方法は固定しない。
3. 停止条件は人の同席なしに観測・評価できるトリガーとして書き、それぞれに止まる理由の種類を併記する。

既存の委任方針、本文の要求項目、本文更新前の承認、title・labels 等の扱いを維持する。外部の判定手続きの項目番号、他リポジトリの非公開 skill の内部構造、特定のコーディングエージェントに依存する語彙・ツール名を追加しない。

### 完了条件・検証方法

- C1: 生成する本文に未列挙の判断は委任されておらず確認が必要と明記する要求がある。SKILL.md と適用例の両方を読み、未列挙の判断を自動的に許可する余地がないことを確認する。
- C2: 本文提示前に委任判断を洗い出し、列挙漏れを確認する手順がある。調査・設計・実装・検証の通常の選択も委任範囲に含められることを確認する。
- C3: 期待結果・制約を定める判断ごとに反転テストを行い、全完了条件が通るなら条件と検証方法を補強する要求がある。「客観的に判定できる」だけでは成立しない。
- C4: 各停止条件に、人の同席を要しない観測可能なトリガーと理由の種類を要求している。人が問題に気づくことだけをトリガーとする記述では成立しない。
- C5: 差分に外部の判定手続きの項目番号、他リポジトリの skill 内部構造、特定エージェントに依存する語彙・ツール名の追加がない。
- C6: 目的・背景・期待結果、スコープと制約、完了条件と検証方法、委ねた判断、停止条件、必要な実装方針の要求が残り、既存の委任方針と承認・メタデータ方針を維持している。変更前後を比較する。
- C7: 更新後の skill を実際の Issue に適用した完全な本文案と、要求上の判断を反転させた場合に失敗する完了条件の対応を記録する。各反転で少なくとも一つが不成立になることを手動確認する。

`git diff --check` で差分の空白エラーがないことも確認する。これは意味的な検証の代わりにはならない。

### 後続エージェントに委ねる判断

- 調査: この Issue とリポジトリ内の関連文書から、既存の要求や検証方法を確認するための読み取り手順。
- 設計・実装: 三つの要求を散文または既存の箇条書きへ配置する方法と具体的な英文。上記の要求と既存方針を変えない範囲に限る。
- 表現: 止まる理由の語彙・粒度、停止条件と委任判断の例示の有無。外部の非公開手続きや特定エージェントへの依存を加えない範囲に限る。
- 検証: 実際の Issue への適用で使う具体例、手動検証の手順と記録形式。完全な本文案と反転テスト結果を確認できる形にする。

ここに列挙されていない判断は委任されていない。後続エージェントは決定前に停止し、確認を求める。

### 停止条件

- 必要な判断を上記の委任項目・範囲に対応付けられない場合。理由: 未委任の判断。
- 調査で得た要件とこの Issue の要求が両立せず、片方を破棄・変更する必要がある場合。理由: 要件の衝突。
- 実装案が既存の委任方針、承認手順、メタデータの扱いの変更を必要とする場合。理由: 合意したスコープの逸脱。

停止時は該当する判断や衝突する記述を示して確認を求める。

## Manual reversal review

| Required decision | Reversed behavior | Failing criterion |
| --- | --- | --- |
| Unlisted decisions require clarification | Treat an unlisted decision as implicitly authorized | C1 |
| Inventory delegation before presentation | Present the body without checking delegation omissions | C2 |
| Criteria distinguish required behavior from its opposite | Accept objective checks that pass for both alternatives | C3 |
| Stops can be evaluated without a person present | Stop only when a human reviewer notices a problem | C4 |
| Stops include a reason category | Include a trigger without its stopping reason | C4 |
| Keep the skill independent of external procedures and agents | Add private procedure numbers or agent-specific tools | C5 |
| Preserve existing requirements and delegation policy | Drop a required body element or require approval of all routine choices | C6 |
| Validate through a real issue application | Provide only a claim of validation without a body or reversal results | C7 |

All eight reversed behaviors fail at least one explicit criterion in the proposed body. Choosing prose instead of bullets, or changing the reason vocabulary without changing its meaning, intentionally passes: those choices are delegated.

The frontmatter example also distinguishes the two cases: a criterion such as “rename succeeds on a canonical page” passes whether unknown keys are kept or lost. A criterion that compares an input containing an unknown key and its nested value with the renamed output, expecting that key and value to be preserved, fails when they are dropped. This is an illustrative manual check of criterion design; no CLI execution is claimed.

The source background associates missing delegation with unnecessary escalation, while its explicit scope requires escalation for unlisted decisions. These are reconciled by requiring a pre-presentation inventory that covers routine choices, while retaining the explicit fallback for remaining omissions.
