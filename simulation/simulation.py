"""
Chernobyl Reactor No. 4 — Interactive Simulation
April 25–26, 1986
Run with: python chernobyl_simulation.py
Requires: Python 3.x (tkinter is included in standard library)
"""

import tkinter as tk
from tkinter import font as tkfont
import math
import random

# ── Colour palette ────────────────────────────────────────────────────────────
BG          = "#1a1a1a"
PANEL_BG    = "#242424"
BORDER      = "#383838"
TEXT_PRI    = "#e8e6e0"
TEXT_SEC    = "#888780"
BLUE        = "#378ADD"
BLUE_DARK   = "#0C447C"
AMBER       = "#EF9F27"
AMBER_DARK  = "#BA7517"
RED         = "#E24B4A"
RED_DARK    = "#A32D2D"
GREEN       = "#639922"
YELLOW      = "#FCDE5A"
GRAY        = "#5F5E5A"
GRAY_LIGHT  = "#B4B2A9"
VESSEL_FILL = "#2c2c2a"
ROD_NORMAL  = "#185FA5"
FUEL_NORMAL = "#3C3489"

# ── Stage data ────────────────────────────────────────────────────────────────
STAGES = [
    {
        "title": "The safety test begins",
        "time":  "April 25, 1986 — 01:06 AM",
        "desc": (
            "Reactor 4 begins powering down for a scheduled safety test. Engineers want to verify "
            "that, during a blackout, the turbines' residual spin could power the emergency cooling "
            "pumps. The test had been postponed repeatedly — operators were under enormous pressure "
            "to complete it quickly before the reactor was needed again for the grid."
        ),
        "power":   "1,600 MW",   "rods":    "205 / 211",  "coolant": "Normal",    "status": "Stable",
        "p_color": GREEN,        "r_color": GREEN,         "c_color": GREEN,       "s_color": GREEN,
        "glow":    0.05,         "rod_frac": 0.85,         "fuel_color": FUEL_NORMAL,
        "explode": False,        "shake":   False,         "radiate": False,
    },
    {
        "title": "Power drops dangerously low",
        "time":  "April 26 — 00:28 AM",
        "desc": (
            "A miscommunication causes reactor output to plummet to just 30 MW — near total shutdown. "
            "Xenon-135 gas, a fission byproduct, floods the core and 'poisons' the reaction by "
            "absorbing neutrons. To revive power, operators pull most control rods out of the core, "
            "leaving far too few inserted. The minimum safe number was 15 rods; they had just 8."
        ),
        "power":   "200 MW",     "rods":    "8 / 211",    "coolant": "Reduced",   "status": "Unstable",
        "p_color": AMBER,        "r_color": RED,           "c_color": AMBER,       "s_color": AMBER,
        "glow":    0.3,          "rod_frac": 0.15,         "fuel_color": AMBER_DARK,
        "explode": False,        "shake":   False,         "radiate": False,
    },
    {
        "title": "Test begins — safety systems disabled",
        "time":  "April 26 — 01:23 AM",
        "desc": (
            "With only 200 MW of power, operators begin the turbine test anyway. To prevent the "
            "reactor from auto-shutting down during the test, the emergency core cooling system "
            "(ECCS) is manually disabled. The reactor is now running unstably with almost no safety "
            "margin — a single unexpected event could trigger a catastrophic cascade."
        ),
        "power":   "200 MW",     "rods":    "6 / 211",    "coolant": "Degraded",  "status": "Critical",
        "p_color": AMBER,        "r_color": RED,           "c_color": RED,         "s_color": RED,
        "glow":    0.45,         "rod_frac": 0.10,         "fuel_color": RED_DARK,
        "explode": False,        "shake":   False,         "radiate": False,
    },
    {
        "title": "Positive void coefficient — runaway begins",
        "time":  "April 26 — 01:23:40 AM",
        "desc": (
            "As coolant water turns to steam, the RBMK reactor's fatal design flaw activates: steam "
            "amplifies the reaction instead of dampening it (positive void coefficient). Power surges "
            "uncontrollably. Shift foreman Leonid Toptunov hits the emergency SCRAM button (AZ-5) "
            "to insert all control rods and shut the reactor down."
        ),
        "power":   "SURGING",    "rods":    "→ inserting","coolant": "Boiling",   "status": "RUNAWAY",
        "p_color": RED,          "r_color": AMBER,         "c_color": RED,         "s_color": RED,
        "glow":    0.75,         "rod_frac": 0.45,         "fuel_color": RED,
        "explode": False,        "shake":   True,          "radiate": False,
    },
    {
        "title": "Graphite tip effect — power spikes to 30,000 MW",
        "time":  "April 26 — 01:23:44 AM",
        "desc": (
            "A second fatal design flaw strikes: the control rods have graphite tips that briefly "
            "amplify the reaction as they enter. Instead of stopping the chain reaction, inserting "
            "the rods accelerates it. Power spikes to an estimated 30,000 MW — 10× the rated maximum "
            "— in just 3 seconds. The fuel begins to fragment and disintegrate inside the channels."
        ),
        "power":   "30,000 MW+", "rods":    "Jammed",     "coolant": "Flash steam","status": "CRITICAL",
        "p_color": RED,          "r_color": RED,           "c_color": RED,          "s_color": RED,
        "glow":    1.0,          "rod_frac": 0.55,         "fuel_color": YELLOW,
        "explode": False,        "shake":   True,          "radiate": False,
    },
    {
        "title": "Steam explosion — reactor destroyed",
        "time":  "April 26 — 01:23:47 AM",
        "desc": (
            "A massive steam explosion tears apart the reactor vessel, blowing off the 1,000-tonne "
            "reinforced concrete lid. A second explosion — possibly nuclear — follows seconds later, "
            "ejecting burning graphite and nuclear fuel across the site. The reactor core is now "
            "open to the sky and burning at over 2,000 °C."
        ),
        "power":   "∞",          "rods":    "Destroyed",  "coolant": "Gone",      "status": "DESTROYED",
        "p_color": RED,          "r_color": RED,           "c_color": RED,         "s_color": RED,
        "glow":    1.0,          "rod_frac": 0.0,          "fuel_color": YELLOW,
        "explode": True,         "shake":   True,          "radiate": False,
    },
    {
        "title": "Radiation release — the aftermath",
        "time":  "April 26 — 01:24 AM onward",
        "desc": (
            "Approximately 400× the radiation of the Hiroshima bomb is released over 10 days. "
            "134 workers suffer acute radiation syndrome; 28 die within months. Soviet authorities "
            "wait 36 hours before evacuating the 49,000 residents of Pripyat — just 3 km away. "
            "The disaster directly triggered redesign of all RBMK reactors and accelerated the "
            "collapse of Soviet public confidence."
        ),
        "power":   "—",          "rods":    "—",           "coolant": "—",         "status": "OPEN CORE",
        "p_color": RED,          "r_color": RED,           "c_color": RED,         "s_color": RED,
        "glow":    0.5,          "rod_frac": 0.0,          "fuel_color": RED,
        "explode": True,         "shake":   False,         "radiate": True,
    },
]

# ── Helper: interpolate hex colours ──────────────────────────────────────────
def lerp_color(c1, c2, t):
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    r = int(r1 + (r2-r1)*t)
    g = int(g1 + (g2-g1)*t)
    b = int(b1 + (b2-b1)*t)
    return f"#{r:02x}{g:02x}{b:02x}"

# ── Main application ──────────────────────────────────────────────────────────
class ChernobylSim(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chernobyl Reactor No. 4 — Event Simulation")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(820, 680)

        self.current = 0
        self._shake_active = False
        self._flash_state  = True
        self._particles    = []          # debris / radiation particles
        self._anim_after   = None

        self._build_ui()
        self._render(animate=False)
        self.after(500, self._tick)

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Top: title bar ──
        top = tk.Frame(self, bg=BG, pady=8)
        top.pack(fill="x", padx=20)
        tk.Label(top, text="☢  Chernobyl Nuclear Power Plant — Reactor No. 4",
                 bg=BG, fg=RED, font=("Courier New", 13, "bold")).pack(side="left")
        tk.Label(top, text="April 25–26, 1986",
                 bg=BG, fg=TEXT_SEC, font=("Courier New", 11)).pack(side="right")

        # ── Stage dots ──
        dot_frame = tk.Frame(self, bg=BG, pady=4)
        dot_frame.pack(fill="x", padx=20)
        tk.Label(dot_frame, text="Timeline:", bg=BG, fg=TEXT_SEC,
                 font=("Courier New", 10)).pack(side="left", padx=(0,10))
        self._dots = []
        for i in range(len(STAGES)):
            d = tk.Canvas(dot_frame, width=16, height=16, bg=BG,
                          highlightthickness=0, cursor="hand2")
            d.pack(side="left", padx=4)
            d.bind("<Button-1>", lambda e, n=i: self._go(n))
            self._dots.append(d)

        # ── Main area: canvas + metrics ──
        mid = tk.Frame(self, bg=BG)
        mid.pack(fill="both", expand=True, padx=20, pady=(0,6))

        # Reactor canvas
        self.canvas = tk.Canvas(mid, bg=BG, highlightthickness=0,
                                width=480, height=360)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Metrics sidebar
        side = tk.Frame(mid, bg=BG, width=200)
        side.pack(side="right", fill="y", padx=(12,0))
        side.pack_propagate(False)

        self._metric_vars = {}
        metrics = [("Reactor power","power"), ("Control rods","rods"),
                   ("Coolant flow","coolant"), ("Core status","status")]
        for label, key in metrics:
            box = tk.Frame(side, bg=PANEL_BG, pady=8, padx=10)
            box.pack(fill="x", pady=4)
            tk.Label(box, text=label.upper(), bg=PANEL_BG, fg=TEXT_SEC,
                     font=("Courier New", 8)).pack(anchor="w")
            v = tk.StringVar()
            lbl = tk.Label(box, textvariable=v, bg=PANEL_BG, fg=GREEN,
                           font=("Courier New", 13, "bold"))
            lbl.pack(anchor="w")
            self._metric_vars[key] = (v, lbl)

        # Separator
        tk.Frame(side, bg=BORDER, height=1).pack(fill="x", pady=8)

        # Mini physics note
        self._physics_var = tk.StringVar()
        tk.Label(side, textvariable=self._physics_var,
                 bg=BG, fg=TEXT_SEC, font=("Courier New", 9),
                 wraplength=190, justify="left").pack(anchor="w")

        # ── Info panel ──
        info = tk.Frame(self, bg=PANEL_BG, padx=16, pady=12,
                        highlightbackground=BORDER, highlightthickness=1)
        info.pack(fill="x", padx=20, pady=(0,6))

        self._title_var = tk.StringVar()
        self._time_var  = tk.StringVar()
        self._desc_var  = tk.StringVar()

        tk.Label(info, textvariable=self._title_var, bg=PANEL_BG, fg=TEXT_PRI,
                 font=("Courier New", 12, "bold"), anchor="w").pack(fill="x")
        tk.Label(info, textvariable=self._time_var, bg=PANEL_BG, fg=AMBER,
                 font=("Courier New", 10), anchor="w").pack(fill="x")
        tk.Label(info, textvariable=self._desc_var, bg=PANEL_BG, fg=TEXT_SEC,
                 font=("Courier New", 10), wraplength=760, justify="left",
                 anchor="w").pack(fill="x", pady=(6,0))

        # ── Navigation buttons ──
        nav = tk.Frame(self, bg=BG, pady=8)
        nav.pack(fill="x", padx=20)
        self._prev_btn = tk.Button(nav, text="← Previous", command=lambda: self._go(self.current-1),
                                   bg=PANEL_BG, fg=TEXT_PRI, relief="flat",
                                   font=("Courier New", 10), padx=16, pady=6,
                                   activebackground=BORDER, cursor="hand2",
                                   highlightbackground=BORDER, highlightthickness=1)
        self._prev_btn.pack(side="left", padx=(0,8))
        self._next_btn = tk.Button(nav, text="Next →", command=lambda: self._go(self.current+1),
                                   bg=RED_DARK, fg=TEXT_PRI, relief="flat",
                                   font=("Courier New", 10), padx=16, pady=6,
                                   activebackground=RED, cursor="hand2")
        self._next_btn.pack(side="left")
        self._stage_counter = tk.Label(nav, bg=BG, fg=TEXT_SEC, font=("Courier New", 10))
        self._stage_counter.pack(side="right")

    # ── Navigation ────────────────────────────────────────────────────────────
    def _go(self, n):
        if 0 <= n < len(STAGES):
            self.current = n
            self._particles = []
            self._render(animate=True)

    # ── Main render ───────────────────────────────────────────────────────────
    def _render(self, animate=True):
        s = STAGES[self.current]
        self._draw_reactor(s)
        self._update_info(s)
        self._update_dots()
        if s["explode"] and not self._particles:
            self._spawn_debris()

    # ── Reactor canvas drawing ────────────────────────────────────────────────
    def _draw_reactor(self, s):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()  or 480
        H = c.winfo_height() or 360

        cx = W // 2         # centre x
        # Building outline
        bx1, by1, bx2, by2 = cx-180, 20, cx+180, H-10
        dash = (8,4) if s["explode"] else ()
        outline_col = RED if s["explode"] else BORDER
        c.create_rectangle(bx1, by1, bx2, by2,
                           outline=outline_col, width=2,
                           dash=dash, fill="")
        c.create_text(cx, by1-10, text="Reactor Building No. 4",
                      fill=TEXT_SEC, font=("Courier New", 9))

        # Vessel
        vx1, vy1, vx2, vy2 = cx-110, by1+30, cx+110, by2-20
        if s["shake"] and self._shake_active:
            ox, oy = random.randint(-3,3), random.randint(-2,2)
            vx1+=ox; vy1+=oy; vx2+=ox; vy2+=oy
        glow_t = s["glow"]
        glow_col = lerp_color("#2c2c2a", "#E24B4A", glow_t)
        c.create_rectangle(vx1, vy1, vx2, vy2,
                           fill=glow_col, outline=GRAY_LIGHT, width=2)

        # Coolant pipes
        pipe_col = RED if s["c_color"] == RED else BLUE
        c.create_line(bx1+10, (vy1+vy2)//2, vx1, (vy1+vy2)//2,
                      fill=pipe_col, width=4, capstyle="round")
        c.create_line(vx2, (vy1+vy2)//2, bx2-10, (vy1+vy2)//2,
                      fill=pipe_col, width=4, capstyle="round")
        c.create_text(bx1+2, (vy1+vy2)//2-10,
                      text="water in" if pipe_col==BLUE else "boiling",
                      fill=pipe_col, font=("Courier New",7), anchor="w")
        c.create_text(bx2-2, (vy1+vy2)//2-10,
                      text="steam out", fill=pipe_col,
                      font=("Courier New",7), anchor="e")

        # Fuel channels + control rods
        vcw  = vx2 - vx1
        n_ch = 7
        ch_w = 14
        gap  = (vcw - n_ch*ch_w) // (n_ch+1)
        for i in range(n_ch):
            fx = vx1 + gap + i*(ch_w+gap)
            # Fuel channel
            c.create_rectangle(fx, vy1+8, fx+ch_w, vy2-8,
                               fill=s["fuel_color"], outline="", width=0)
            # Control rod
            rod_h = int((vy2-vy1-16) * s["rod_frac"])
            rod_col = RED if s["r_color"]==RED else ROD_NORMAL
            c.create_rectangle(fx+2, vy1+8, fx+ch_w-2, vy1+8+rod_h,
                               fill=rod_col, outline="", width=0)

        # Core label
        c.create_text(cx, vy2-12,
                      text="CORE DESTROYED — OPEN TO SKY" if s["explode"] else "reactor core (RBMK-1000)",
                      fill=RED if s["explode"] else TEXT_SEC,
                      font=("Courier New", 8, "bold" if s["explode"] else "normal"))

        # Explosion blast
        if s["explode"]:
            alpha_steps = 6
            for i in range(alpha_steps, 0, -1):
                t = i / alpha_steps
                er = int(150 * t)
                eg = int(100 * t)
                col = lerp_color("#FCDE5A", "#E24B4A", 1-t)
                c.create_oval(cx-er, vy1-eg-40, cx+er, vy1+eg,
                             fill=col, outline="", stipple="gray50" if t<0.5 else "")

        # Debris particles
        for p in self._particles:
            c.create_oval(p[0]-p[4], p[1]-p[4], p[0]+p[4], p[1]+p[4],
                         fill=p[2], outline="")

        # Radiation symbol (stage 7)
        if s["radiate"] and self._flash_state:
            rx, ry, rr = bx2+30, by1+40, 28
            c.create_oval(rx-rr, ry-rr, rx+rr, ry+rr,
                         outline=RED, width=2, fill="")
            c.create_oval(rx-6, ry-6, rx+6, ry+6, fill=RED, outline="")
            for angle in [90, 210, 330]:
                r = math.radians(angle)
                for da in [-25, 25]:
                    ra = math.radians(angle+da)
                    x1 = rx + 8*math.cos(r)
                    y1 = ry - 8*math.sin(r)
                    x2 = rx + (rr-4)*math.cos(ra)
                    y2 = ry - (rr-4)*math.sin(ra)
                    c.create_line(x1, y1, x2, y2, fill=RED, width=1)
            c.create_text(rx, ry+rr+10, text="RADIATION",
                         fill=RED, font=("Courier New", 7, "bold"))

        # Turbine generator box
        tgx = bx2+10
        c.create_rectangle(tgx, (vy1+vy2)//2-20, tgx+60, (vy1+vy2)//2+20,
                           fill=PANEL_BG, outline=BORDER)
        c.create_text(tgx+30, (vy1+vy2)//2,
                     text="turbine\ngenerator",
                     fill=TEXT_SEC, font=("Courier New",7), justify="center")

    # ── Info panel update ─────────────────────────────────────────────────────
    def _update_info(self, s):
        self._title_var.set(f"Stage {self.current+1} / {len(STAGES)} — {s['title']}")
        self._time_var.set(s["time"])
        self._desc_var.set(s["desc"])

        metric_keys = [("power","power","p_color"), ("rods","rods","r_color"),
                       ("coolant","coolant","c_color"), ("status","status","s_color")]
        for key, val_key, col_key in metric_keys:
            v, lbl = self._metric_vars[key]
            v.set(s[val_key])
            lbl.configure(fg=s[col_key])

        physics_notes = [
            "Normal fission: U-235 absorbs\na neutron, splits, releases\nheat + 2-3 new neutrons.",
            "Xenon poisoning: Xe-135\nbuilds up after power drop,\nabsorbs neutrons greedily.",
            "ECCS disabled: emergency\ncore cooling cannot inject\nwater if needed.",
            "+void coefficient: steam\nvoids increase reactivity\ninstead of reducing it.",
            "Graphite tip effect: rods\nboost power for ~3 seconds\nbefore absorbing neutrons.",
            "Steam explosion ruptures\npressure vessel. Open-air\nfire at 2,000 °C.",
            "Half-life of Cs-137:\n30 years. I-131: 8 days.\nExclusion zone: 2,600 km².",
        ]
        self._physics_var.set("⚛ Physics note:\n" + physics_notes[self.current])

        self._prev_btn.configure(state="disabled" if self.current==0 else "normal")
        self._next_btn.configure(state="disabled" if self.current==len(STAGES)-1 else "normal")
        self._stage_counter.configure(text=f"Step {self.current+1} of {len(STAGES)}")

    # ── Stage dots ────────────────────────────────────────────────────────────
    def _update_dots(self):
        for i, d in enumerate(self._dots):
            d.delete("all")
            if i == self.current:
                d.create_oval(2, 2, 14, 14, fill=RED, outline="")
            elif i < self.current:
                d.create_oval(4, 4, 12, 12, fill=GRAY, outline="")
            else:
                d.create_oval(4, 4, 12, 12, fill="", outline=BORDER, width=1.5)

    # ── Debris particles ──────────────────────────────────────────────────────
    def _spawn_debris(self):
        W = self.canvas.winfo_width() or 480
        H = self.canvas.winfo_height() or 360
        cx = W // 2
        cy = 80
        colors = [AMBER, RED, AMBER_DARK, "#633806", FUEL_NORMAL, YELLOW]
        for _ in range(30):
            angle  = random.uniform(0, 2*math.pi)
            speed  = random.uniform(1.5, 4.5)
            self._particles.append([
                cx + random.randint(-20,20),   # x
                cy + random.randint(-10,10),   # y
                random.choice(colors),          # colour
                (math.cos(angle)*speed, math.sin(angle)*speed-2),  # velocity
                random.randint(3,7),            # radius
            ])

    # ── Animation tick ────────────────────────────────────────────────────────
    def _tick(self):
        s = STAGES[self.current]
        self._shake_active = not self._shake_active
        self._flash_state  = not self._flash_state

        W = self.canvas.winfo_width()  or 480
        H = self.canvas.winfo_height() or 360

        # Move debris
        if self._particles:
            alive = []
            for p in self._particles:
                p[0] += p[3][0]
                p[1] += p[3][1]
                p[3] = (p[3][0]*0.97, p[3][1]+0.15)   # friction + gravity
                if 0 <= p[0] <= W and 0 <= p[1] <= H:
                    alive.append(p)
            self._particles = alive

        self._draw_reactor(s)
        self.after(80, self._tick)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ChernobylSim()
    app.mainloop()