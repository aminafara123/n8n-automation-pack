# Renders docs/demo.gif with charmbracelet/vhs (needs vhs, ttyd and ffmpeg on PATH).
# Run from the repo root, with the deps installed in .venv:  vhs docs/demo.tape
# Follows the DEMO.md terminal fallback (no live n8n): validate the pack, then show the workflow structure and LLM node.
Output docs/demo.gif

Set Shell "bash"
Set FontSize 18
Set Width 1200
Set Height 700
Set Padding 24
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set TypingSpeed 40ms

Hide
Type "VIRTUAL_ENV_DISABLE_PROMPT=1 source .venv/bin/activate"
Enter
Wait@120s
Type "clear"
Enter
Wait@120s
Show
Sleep 500ms

Type "ls workflows/"
Sleep 400ms
Enter
Wait@120s
Sleep 2s

Type "make validate"
Sleep 400ms
Enter
Wait@120s
Sleep 3s

Hide
Type "clear"
Enter
Sleep 200ms
Show
Type `grep '"type": "n8n-nodes' workflows/2-email-triage.json`
Sleep 400ms
Enter
Wait@120s
Sleep 3s

Type `grep -o '"url": "[^"]*' workflows/2-email-triage.json`
Sleep 400ms
Enter
Wait@120s
Sleep 3.5s

Type "make test"
Sleep 400ms
Enter
Wait@120s
Sleep 2s

Sleep 1s
