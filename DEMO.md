# 60-second demo script

Goal: show that these are real, valid n8n workflows that import cleanly and run on a local LLM. Record at 1080p, no audio needed (captions optional).

## 0:00 - 0:10  The pitch (terminal)
Show the repo tree, then run the gate:

```bash
make install
make validate
```

Point at the `5/5 workflows valid` line. Say: "Five importable n8n workflows, each checked to be a legal export before it touches the GUI."

## 0:10 - 0:30  Import into n8n (browser)
In n8n: Workflows > top-right menu > **Import from File** > pick `workflows/2-email-triage.json`. The canvas fills in: Gmail Trigger -> Classify + Draft (LLM) -> Parse LLM JSON -> Add Label -> Create Draft Reply. Hover the sticky note so the viewer reads what it does.

## 0:30 - 0:45  Show the LLM node
Open **Classify + Draft (LLM)**. Show the URL `{{ $env.LLM_BASE_URL || 'http://127.0.0.1:11434/v1' }}/chat/completions` and the JSON body. Say: "The AI step is a plain HTTP call to a local model by default. Swap two env vars to use any provider."

## 0:45 - 0:60  Run it once
With Ollama running locally and a Gmail credential attached, use **Test workflow** (or pin a sample Gmail item) so the draft is created. Open the resulting Gmail draft and point at the "-- AI-generated draft. Review before sending. --" footer. Close with: "AI drafts, a human sends. Import, add credentials, activate."

## Fallback if no live n8n instance
Record only the terminal segment (0:00 - 0:10) plus a scroll through `workflows/1-lead-intake.json` showing the node and connection structure. The validator output alone proves the files are real.
