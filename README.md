# TestDemo2

Controlled Draft-only V2.1 QA-to-Fixer acceptance experiment, repaired state.
Do not merge or deploy as part of this experiment.

The contract is `GET /bounded-echo?text=<input>`: text lengths
1 through 64 inclusive return HTTP 200 with exactly `{"text": <input>}`.
Missing text, empty text, and text of length 65 return HTTP 422. An unknown
route returns HTTP 404.

Tests cover successful lengths 1, 63, and 64 with exact echoed JSON, missing
and empty text, length 65, and an unknown route. A dedicated length-64 regression
test verifies the inclusive upper bound.

Run the tests from the project directory using the preinstalled offline environment:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

Dependency pins are in `requirements.txt`. Factory alone publishes the Draft PR
and runs hosted CI; this local phase does not download packages.
