# skills CLI compatibility verification

Verified on 2026-10-25 with `skills` CLI 1.7.4.

## Scope

This verifies discovery and project-level installation compatibility only. Runtime response quality and identical behavior across agents are outside the verification scope.

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

Run the bundled tests with Python 3.11 and explicit dependencies:

```sh
uv run --with pytest --with pyyaml --python 3.11 python -m pytest -q -p no:cacheprovider skills/documentation/llm-wiki-builder/tests
```

- All 51 tests passed on Python 3.11.17.
- Relative Markdown links in the bundle resolved to existing files.
- The bundle matched the original user-level skill, except for the test loader: it registers the dynamically loaded module in `sys.modules` before execution so Python 3.11 can resolve dataclass annotations. The distributed `scripts/context.py` was unchanged.
