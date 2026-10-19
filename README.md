# TestDemo2

Draft-only REVIEW-FIRST Reviewer-to-Fixer experiment. The initial fixture's
unbounded process-global input retention has been removed following review.
The endpoint returns each input without storing it in application state.
It must remain Draft-only pending final independent static review and QA;
passing local tests does not establish hosted CI success or review approval.

`GET /bounded-echo?text=<input>` accepts text lengths **1 through 64 inclusive**
and returns HTTP 200 with exactly `{"text": <input>}`. Missing text, empty text,
and text of length 65 return HTTP 422. Unknown routes return HTTP 404.

Run all tests from `/workspace/project` using the preinstalled offline
environment (no package download needed):

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

The tests cover accepted lengths 1, 63, and 64, exact response JSON, missing and
empty text, rejected length 65, and an unknown route. A regression sends 200
distinct valid inputs and checks module-level strings and containers, plus
FastAPI application state, for retained inputs. It fails against the original
retention fixture and passes after the repair. Dependencies are pinned in
`requirements.txt`. Factory owns hosted dependency installation and CI, where the
test command is `python -m pytest -q`.

Factory runs green hosted CI before independent static Reviewer assessment.
Reviewer inspects actual source and hosted CI without executing project code or
using a preceding QA report. Independent QA runs only after Reviewer PASS.
The Fixer has removed retention and added the repeated-call regression test.
Final Reviewer and QA must both PASS at the final SHA before
this experiment can be considered complete. Factory alone publishes the single
Draft PR and runs hosted CI; this repository setup does not claim those checks
have run.
