#!/usr/bin/env python3
"""
Sunny Bad Buddy Timer
=================
A cut-out sun mascot who bounces up from the bottom of your screen on a
timer (every 30 minutes by default) to remind you to make your meetings on
time. No card, no window chrome -- just the little guy himself. **Click him**
to open a menu: On my way, Snooze, change the interval, or quit.

Pure standard-library Tkinter. Pillow is optional (it just makes the cut-out
edges a touch cleaner). Transparency is best on Windows; on macOS/Linux it
falls back to a small floating card so it still works.

Usage:
    python buddy.py                 # bounce up every 30 minutes
    python buddy.py --now           # ...and once right now (great for testing)
    python buddy.py --every 15      # every 15 minutes
    python buddy.py --linger 0      # stay until clicked (default: auto-hide 60s)
"""

import argparse
import math
import os
import random
import shutil
import subprocess
import sys
import tkinter as tk
from datetime import datetime

__version__ = "2.5  (roaming bounce + sounds)"

# When bundled by PyInstaller, data files live in a temp dir (sys._MEIPASS);
# otherwise they sit next to this script.
if getattr(sys, "frozen", False):
    HERE = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    HERE = os.path.dirname(os.path.abspath(__file__))
MASCOT_PATH = os.path.join(HERE, "assets", "mascot.png")
CLICK_SOUND = os.path.join(HERE, "assets", "click.mp3")   # left-click / smack
TIMER_SOUND = os.path.join(HERE, "assets", "timer.mp3")   # on arrival (timer up)

KEY = "#FF00FF"          # magenta color-key -> becomes transparent + click-through
KEY_RGB = (255, 0, 255)
BUBBLE_BG = "#FFFFFF"
BUBBLE_EDGE = "#F5A623"
BUBBLE_INK = "#4A3B10"

HYPE_LINES = [
    "Meeting soon!\nLet's be on time ☀️",
    "Two minutes early\nis right on time!",
    "Wrap it up —\nmeeting's near!",
    "Save the tab,\njoin the call!",
    "Be first on\nthe call. Iconic.",
    "Stand up, shine,\nmeeting time!",
    "Psst — your\nmeeting misses you.",
    "Big sun energy:\nnever late ☀️",
]


class SunBuddy:
    def __init__(self, every_min, snooze_min, linger_s, show_now, mascot_h, muted=False):
        self.interval_ms = int(every_min * 60_000)
        self.every_min = every_min
        self.snooze_min = snooze_min
        self.linger_ms = int(linger_s * 1000)
        self.mascot_h = mascot_h
        self.muted = muted

        self.root = tk.Tk()
        self.root.withdraw()
        self._enable_dpi_awareness()

        self.win = None            # the mascot Toplevel
        self.canvas = None
        self.photo = None
        self.transparent_ok = False
        self.win_w = self.win_h = 0
        self.mascot_bottom_pad = 0

        self._tick_job = None
        self._anim_job = None
        self._linger_job = None
        self._menu_open = False

        # 2-D bounce physics: window top-left position + velocity (px, px/s)
        self.px = self.py = 0.0
        self.vx = self.vy = 0.0
        self.bounds = (0, 0, 0, 0)   # left, top, right, bottom of the play area
        self.state = "rest"          # "roam" | "rest"

        self._build_window()

        first = 300 if show_now else self.interval_ms
        self._schedule(first)
        self._log_next(first)

    # -- platform helpers ----------------------------------------------------
    def _enable_dpi_awareness(self):
        if sys.platform.startswith("win"):
            try:
                import ctypes
                try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(1)
                except Exception:
                    ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

    def _play_sound(self, path, alias):
        """Play an mp3/wav clip, non-blocking, best-effort per platform."""
        if self.muted or not os.path.exists(path):
            return
        try:
            if sys.platform.startswith("win"):
                # MCI plays mp3 (winsound is wav-only). Reopen each time so the
                # clip restarts from the top on every trigger.
                import ctypes
                mci = ctypes.windll.winmm.mciSendStringW
                mci(f"close {alias}", None, 0, None)
                mci(f'open "{path}" alias {alias}', None, 0, None)
                mci(f"play {alias} from 0", None, 0, None)
            elif sys.platform == "darwin":
                subprocess.Popen(["afplay", path],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                for pl in ("ffplay", "mpg123", "cvlc", "paplay"):
                    exe = shutil.which(pl)
                    if not exe:
                        continue
                    if pl == "ffplay":
                        cmd = [exe, "-nodisp", "-autoexit", "-loglevel", "quiet", path]
                    elif pl == "cvlc":
                        cmd = [exe, "--play-and-exit", "--intf", "dummy", path]
                    else:
                        cmd = [exe, path]
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break
        except Exception:
            pass

    def _work_area(self):
        """(left, top, right, bottom) of usable screen, excluding the taskbar."""
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        if sys.platform.startswith("win"):
            try:
                import ctypes
                from ctypes import wintypes
                r = wintypes.RECT()
                # SPI_GETWORKAREA = 0x0030
                ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(r), 0)
                if r.right > r.left and r.bottom > r.top:
                    return r.left, r.top, r.right, r.bottom
            except Exception:
                pass
            return 0, 0, sw, sh - 48  # assume a ~48px taskbar
        return 0, 0, sw, sh - 4

    # -- image ---------------------------------------------------------------
    def _load_photo(self):
        target_h = self.mascot_h
        try:
            from PIL import Image, ImageFilter, ImageTk
            img = Image.open(MASCOT_PATH).convert("RGBA")
            w = round(img.width * target_h / img.height)
            img = img.resize((w, target_h), Image.LANCZOS)
            a = img.split()[3].point(lambda p: 255 if p >= 128 else 0)
            a = a.filter(ImageFilter.MinFilter(3))  # erode 1px -> no halo
            img.putalpha(a)
            if self.transparent_ok:
                # bake transparent areas to the color-key so Windows hides them
                base = Image.new("RGBA", img.size, KEY_RGB + (255,))
                base.alpha_composite(img)
                self.photo = ImageTk.PhotoImage(base.convert("RGB"))
            else:
                # keep alpha so it blends onto the fallback card
                self.photo = ImageTk.PhotoImage(img)
        except Exception:
            img = tk.PhotoImage(file=MASCOT_PATH)
            factor = max(1, round(img.height() / target_h))
            if factor > 1:
                img = img.subsample(factor, factor)
            self.photo = img
        return self.photo.width(), self.photo.height()

    # -- window construction -------------------------------------------------
    def _build_window(self):
        w = tk.Toplevel(self.root)
        self.win = w
        w.withdraw()
        w.overrideredirect(True)
        w.attributes("-topmost", True)

        # Try real color-key transparency (clean cut-out on Windows).
        try:
            w.attributes("-transparentcolor", KEY)
            w.configure(bg=KEY)
            self.transparent_ok = True
            canvas_bg = KEY
        except tk.TclError:
            # No color-key here -> soft card fallback so it still runs.
            self.transparent_ok = False
            canvas_bg = "#FFF6D8"
            w.configure(bg=BUBBLE_EDGE)

        mw, mh = self._load_photo()
        bubble_h = 52
        gap = 8
        pad = 6 if self.transparent_ok else 3
        self.win_w = mw + pad * 2
        self.win_h = bubble_h + gap + mh + pad * 2
        self.mascot_bottom_pad = pad

        c = tk.Canvas(w, width=self.win_w, height=self.win_h,
                      bg=canvas_bg, highlightthickness=0, bd=0)
        c.pack()
        self.canvas = c

        cx = self.win_w // 2
        # speech bubble
        self._draw_bubble(c, cx, pad, self.win_w - pad * 2, bubble_h)
        self.bubble_text = c.create_text(
            cx, pad + bubble_h // 2 - 2, text="", width=self.win_w - pad * 4,
            font=("Helvetica", 10, "bold"), fill=BUBBLE_INK, justify="center")
        # mascot
        self.mascot_img = c.create_image(
            cx, pad + bubble_h + gap + mh // 2, image=self.photo)

        c.configure(cursor="hand2")
        c.bind("<Button-1>", self._on_click)           # left: sound + little pop
        c.bind("<Double-Button-1>", self._open_menu)   # double: options menu
        c.bind("<Button-3>", self._smack)              # right: beach-ball smack
        w.bind("<Escape>", lambda _e: self._dismiss())

        self._build_menu()

    def _draw_bubble(self, c, cx, top, width, height):
        x0 = cx - width // 2
        y0 = top
        x1 = cx + width // 2
        y1 = top + height
        r = 14
        fill = BUBBLE_BG if self.transparent_ok else BUBBLE_BG
        # rounded rectangle via a smoothed polygon
        pts = [x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r, x1, y1 - r,
               x1, y1, x1 - r, y1, x0 + r, y1, x0, y1, x0, y1 - r,
               x0, y0 + r, x0, y0]
        c.create_polygon(pts, smooth=True, fill=fill,
                         outline=BUBBLE_EDGE, width=2)
        # little tail pointing down toward the mascot
        c.create_polygon(cx - 9, y1 - 1, cx + 9, y1 - 1, cx, y1 + 11,
                         fill=fill, outline=fill)

    def _build_menu(self):
        m = tk.Menu(self.root, tearoff=0)
        m.add_command(label="✅  On my way!", command=self._dismiss)
        m.add_separator()
        m.add_command(label=f"\U0001F634  Snooze {int(self.snooze_min)} min",
                      command=lambda: self._snooze(self.snooze_min))
        m.add_command(label="\U0001F634  Snooze 15 min",
                      command=lambda: self._snooze(15))
        sub = tk.Menu(m, tearoff=0)
        for n in (10, 15, 20, 30, 45, 60):
            sub.add_radiobutton(
                label=f"every {n} min", value=n,
                command=lambda n=n: self._set_interval(n))
        m.add_cascade(label="⏰  Remind me…", menu=sub)
        self._sound_var = tk.BooleanVar(value=not self.muted)
        m.add_checkbutton(label="\U0001F50A  Sounds",
                          variable=self._sound_var, command=self._toggle_sound)
        m.add_separator()
        m.add_command(label="✖  Quit Sunny Bad Buddy Timer", command=self._quit)
        self.menu = m

    def _toggle_sound(self):
        self.muted = not self._sound_var.get()
        print(f"[sunny] sounds {'off' if self.muted else 'on'}", flush=True)

    # -- scheduling ----------------------------------------------------------
    def _schedule(self, delay_ms):
        if self._tick_job is not None:
            self.root.after_cancel(self._tick_job)
        self._tick_job = self.root.after(delay_ms, self._tick)

    def _log_next(self, delay_ms):
        mins = delay_ms / 60000
        print(f"[sunny] next visit in ~{mins:.0f} min", flush=True)

    def _tick(self):
        self._appear()
        self._schedule(self.interval_ms)
        self._log_next(self.interval_ms)

    def _set_interval(self, n):
        self.every_min = n
        self.interval_ms = int(n * 60_000)
        self._schedule(self.interval_ms)
        print(f"[sunny] interval set to {n} min", flush=True)

    # -- show / hide ---------------------------------------------------------
    def _appear(self):
        self.canvas.itemconfigure(self.bubble_text, text=random.choice(HYPE_LINES))
        left, top, right, bottom = self._work_area()
        self.bounds = (left, top, right, bottom)
        # start near the bottom-right corner, then fling across the screen
        self.px = float(right - self.win_w - 40)
        self.py = float(bottom - self.win_h)
        self.win.geometry(f"{self.win_w}x{self.win_h}+{int(self.px)}+{int(self.py)}")
        self.win.deiconify()
        self.win.lift()
        self.win.attributes("-topmost", True)
        self._play_sound(TIMER_SOUND, "sunnytimer")

        # launch up-and-to-the-left so he bounces around the whole screen
        self._launch(-440.0, -940.0)

        # auto-hide after lingering (unless disabled)
        if self._linger_job is not None:
            self.root.after_cancel(self._linger_job)
        if self.linger_ms > 0:
            self._linger_job = self.root.after(self.linger_ms, self._retreat_if_idle)

    # -- bounce physics ------------------------------------------------------
    G = 1500.0          # gravity (px/s^2)
    WALL_DAMP = 0.86    # energy kept when bouncing off a side wall / ceiling
    FLOOR_DAMP = 0.74   # energy kept when bouncing off the floor
    AIR_DRAG = 0.995    # gentle horizontal drag while airborne

    def _launch(self, vx, vy):
        """Give Sunny a velocity and (re)start the roam animation."""
        self.vx, self.vy = vx, vy
        self.state = "roam"
        if self._anim_job is None:
            self._animate()

    def _animate(self):
        dt = 0.016
        left, top, right, bottom = self.bounds
        max_x = right - self.win_w
        max_y = bottom - self.win_h

        if self.state == "roam":
            self.vy += self.G * dt
            self.vx *= self.AIR_DRAG
            self.px += self.vx * dt
            self.py += self.vy * dt

            if self.px <= left:
                self.px = float(left); self.vx = abs(self.vx) * self.WALL_DAMP
            elif self.px >= max_x:
                self.px = float(max_x); self.vx = -abs(self.vx) * self.WALL_DAMP
            if self.py <= top:
                self.py = float(top); self.vy = abs(self.vy) * self.WALL_DAMP

            if self.py >= max_y:                       # hit the floor
                self.py = float(max_y)
                self.vy = -abs(self.vy) * self.FLOOR_DAMP
                self.vx *= 0.9                         # rolling friction
                if abs(self.vy) < 70 and abs(self.vx) < 25:
                    self.vx = self.vy = 0.0            # settle down and rest
                    self.state = "rest"

            try:
                self.win.geometry(f"+{int(self.px)}+{int(self.py)}")
            except tk.TclError:
                self._anim_job = None
                return

        if self.state == "rest":
            self._anim_job = None                      # stop looping, save CPU
            return
        self._anim_job = self.root.after(16, self._animate)

    def _stop_anim(self):
        if self._anim_job is not None:
            self.root.after_cancel(self._anim_job)
            self._anim_job = None

    def _retreat_if_idle(self):
        if not self._menu_open:
            self._dismiss()

    def _dismiss(self):
        self._stop_anim()
        if self._linger_job is not None:
            self.root.after_cancel(self._linger_job)
            self._linger_job = None
        try:
            self.win.withdraw()
        except tk.TclError:
            pass

    # -- interaction ---------------------------------------------------------
    def _bump_linger(self):
        """Restart the auto-hide countdown whenever Sunny is interacted with."""
        if self._linger_job is not None:
            self.root.after_cancel(self._linger_job)
            self._linger_job = None
        if self.linger_ms > 0 and self.win.state() != "withdrawn":
            self._linger_job = self.root.after(self.linger_ms, self._retreat_if_idle)

    def _on_click(self, event):
        # left-click: play the clip and give him a little upward pop
        self._play_sound(CLICK_SOUND, "sunnyclick")
        self._bump_linger()
        self._launch(self.vx * 0.5 + random.uniform(-140, 140), -460.0)

    def _smack(self, event):
        # right-click: whack the beach ball with a strong random impulse,
        # pushed away from whichever side you hit
        self._play_sound(CLICK_SOUND, "sunnyclick")
        self._bump_linger()
        away = -1.0 if event.x > self.win_w / 2 else 1.0
        self._launch(away * random.uniform(420, 760), -random.uniform(680, 1020))

    def _open_menu(self, event):
        # extend linger while the user is interacting
        if self._linger_job is not None:
            self.root.after_cancel(self._linger_job)
            self._linger_job = None
        self._menu_open = True
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
            self._menu_open = False
            # if still visible and linger enabled, restart the countdown
            if self.linger_ms > 0 and self.win.state() != "withdrawn":
                self._linger_job = self.root.after(self.linger_ms, self._retreat_if_idle)

    def _snooze(self, minutes):
        self._dismiss()
        self._schedule(int(minutes * 60_000))
        print(f"[sunny] snoozed {int(minutes)} min", flush=True)

    def _quit(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    # -- run -----------------------------------------------------------------
    def _pulse(self):
        # Keep the Python interpreter ticking during Tk's event loop so an
        # incoming Ctrl+C (SIGINT) actually gets delivered instead of being
        # swallowed by the C-level loop.
        self.root.after(200, self._pulse)

    def _on_sigint(self, *_):
        print("\n[sunny] bye! stay punctual ☀️", flush=True)
        self._quit()

    def run(self):
        print(f"[sunny] Sunny Bad Buddy Timer v{__version__}", flush=True)
        print("[sunny] running ☀️  He'll bounce up on schedule.\n"
              "[sunny] click him for options, Esc, or Ctrl+C here to stop.",
              flush=True)
        try:
            import signal
            signal.signal(signal.SIGINT, self._on_sigint)
        except (ValueError, ImportError):
            pass  # not on the main thread / unsupported -> menu Quit still works
        self._pulse()
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_sigint()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="A cut-out sun mascot that bounces up to keep you punctual.")
    ap.add_argument("--version", action="version",
                    version=f"Sunny Bad Buddy Timer v{__version__}")
    ap.add_argument("--mute", action="store_true", help="silence the soft ding")
    ap.add_argument("--every", type=float, default=30, metavar="MIN",
                    help="minutes between visits (default: 30)")
    ap.add_argument("--snooze", type=float, default=5, metavar="MIN",
                    help="minutes the main snooze adds (default: 5)")
    ap.add_argument("--linger", type=float, default=60, metavar="SEC",
                    help="seconds to stay before auto-hiding; 0 = until clicked (default: 60)")
    ap.add_argument("--size", type=int, default=380, metavar="PX",
                    help="mascot height in pixels (default: 380)")
    ap.add_argument("--now", action="store_true",
                    help="also bounce up immediately on launch")
    args = ap.parse_args(argv)

    if not os.path.exists(MASCOT_PATH):
        sys.exit(f"[sunny] missing mascot image at {MASCOT_PATH}")

    # A double-clicked .exe passes no flags, so greet the user right away.
    show_now = args.now or getattr(sys, "frozen", False)

    SunBuddy(every_min=args.every, snooze_min=args.snooze, linger_s=args.linger,
             show_now=show_now, mascot_h=args.size, muted=args.mute).run()


if __name__ == "__main__":
    main()
