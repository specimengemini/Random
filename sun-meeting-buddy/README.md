# ☀️ Sunny Bad Buddy Timer

A cut-out sun mascot who **bounces up from the bottom of your screen** every
30 minutes to remind you to make your meetings on time. No window, no card —
just the little guy himself, with a tiny speech bubble.

![the buddy in action](assets/preview.png)

**Click him** to open his menu:

- ✅ **On my way!** — dismiss until the next visit
- 😴 **Snooze 5 min** / **Snooze 15 min**
- ⏰ **Remind me…** — change how often he visits (10–60 min), live
- ✖ **Quit Sunny Bad Buddy Timer**

He bounces in with a **soft ding** to grab your attention, does a gentle idle
bob, and quietly retreats after a minute if you ignore him (configurable).
Press `Esc` to dismiss him too. The menu also has a **🔔 Ding on arrival**
toggle if you want him silent.

## Checking your version

To be sure your copy is up to date, run:
```bash
python buddy.py --version
```
The current build prints:
```
Sunny Bad Buddy Timer v2.4  (standalone .exe)
```
The version also prints in the first line when you launch it. If you see an
older version (or `--version` isn't recognized), pull the latest:
```bash
git pull origin claude/meeting-reminder-app-6mhbkx
```
or re-download the branch ZIP from GitHub and replace your folder.

## Run it

Needs Python 3 (Tkinter is included with the standard Windows/macOS installers).
No other libraries required.

**Windows**
```bat
run.bat --now
```

**macOS / Linux**
```bash
./run.sh --now
```

or directly:
```bash
python buddy.py --now
```

### Make a standalone .exe (no Python folder needed)

Want a single app file you can double-click, move anywhere, or share — with no
visible Python? **Double-click `Build EXE.bat`** once. It installs the build
tool and produces:

```
dist\SunnyBadBuddyTimer.exe
```

Double-click that `.exe` to run Sunny (he shows up right away, then every 30
minutes). You can move it to your Desktop, or right-click → **Pin to Taskbar**.
Building needs Python installed *once* to do the build; running the finished
`.exe` does not.

### Easiest: double-click, no typing

On Windows, just **double-click `Sunny Bad Buddy Timer.bat`** — Sunny bounces up
right away (no console window) and keeps going every 30 minutes. Stop him from
his click-menu → **Quit Sunny Bad Buddy Timer**.

Want him on your Desktop? **Double-click `Create Desktop Shortcut.bat`** and it
drops a *Sunny Bad Buddy Timer* shortcut (with his face as the icon) on your
Desktop. To launch him automatically at login, press `Win+R`, type
`shell:startup`, and drag that shortcut into the folder that opens.

### Stopping him

- **From his menu:** click him → **Quit Sunny Bad Buddy Timer**. (Always works.)
- **From a terminal:** if you launched with `python buddy.py`, press **Ctrl+C**.
- **Double-click `Stop Sunny.bat`:** handy when you started him by double-click
  (no terminal to Ctrl+C in). It only stops Sunny, not other Python programs.

## Options

| Flag | What it does | Default |
|------|--------------|---------|
| `--every MIN` | Minutes between visits | `30` |
| `--snooze MIN` | Minutes the main snooze adds | `5` |
| `--linger SEC` | Seconds before he auto-hides; `0` = stay until clicked | `60` |
| `--size PX` | Mascot height in pixels | `380` |
| `--mute` | Start with the ding silenced | off |
| `--now` | Also bounce up immediately on launch | off |
| `--version` | Print the version and exit | — |

Examples:
```bash
python buddy.py --now                 # see him right away
python buddy.py --every 15            # visit every 15 minutes
python buddy.py --linger 0           # stay put until I click him
python buddy.py --size 240           # make him smaller than the default 380
```

## A note on transparency

The clean, no-background cut-out uses a color-key transparency trick that works
great on **Windows** (he's also click-through — clicking empty space around him
goes to whatever's behind). On **macOS/Linux**, where that isn't supported, he
falls back to a small soft card so the app still works everywhere.

## Start him automatically at login

- **Windows:** press `Win+R`, type `shell:startup`, and drop a shortcut to
  `run.bat` in that folder.
- **macOS:** System Settings → General → Login Items → **+** → pick `run.sh`.
- **Linux:** add `run.sh` to your desktop's *Startup Applications*.

## Notes

- **Zero dependencies.** Pure standard-library Tkinter. If you happen to have
  [Pillow](https://python-pillow.org/) installed, the cut-out edges are a touch
  cleaner — but it's entirely optional.
- The mascot art lives in `assets/mascot.png` — swap in any transparent PNG to
  change your buddy.
