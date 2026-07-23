#!/usr/bin/env python3
"""
Sun Meeting Buddy
=================
A cheerful desktop mascot who pops up on a timer (every 30 minutes by
default) to nudge you toward your next meeting so you show up on time.

Pure standard-library Tkinter -- no dependencies required. If Pillow is
installed it is used for nicer image scaling, but it is entirely optional.

Usage:
    python buddy.py                 # pop up every 30 minutes
    python buddy.py --every 15      # ...every 15 minutes instead
    python buddy.py --now           # also show one immediately on launch
    python buddy.py --snooze 5      # snooze button adds 5 minutes

Quit any time from your terminal with Ctrl+C, or use the "Not now" ->
tray-less design: closing the popup just hides it until the next tick.
"""

import argparse
import os
import random
import sys
import tkinter as tk
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
MASCOT_PATH = os.path.join(HERE, "assets", "mascot.png")

# --- palette (sunny) --------------------------------------------------------
CARD_BG = "#FFF6D8"      # warm cream card
ACCENT = "#F5A623"       # sun orange
ACCENT_DK = "#E0871C"
INK = "#4A3B10"          # deep warm brown text
INK_SOFT = "#8A7530"
BTN_GO = "#2FB170"       # green "on my way"
BTN_GO_DK = "#26935D"
BTN_SNOOZE = "#F0E2A8"

HYPE_LINES = [
    "Meeting soon, superstar. Let's shine on time. ☀️",
    "Two minutes early = right on time. You got this!",
    "Wrap it up, hydrate, and roll into that meeting like a boss.",
    "The calendar called. It said: be legendary AND punctual.",
    "Save the tab. Grab the notes. Go make that meeting.",
    "Big sun energy: warm, bright, and never late.",
    "Future you is thanking present you for leaving now.",
    "Peace out of this task ✌️ -- your meeting awaits.",
    "Stand up, stretch, sparkle. Meeting time is near!",
    "Be the person who joins the call first. Iconic.",
]


class Buddy:
    def __init__(self, interval_min: float, snooze_min: float, show_now: bool):
        self.interval_ms = int(interval_min * 60_000)
        self.snooze_ms = int(snooze_min * 60_000)
        self.snooze_min = snooze_min

        self.root = tk.Tk()
        self.root.withdraw()  # the controller window stays hidden
        self.root.title("Sun Meeting Buddy")

        self.image = self._load_image()
        self.popup = None
        self._next_tick = None

        first_delay = 200 if show_now else self.interval_ms
        self._schedule(first_delay)
        self._log_next(first_delay)

    # -- image ---------------------------------------------------------------
    def _load_image(self):
        """Return a Tk PhotoImage of the mascot, scaled to a friendly size."""
        target_w = 300
        try:
            from PIL import Image, ImageTk  # optional, nicer scaling
            img = Image.open(MASCOT_PATH)
            h = round(img.height * target_w / img.width)
            img = img.resize((target_w, h), Image.LANCZOS)
            # Composite onto the card colour so alpha edges blend cleanly.
            bg = Image.new("RGBA", img.size, CARD_BG)
            bg.alpha_composite(img.convert("RGBA"))
            return ImageTk.PhotoImage(bg.convert("RGB"))
        except Exception:
            # Stdlib fallback: PhotoImage reads PNG (Tk 8.6+) and honours
            # alpha against the widget background. Subsample to shrink.
            img = tk.PhotoImage(file=MASCOT_PATH)
            factor = max(1, round(img.width() / target_w))
            if factor > 1:
                img = img.subsample(factor, factor)
            return img

    # -- scheduling ----------------------------------------------------------
    def _schedule(self, delay_ms: int):
        if self._next_tick is not None:
            self.root.after_cancel(self._next_tick)
        self._next_tick = self.root.after(delay_ms, self._tick)

    def _log_next(self, delay_ms: int):
        when = (datetime.now() + timedelta(milliseconds=delay_ms)).strftime("%H:%M")
        print(f"[sun-buddy] next pop-up at {when}", flush=True)

    def _tick(self):
        self._show_popup()
        self._schedule(self.interval_ms)
        self._log_next(self.interval_ms)

    # -- popup ---------------------------------------------------------------
    def _show_popup(self):
        if self.popup is not None and tk.Toplevel.winfo_exists(self.popup):
            self.popup.destroy()

        p = tk.Toplevel(self.root)
        self.popup = p
        p.overrideredirect(True)          # borderless mascot card
        p.attributes("-topmost", True)
        try:
            p.attributes("-alpha", 0.0)   # for fade-in
        except tk.TclError:
            pass
        p.configure(bg=ACCENT)

        # 2px accent frame around a cream card
        card = tk.Frame(p, bg=CARD_BG)
        card.pack(padx=3, pady=3)

        tk.Label(
            card, image=self.image, bg=CARD_BG, borderwidth=0, highlightthickness=0
        ).pack(padx=22, pady=(18, 4))

        tk.Label(
            card, text="Meeting check-in!", bg=CARD_BG, fg=ACCENT_DK,
            font=("Helvetica", 20, "bold"),
        ).pack()

        tk.Label(
            card, text=random.choice(HYPE_LINES), bg=CARD_BG, fg=INK,
            font=("Helvetica", 12), wraplength=300, justify="center",
        ).pack(padx=24, pady=(6, 2))

        tk.Label(
            card, text="It's " + datetime.now().strftime("%I:%M %p").lstrip("0"),
            bg=CARD_BG, fg=INK_SOFT, font=("Helvetica", 11, "italic"),
        ).pack(pady=(0, 10))

        btns = tk.Frame(card, bg=CARD_BG)
        btns.pack(padx=20, pady=(0, 20), fill="x")

        go = tk.Button(
            btns, text="On my way!  ✅", command=p.destroy,
            bg=BTN_GO, fg="white", activebackground=BTN_GO_DK,
            activeforeground="white", font=("Helvetica", 12, "bold"),
            relief="flat", borderwidth=0, padx=14, pady=9, cursor="hand2",
        )
        go.pack(side="left", expand=True, fill="x", padx=(0, 6))

        snooze = tk.Button(
            btns, text=f"Snooze {int(self.snooze_min)}m  \U0001F634",
            command=lambda: self._snooze(p),
            bg=BTN_SNOOZE, fg=INK, activebackground="#E6D48A",
            activeforeground=INK, font=("Helvetica", 12, "bold"),
            relief="flat", borderwidth=0, padx=14, pady=9, cursor="hand2",
        )
        snooze.pack(side="left", expand=True, fill="x", padx=(6, 0))

        # Let the user drag the card around.
        self._make_draggable(p, card)
        for lbl in card.winfo_children():
            if isinstance(lbl, tk.Label):
                self._make_draggable(p, lbl)

        # Bottom-right of the screen, with a small margin.
        p.update_idletasks()
        sw, sh = p.winfo_screenwidth(), p.winfo_screenheight()
        w, h = p.winfo_width(), p.winfo_height()
        x, y = sw - w - 28, sh - h - 60
        p.geometry(f"+{x}+{y}")

        p.bind("<Escape>", lambda _e: p.destroy())
        self._fade_in(p)

    def _snooze(self, popup):
        popup.destroy()
        self._schedule(self.snooze_ms)
        self._log_next(self.snooze_ms)

    def _fade_in(self, p, value=0.0):
        if not tk.Toplevel.winfo_exists(p):
            return
        try:
            p.attributes("-alpha", value)
        except tk.TclError:
            return
        if value < 1.0:
            p.after(16, lambda: self._fade_in(p, min(1.0, value + 0.08)))

    def _make_draggable(self, popup, widget):
        def start(e):
            widget._dx, widget._dy = e.x, e.y

        def move(e):
            x = popup.winfo_x() + e.x - getattr(widget, "_dx", 0)
            y = popup.winfo_y() + e.y - getattr(widget, "_dy", 0)
            popup.geometry(f"+{x}+{y}")

        widget.bind("<Button-1>", start)
        widget.bind("<B1-Motion>", move)

    # -- run -----------------------------------------------------------------
    def run(self):
        print(
            "[sun-buddy] running. Leave this open; I'll pop up on schedule.\n"
            "[sun-buddy] press Ctrl+C here to stop.",
            flush=True,
        )
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n[sun-buddy] bye! stay punctual ☀️")


def main(argv=None):
    ap = argparse.ArgumentParser(description="A sunny mascot that reminds you to make your meetings on time.")
    ap.add_argument("--every", type=float, default=30, metavar="MIN",
                    help="minutes between pop-ups (default: 30)")
    ap.add_argument("--snooze", type=float, default=5, metavar="MIN",
                    help="minutes the snooze button adds (default: 5)")
    ap.add_argument("--now", action="store_true",
                    help="show a pop-up immediately on launch too")
    args = ap.parse_args(argv)

    if not os.path.exists(MASCOT_PATH):
        sys.exit(f"[sun-buddy] missing mascot image at {MASCOT_PATH}")

    Buddy(interval_min=args.every, snooze_min=args.snooze, show_now=args.now).run()


if __name__ == "__main__":
    main()
