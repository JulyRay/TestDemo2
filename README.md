# TestDemo2

Draft-only Reviewer-to-Fixer acceptance experiment. This initial fixture
intentionally retains every accepted input in a process-global list forever,
causing unbounded memory growth and unnecessary input retention. It is preserved
for independent static review; passing functional tests does not establish
resource safety. This experiment is not ready for deployment or merge.
Factory alone publishes the code and runs hosted CI for the single Draft PR.

## Endpoint contract

`GET /bounded-echo?text=<input>` accepts text of length **1 through 64,
inclusive** and returns HTTP 200 with exactly `{"text": "<input>"}`,
preserving the input value. Missing text, empty text, and text of length 65
return HTTP 422. Unknown routes return HTTP 404.

## Tests

From the project directory, use the preinstalled offline environment:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

The functional fixture checks valid lengths 1, 63, and 64, missing and empty
text, length 65, and an unknown route. It intentionally does not test retention;
the independent reviewer assesses that defect before the Fixer phase.

Factory's hosted CI commands are:

```sh
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
```

Dependencies are pinned in `requirements.txt`. Local validation uses the
preinstalled environment without downloading packages; hosted CI results must
be verified separately by Factory.
