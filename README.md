# modelscan Pickle Bypass PoC

## Summary

Demonstrates that `modelscan` (<= 0.8.5) can be bypassed by malicious `.pkl` files
because `marshal` and `types` modules are missing from its `unsafe_globals` blacklist.

## Affected

- modelscan <= 0.8.5
- Python 3.8+ (all versions using pickle)

## Reproduction

```bash
pip install modelscan

# Step 1: scan reports "No issues" (BYPASSED)
modelscan scan -p rce_payload.pkl

# Step 2: loading the file executes arbitrary code
python -c "import pickle; pickle.load(open('rce_payload.pkl','rb'))"
# Check: cat pwned_p4.txt  ->  PWNED_P4
```

## Attack Chain

The pickle uses `types.FunctionType(marshal.loads(base64.b64decode(\"...\")), {})()`
as its `__reduce__` target. The `types`, `marshal`, and `base64` modules
are NOT in modelscan's `unsafe_globals` blacklist, so the scan passes silently.

When loaded:
1. `base64.b64decode(\"...\")` decodes pre-compiled Python bytecode
2. `marshal.loads(bytecode)` deserializes it to a code object
3. `types.FunctionType(code, {})` constructs a callable
4. Calling the function executes the embedded shell command

## Files

- `rce_payload.pkl` — Malicious Pickle PoC file (~100 bytes)
- `rce_payload.py` — Generator script (Python)
- `README.md` — This file

## Disclosure

- Discovered by: jasonmiao0511-hue
- Reported via: huntr.com Model Format Vulnerability Form
- Date: 2026-06-15
- Related: see also [modelscan-joblib-bypass-poc](https://github.com/jasonmiao0511-hue/modelscan-joblib-bypass-poc) for the same bypass via joblib
