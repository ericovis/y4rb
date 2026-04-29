This is a simple resumé builder that uses HTML, CSS and YAML to generate resumés. HTML and CSS will define the overall look while YAML will define the data.


## Tools

This repo uses `uv` for package and project management. Always use `uv run` to execute any tool or script — never call `python`, `ruff`, `ty`, `pytest`, or other project tools directly.

Examples:
- Run the app: `uv run python main.py`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run ty check`
- Tests: `uv run pytest`


## Code Verification Loop

Before considering any task complete, run in order:
1. `uv run ruff check .` — must pass with no errors
2. `uv run ty check` — must pass with no errors
3. `uv run pytest` — all tests must pass
