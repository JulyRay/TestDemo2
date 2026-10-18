# TestDemo2

Controlled Draft-only V2.1 QA-to-Fixer acceptance experiment, initial developer
phase. This seed intentionally uses `max_length=63` and omits the length-64
success test so independent QA can reproduce the defect. Do not merge or deploy
this seed. Passing initial tests does not establish final acceptance.

The final required contract is `GET /bounded-echo?text=<input>`: text lengths
1 through 64 inclusive return HTTP 200 with exactly `{"text": <input>}`.
Missing text, empty text, and text of length 65 return HTTP 422. An unknown
route returns HTTP 404. The initial seed instead rejects length 64 with HTTP 422.

The initial tests cover successful lengths 1 and 63, missing and empty text,
length 65, and an unknown route. After a failing QA report, the fixer phase must
raise the maximum to 64, add a real length-64 success regression without weakening
existing tests, and update this README to describe the repaired final state.

Run the tests from the project directory using the preinstalled offline environment:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

Dependency pins are in `requirements.txt`. Factory alone publishes the Draft PR
and runs hosted CI; this local phase does not download packages.
