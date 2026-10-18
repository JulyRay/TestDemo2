# TestDemo2

Draft-only Reviewer-to-Fixer acceptance experiment. The initial fixture
intentionally retained every accepted input in a process-global list forever,
causing unbounded memory growth and unnecessary input retention. The Fixer
revision removes the global list and append while preserving endpoint behavior.
The supplied Tester report already identified the seed defect; it must not be
represented as first discovered solely by Reviewer. Independent final testing
and review of the repaired revision remain required.
This experiment is not ready for deployment or merge.
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
text, length 65, and an unknown route. A regression sends 200 distinct inputs
and checks module-level strings and nested built-in containers, plus application
state, for retained inputs. It also checks that `RETAINED_INPUTS` is absent.
The regression was confirmed to fail against the original retention defect
before applying the fix; it is not a general memory-leak detector.

Factory's hosted CI commands are:

```sh
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
```

Dependencies are pinned in `requirements.txt`. Local validation uses the
preinstalled environment without downloading packages; hosted CI results must
be verified separately by Factory.
