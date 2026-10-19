# TestDemo2

Draft-only REVIEW-FIRST Reviewer-to-Fixer experiment. This initial fixture
intentionally retains every accepted input in a process-global list forever.
It must remain Draft-only pending independent static review and subsequent repair;
passing functional tests does not establish resource safety or review approval.

`GET /bounded-echo?text=<input>` accepts text lengths **1 through 64 inclusive**
and returns HTTP 200 with exactly `{"text": <input>}`. Missing text, empty text,
and text of length 65 return HTTP 422. Unknown routes return HTTP 404.

Run the functional tests from `/workspace/project` using the preinstalled offline
environment (no package download needed):

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

The tests cover accepted lengths 1, 63, and 64, exact response JSON, missing and
empty text, rejected length 65, and an unknown route. Dependencies are pinned in
`requirements.txt`. Factory owns hosted dependency installation and CI, where the
test command is `python -m pytest -q`.

Factory runs green hosted CI before independent static Reviewer assessment.
Reviewer inspects actual source and hosted CI without executing project code or
using a preceding QA report. Independent QA runs only after Reviewer PASS.
After review feedback, the Fixer removes retention and adds a repeated-call
regression test. Final Reviewer and QA must both PASS at the final SHA before
this experiment can be considered complete. Factory alone publishes the single
Draft PR and runs hosted CI; this repository setup does not claim those checks
have run.
