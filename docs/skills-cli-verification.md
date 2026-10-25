# skills CLI compatibility verification

Verified on 2026-10-25 with `skills` CLI 1.7.4.

## Scope

The CLI checks verify discovery and project-level installation compatibility. The bundle checks below cover script behavior and documentation structure. Runtime response quality and identical behavior across agents are outside the verification scope.

## Commands

Run discovery against the repository root:

```sh
npx skills add . --list
```

Run isolated project installations from separate temporary directories:

```sh
npx skills add /path/to/repository --skill '*' --agent claude-code --copy --yes
npx skills add /path/to/repository --skill '*' --agent codex --copy --yes
```

## Results

- Discovery returned exactly ten skills: `adr`, `align`, `brief`, `discover`, `elaborate`, `first-bet`, `investigate`, `llm-wiki-builder`, `refine`, and `tdd`.
- Discovery did not return `dev`, `flow`, `decompose`, `implement`, `verify`, or `review`.
- Claude Code project installation created all ten `SKILL.md` files under `.claude/skills/`.
- Codex project installation created all ten `SKILL.md` files under `.agents/skills/`.
- Every installed `SKILL.md` was byte-identical to its source file.
- All 17 files bundled with `llm-wiki-builder`, including references, assets, scripts, tests, and fixtures, were installed byte-identically for both agents.
- Both installations ran under a newly created `/tmp` root. They did not write to this repository or any global agent skill directory.

## llm-wiki-builder bundle verification

Run the bundled tests with explicit dependencies on the minimum supported series and a newer maintained series:

```sh
uv run --with pytest --with pyyaml --python 3.11 python -m pytest -q -p no:cacheprovider skills/documentation/llm-wiki-builder/tests
uv run --with pytest --with pyyaml --python 3.14 python -m pytest -q -p no:cacheprovider skills/documentation/llm-wiki-builder/tests
```

- All 70 tests passed on both Python 3.11.17 and Python 3.14.9.
- All 19 local Markdown links and section anchors resolved.
- The skill passed the skill-creator frontmatter and structure validator.
- Distributed instructions, templates, comments, and examples are maintained in English. The generated wiki and maintenance skill follow explicit user language instructions, then target repository conventions; unclear choices are confirmed during design.
- A regression test verifies Japanese prose, titles, aliases, and schema-defined headings without imposing English on target content. Unicode escapes keep test source examples in English.
- The bundle is now maintained independently of the original user-level skill: its documentation was translated and simplified, and review findings were fixed with regression tests. Schema structure and values now produce schema errors instead of uncaught exceptions; malformed source records fail audit; invalid page types do not crash; superseded pages require successors.
- The test loader registers the dynamically loaded module in `sys.modules` before execution so Python 3.11 can resolve dataclass annotations.
- Reviewed instructions preserve source evidence and human verification requirements, keep generated references self-contained, and distinguish authorized propagation to human-facing documents from autonomous wiki updates.
- These checks cover script behavior and packaging. Agent interpretation of language instructions was reviewed statically, not tested through a live installation task.
