# ☀️ Sunny Bad Buddy Timer

A cut-out sun mascot who **bounces and roams all around your screen** every
30 minutes to remind you to make your meetings on time. No window, no card —
just the little guy himself, ricocheting off the walls with a tiny speech
bubble.

![the buddy in action](assets/preview.png)

When the timer's up he flies in playing a **~5-second hype clip** and floats
around the screen like a light beach ball — spinning, ping-ponging off the
edges, **squishing** when he hits a wall, and casting a **ground shadow** that
grows and fades with his height — until he settles. A **live clock** (HH:MM in
golden yellow) is pinned to the center of his sun orb — it rides along and
stays upright as he spins.

### How to play with him

| Do this | He does this |
|---------|--------------|
| **Left-click** him | Whacks him like a beach ball — he bounces off with a spin. **Each hit adds more momentum**, so keep whacking to send him flying. Plays his clip. |
| **Right-click** him | Opens his options menu (below) |
| **Esc** | Sends him away until the next visit |

He also gives a **boing** each time he bounces off a wall or corner — each
successive boing is half as loud as the last (resetting when you click him), so
the rapid settling bounces fade out instead of spamming.

**Options menu** (right-click):

- ✅ **On my way!** — dismiss until the next visit
- ⏰ **Set an alarm…** — pops up at a specific time (e.g. `2:30 pm`)
- 🔔 **Set a reminder…** — pops up in *N* minutes with an optional note
- 🔁 **Remind me…** — recurring, either **on the clock** (`:00 / :15 / :30`, top
  of the hour…) or **every N min from now**
- ⏱ **Alert me … before an alarm** — add 1 / 5 / 10 / 15-min heads-up pings
  before each alarm you set
- 😴 **Snooze 5 / 15 min**
- 🔊 **Sounds** — turn the arrival clip, click clip, and bounce boing on/off
  individually
- ✖ **Quit Sunny Bad Buddy Timer**

He quietly retreats after a minute if you ignore him (configurable with
`--linger`; set `--linger 0` to keep him bouncing until you dismiss him).

### Tray icon

If [`pystray`](https://pypi.org/project/pystray/) is installed (`pip install
pystray`), Sunny also tucks a **system-tray icon** into your notification area,
so he's always reachable even while hidden — **left-click it to show him now**,
or right-click for set-alarm / set-reminder / quit. It's skipped silently if
pystray isn't installed; the bundled `.exe` includes it.

### His sounds

Sound files live in `assets/` — swap in your own to change them:

- `assets/timer.mp3` — the long hype clip (~5s); plays when the timer is up
- `assets/click.mp3` — the short clip; plays the instant you click him
- `assets/bounce.wav` — the beach-ball boing on wall/corner hits

**Clicking him (left-click)** plays the short clip immediately, then rolls into
the long clip right after — short then long. Each sound has its own on/off
switch under **Sounds** in the menu.

Dismissing him (menu, `Esc`, or auto-hide) also stops the current clip, so a
long timer song won't keep playing after he's gone.

## Checking your version

To be sure your copy is up to date, run:
```bash
python buddy.py --version
```
The current build prints:
```
Sunny Bad Buddy Timer v2.14  (bounce fade + tray click)
```
It's also shown at the **bottom of his right-click menu** (handy when you
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
right away (no console window) and keeps going every 30 minutes. Stop him by
right-clicking him → **Quit Sunny Bad Buddy Timer**.

Want him on your Desktop? **Double-click `Create Desktop Shortcut.bat`** and it
drops a *Sunny Bad Buddy Timer* shortcut (with his face as the icon) on your
Desktop. To launch him automatically at login, press `Win+R`, type
`shell:startup`, and drag that shortcut into the folder that opens.

### Stopping him

- **From his menu:** right-click him → **Quit Sunny Bad Buddy Timer**. (Always works.)
- **From the tray icon:** right-click the tray icon → **Quit** (if pystray is installed).
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

- **Runs on standard-library Tkinter.** Two optional extras: **Pillow** for the
  spin & squish (and shadow), and **pystray** for the tray icon —
  `pip install pillow pystray`. Without them he still flies in, roams, bounces,
  and plays sounds. The bundled `.exe` includes both automatically.
- The mascot art lives in `assets/mascot.png` — swap in any transparent PNG to
  change your buddy.
