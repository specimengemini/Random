# ☀️ Sun Meeting Buddy

A cheerful desktop mascot who slides into the corner of your screen **every
30 minutes** to nudge you toward your next meeting — so you're never the one
joining late.

![the buddy in action](assets/preview.png)

He shows up bottom-right, throws you a hype line, tells you the time, and gives
you two choices: **On my way! ✅** or **Snooze 5m 😴**. Drag him around, or hit
`Esc` to dismiss.

## Run it

You need Python 3 (which ships with Tkinter on Windows and macOS). No other
libraries required.

**macOS / Linux**
```bash
./run.sh
```

**Windows**
```bat
run.bat
```

or directly, anywhere:
```bash
python3 buddy.py
```

Leave the terminal window open — that's what keeps him running. Press
`Ctrl+C` there to stop.

## Options

| Flag | What it does | Default |
|------|--------------|---------|
| `--every MIN` | Minutes between pop-ups | `30` |
| `--snooze MIN` | Minutes the snooze button adds | `5` |
| `--now` | Also pop up immediately on launch (nice for a test) | off |

Examples:
```bash
python3 buddy.py --now              # see him right away
python3 buddy.py --every 15         # remind me every 15 minutes
python3 buddy.py --every 25 --snooze 3
```

## Want him to start automatically at login?

- **macOS:** System Settings → General → Login Items → **+** → pick `run.sh`
  (or add a `launchd` plist).
- **Windows:** press `Win+R`, type `shell:startup`, and drop a shortcut to
  `run.bat` in that folder.
- **Linux:** add `run.sh` to your desktop environment's *Startup Applications*.

## Notes

- **Zero dependencies.** Pure standard-library Tkinter. If you happen to have
  [Pillow](https://python-pillow.org/) installed, he'll use it for marginally
  smoother image scaling — but it's completely optional.
- The mascot art lives in `assets/mascot.png` — swap in any transparent PNG to
  change your buddy.
