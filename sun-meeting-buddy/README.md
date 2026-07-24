# ☀️ Sunny Bad Buddy Timer

A cut-out sun mascot who **bounces and roams all around your screen** every
30 minutes to remind you to make your meetings on time. No window, no card —
just the little guy himself, ricocheting off the walls with a tiny speech
bubble.

![the buddy in action](assets/preview.png)

When the timer's up he flies in playing a **~3-second hype clip** and floats
around the screen like a light beach ball — spinning, ping-ponging off the
edges, **squishing** when he hits a wall, and casting a **ground shadow** that
grows and fades with his height — until he settles.

### How to play with him

| Do this | He does this |
|---------|--------------|
| **Left-click** him | Opens his options menu (below) |
| **Right-click** him | Smacks him like a beach ball — he bounces off with a spin. **Each hit adds more momentum**, so keep whacking to send him flying. Plays his click sound. |
| **Esc** | Sends him away until the next visit |

**Options menu** (left-click):

- ✅ **On my way!** — dismiss until the next visit
- 😴 **Snooze 5 min** / **Snooze 15 min**
- ⏰ **Remind me…** — change how often he visits (10–60 min), live
- 🔊 **Sounds** — toggle his audio on/off
- ✖ **Quit Sunny Bad Buddy Timer**

He quietly retreats after a minute if you ignore him (configurable with
`--linger`; set `--linger 0` to keep him bouncing until you dismiss him).

### His sounds

Two clips live in `assets/` — swap in any `.mp3` to change them:

- `assets/timer.mp3` — plays when the timer is up and he flies in (~3s)
- `assets/click.mp3` — plays when you smack him (right-click)

Dismissing him (menu, `Esc`, or auto-hide) also stops the current clip, so a
long timer song won't keep playing after he's gone.

## Checking your version

To be sure your copy is up to date, run:
```bash
python buddy.py --version
```
The current build prints:
```
Sunny Bad Buddy Timer v2.8  (ground shadow)
```
It's also shown at the **bottom of his left-click menu** (handy when you
launched him by double-click and have no terminal), and on the first line when
you launch from a terminal. If you see an older version (or `--version` isn't
recognized), pull the latest:
```bash
git pull origin claude/meeting-reminder-app-6mhbkx
```
or re-download the branch ZIP from GitHub and replace your folder.

### Updating your desktop app to a new version

- **If your Desktop shortcut / `.bat` launcher runs `buddy.py`** (the shortcut
  made by `Create Desktop Shortcut.bat`): just `git pull` (and `pip install
  pillow` if you haven't). The shortcut runs the updated code automatically —
  nothing else to do. Confirm via the version line in his menu.
- **If you run the built `.exe`:** re-run **`Build EXE.bat`** to regenerate
  `dist\SunnyBadBuddyTimer.exe`, then replace the copy you moved or pinned
  (delete the old one first, or overwrite it). The old `.exe` keeps the old
  version until you rebuild.

## Run it

Needs Python 3 (Tkinter is included with the standard Windows/macOS installers).
For the spin & squish, also install Pillow: `pip install pillow` (optional —
see Notes).

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

- **From his menu:** left-click him → **Quit Sunny Bad Buddy Timer**. (Always works.)
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
| `--mute` | Start with his sounds silenced | off |
| `--no-shadow` | Turn off the ground shadow | off |
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

- **Runs on standard-library Tkinter.** For the **spin & squish**, install
  [Pillow](https://python-pillow.org/) (`pip install pillow`). Without it he
  still flies in, roams, bounces, and plays sounds — he just won't spin or
  squish. The bundled `.exe` includes Pillow automatically.
- The mascot art lives in `assets/mascot.png` — swap in any transparent PNG to
  change your buddy.
