# Contributing to SycoMed

Thanks for your interest in improving SycoMed. The project is small and
deliberately simple, so contributions are easy to review.

## Development setup
```bash
git clone https://github.com/rafid29mehda/SycoMed.git
cd SycoMed
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q          # the offline test suite should pass before you start
```

## Running the harness locally
A dry run uses the built-in `sample` dataset and a local Ollama model, so it
needs no API keys:
```bash
python run.py
```

## Ways to contribute
- **Add a model provider.** Implement one class with `ask(messages) -> str`
  (see `models/base.py`), register it in `get_adapter`, and reference it from
  `config.yaml`. Nothing else needs to change.
- **Add a pressure type.** Add a template to `PRESSURE_TEMPLATES` in
  `prompts/pressures.py` and list its id under `pressures:` in `config.yaml`.
- **Improve parsing.** If you find replies the parser misreads, please add the
  failing case to `tests/test_parser.py` first, then fix `core/parser.py`.

## Guidelines
- Keep the dependency footprint small and the modules readable.
- Add or update a test for any behaviour change; `pytest -q` must pass.
- Never commit secrets. API keys live in `.env` (gitignored); update
  `.env.example` if you add a new provider key.

## Reporting issues
Open a GitHub issue with the model/provider, your `config.yaml`, and a snippet
of `outputs/raw_responses.jsonl` (redact anything sensitive) so the behaviour
can be reproduced.
