"""
CHERNOBYL REACTOR No.4 — Nuclear Physics Particle Simulation
=============================================================
Shows what ACTUALLY happened inside the RBMK-1000 reactor core:
  • Uranium-235 fission chain reactions (neutron cascades)
  • Xenon-135 poisoning (absorbing neutrons, killing the reaction)
  • Control rod withdrawal (desperately trying to revive power)
  • Positive void coefficient (steam voids amplifying reactions)
  • Graphite tip effect (rods accelerating the runaway)
  • Catastrophic power excursion → steam explosion

Run:  pip install pygame  then  python chernobyl_pygame.py
"""

import pygame
import math, random, sys, time
from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum, auto

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
W, H        = 1600, 1000
FPS         = 60
CORE_X      = 110         # reactor core left edge
CORE_Y      = 80
CORE_W      = 780
CORE_H      = 780
COLS        = 14           # fuel channel columns
ROWS        = 14           # fuel channel rows
CH_W        = CORE_W // COLS
CH_H        = CORE_H // ROWS

# Particle colours
C_BG        = (10,  10,  14)
C_GRID      = (30,  30,  45)
C_VESSEL    = (40,  55,  80)
C_URANIUM   = (180, 140,  30)   # gold
C_NEUTRON   = (220, 240, 255)   # white-blue
C_FISSION   = (255, 200,  50)   # bright yellow flash
C_XENON     = (100,  60, 180)   # purple — absorber
C_STEAM     = (150, 200, 230)   # pale blue
C_GRAPHITE  = (160, 160, 160)   # gray
C_ROD       = ( 20,  80, 160)   # deep blue
C_ROD_HOT   = (220,  80,  40)   # orange-red (graphite tip)
C_GAMMA     = (255, 255, 120)   # gamma ray
C_PLASMA    = (255, 120,  40)   # hot plasma / explosion
C_EXPLOSION = (255,  60,  10)
C_GLOW_R    = (200,  30,  10)
C_TEXT_HI   = (255, 220, 100)
C_TEXT_LO   = (130, 140, 160)
C_GREEN     = ( 60, 200,  80)
C_AMBER     = (230, 160,  30)
C_RED       = (220,  50,  40)
C_PANEL     = ( 18,  18,  28)
C_BORDER    = ( 50,  60,  90)

# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION STAGES
# ══════════════════════════════════════════════════════════════════════════════
class Stage(Enum):
    NORMAL        = 0
    XENON_POISON  = 1
    ROD_WITHDRAW  = 2
    VOID_COEFF    = 3
    GRAPHITE_TIP  = 4
    RUNAWAY       = 5
    EXPLOSION     = 6
    AFTERMATH     = 7

STAGE_INFO = {
    Stage.NORMAL: {
        "title": "NORMAL OPERATION",
        "time":  "Apr 25, 1986  01:06",
        "color": C_GREEN,
        "power": 1600,
        "desc":  [
            "Reactor running at 1,600 MW thermal.",
            "U-235 fissions release 2-3 neutrons each.",
            "Control rods absorb excess neutrons,",
            "keeping chain reaction stable.",
            "Coolant water flows normally.",
        ],
        "physics": "n + U235 → Ba141 + Kr92 + 3n + γ",
    },
    Stage.XENON_POISON: {
        "title": "XENON-135 POISONING",
        "time":  "Apr 26  00:28",
        "color": C_AMBER,
        "power": 30,
        "desc":  [
            "Power drops to ~30 MW accidentally.",
            "Xe-135 (fission byproduct) floods core.",
            "Xenon absorbs neutrons voraciously —",
            "σ_abs = 2.6 million barns!",
            "Chain reaction nearly collapses.",
        ],
        "physics": "Xe135 + n → Xe136  (σ=2.6Mb)",
    },
    Stage.ROD_WITHDRAW: {
        "title": "DESPERATE ROD WITHDRAWAL",
        "time":  "Apr 26  01:00",
        "color": C_AMBER,
        "power": 200,
        "desc":  [
            "Operators pull control rods out",
            "to overcome xenon poisoning.",
            "Only 6-8 rods remain inserted.",
            "Minimum safe: 15 rods.",
            "Reactor dangerously under-controlled.",
        ],
        "physics": "Reactivity margin: CRITICALLY LOW",
    },
    Stage.VOID_COEFF: {
        "title": "POSITIVE VOID COEFFICIENT",
        "time":  "Apr 26  01:23:00",
        "color": C_RED,
        "power": 200,
        "desc":  [
            "Test begins. Coolant flow reduces.",
            "Water turns to steam (voids form).",
            "RBMK flaw: steam INCREASES reactivity",
            "(water was absorbing neutrons).",
            "Power begins rising uncontrolled.",
        ],
        "physics": "∂k/∂void > 0  ← FATAL FLAW",
    },
    Stage.GRAPHITE_TIP: {
        "title": "GRAPHITE TIP EFFECT",
        "time":  "Apr 26  01:23:40",
        "color": C_RED,
        "power": 30000,
        "desc":  [
            "SCRAM (AZ-5) button pressed!",
            "Control rods descend into core.",
            "BUT: graphite tips enter first —",
            "graphite MODERATES, not absorbs!",
            "Rods AMPLIFY reaction for 3 sec.",
        ],
        "physics": "Graphite: moderator (not absorber)",
    },
    Stage.RUNAWAY: {
        "title": "POWER EXCURSION  ████ CRITICAL",
        "time":  "Apr 26  01:23:44",
        "color": C_RED,
        "power": 30000,
        "desc":  [
            "Power hits 30,000 MW — 10× rated max.",
            "Fuel pellets fragment & vaporize.",
            "Coolant flashes to steam instantly.",
            "Pressure rises beyond all limits.",
            "Control rods jam — cannot insert.",
        ],
        "physics": "Prompt criticality exceeded",
    },
    Stage.EXPLOSION: {
        "title": "STEAM EXPLOSION",
        "time":  "Apr 26  01:23:47",
        "color": C_RED,
        "power": 0,
        "desc":  [
            "FIRST EXPLOSION: Steam blast.",
            "1,000-tonne reactor lid launched.",
            "SECOND EXPLOSION: Prompt nuclear?",
            "Burning graphite ejected to roof.",
            "Core open to atmosphere.",
        ],
        "physics": "≈ 400× Hiroshima radiation released",
    },
    Stage.AFTERMATH: {
        "title": "OPEN CORE — RADIATION RELEASE",
        "time":  "Apr 26  01:24 →",
        "color": C_RED,
        "power": 0,
        "desc":  [
            "Graphite fire burns for 10 days.",
            "Cs-137, I-131, Sr-90 released.",
            "134 workers: acute radiation syndrome.",
            "28 die within months.",
            "49,000 evacuated from Pripyat.",
        ],
        "physics": "Cs137 half-life: 30 years",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  PARTICLE CLASSES
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    color: Tuple
    radius: float
    life: float        # 0..1
    decay: float       # life lost per frame
    kind: str          # 'neutron','fission','xenon','steam','debris','gamma'
    glow: bool = False
    data: dict = field(default_factory=dict)

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        self.life -= self.decay
        return self.life > 0

    def draw(self, surf):
        alpha = max(0, min(255, int(self.life * 255)))
        r = max(1, int(self.radius * self.life**0.3))
        col = tuple(min(255, int(c * self.life**0.2)) for c in self.color)
        if self.glow and r > 2:
            gsurf = pygame.Surface((r*6, r*6), pygame.SRCALPHA)
            gc = (*col, max(0, alpha // 4))
            pygame.draw.circle(gsurf, gc, (r*3, r*3), r*3)
            surf.blit(gsurf, (int(self.x)-r*3, int(self.y)-r*3))
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), r)


@dataclass
class FuelCell:
    col: int
    row: int
    energy: float = 0.5    # 0..1  heat level
    xenon: float  = 0.0    # xenon poisoning 0..1
    steam: float  = 0.0    # void fraction 0..1
    fissioning: int = 0    # frames of active fission flash

    @property
    def cx(self): return CORE_X + self.col * CH_W + CH_W // 2
    @property
    def cy(self): return CORE_Y + self.row * CH_H + CH_H // 2

    def color(self):
        if self.fissioning > 0:
            t = self.fissioning / 8
            r = int(255)
            g = int(200 * t + 80*(1-t))
            b = int(50 * t)
            return (r, g, b)
        # blend: cool blue → uranium gold → red hot
        t = self.energy
        if t < 0.5:
            s = t * 2
            return (int(40+100*s), int(40+100*s), int(80+80*(1-s)))
        else:
            s = (t - 0.5) * 2
            return (int(140+115*s), int(140-100*s), int(40-30*s))


# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class Reactor:
    def __init__(self):
        self.stage       = Stage.NORMAL
        self.frame       = 0
        self.particles   : List[Particle] = []
        self.fuel        = [[FuelCell(c, r) for c in range(COLS)] for r in range(ROWS)]
        self.rod_frac    = 0.85     # fraction of rods inserted (0=out, 1=in)
        self.power_mw    = 1600
        self.target_pw   = 1600
        self.neutron_mult= 1.0      # effective neutron multiplier
        self.exploded    = False
        self.explosion_t = 0
        self.shake       = 0        # screen shake frames

        # Spawn background neutrons for normal operation
        self._spawn_timer = 0

    # ── Stage transition ─────────────────────────────────────────────────────
    def set_stage(self, s: Stage):
        self.stage = s
        info = STAGE_INFO[s]
        self.target_pw = info["power"]
        self.particles.clear()

        if s == Stage.XENON_POISON:
            # Flood with xenon
            for row in self.fuel:
                for cell in row:
                    cell.xenon = random.uniform(0.4, 0.9)
            self.neutron_mult = 0.05
        elif s == Stage.ROD_WITHDRAW:
            self.rod_frac = 0.08
            for row in self.fuel:
                for cell in row:
                    cell.xenon = random.uniform(0.1, 0.4)
            self.neutron_mult = 0.3
        elif s == Stage.VOID_COEFF:
            self.rod_frac = 0.06
            for row in self.fuel:
                for cell in row:
                    cell.xenon = 0.0
                    cell.steam = random.uniform(0.1, 0.5)
            self.neutron_mult = 0.8
        elif s == Stage.GRAPHITE_TIP:
            self.rod_frac = 0.35
            self.neutron_mult = 3.0
            for row in self.fuel:
                for cell in row:
                    cell.steam = random.uniform(0.4, 0.9)
        elif s == Stage.RUNAWAY:
            self.rod_frac = 0.0
            self.neutron_mult = 8.0
            for row in self.fuel:
                for cell in row:
                    cell.energy = random.uniform(0.7, 1.0)
                    cell.steam  = 1.0
        elif s == Stage.EXPLOSION:
            self.exploded = True
            self.explosion_t = 0
            self.shake = 120
            self._trigger_explosion()
        elif s == Stage.AFTERMATH:
            self.exploded = True
            self.rod_frac = 0.0
        elif s == Stage.NORMAL:
            self.rod_frac = 0.85
            self.neutron_mult = 1.0
            self.exploded = False
            for row in self.fuel:
                for cell in row:
                    cell.energy = 0.4
                    cell.xenon  = 0.0
                    cell.steam  = 0.0

    # ── Explosion particles ───────────────────────────────────────────────────
    def _trigger_explosion(self):
        cx = CORE_X + CORE_W // 2
        cy = CORE_Y + CORE_H // 2
        for _ in range(400):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(2, 18)
            col   = random.choice([C_EXPLOSION, C_PLASMA, C_FISSION,
                                   (255,200,50), (200,30,10)])
            self.particles.append(Particle(
                cx + random.randint(-80,80),
                cy + random.randint(-80,80),
                math.cos(angle)*speed, math.sin(angle)*speed - random.uniform(0,4),
                col, random.uniform(4,14), 1.0,
                random.uniform(0.003, 0.012), 'debris', glow=True
            ))
        # Shockwave ring particles
        for i in range(80):
            angle = math.tau * i / 80
            speed = random.uniform(6, 14)
            self.particles.append(Particle(
                cx, cy,
                math.cos(angle)*speed, math.sin(angle)*speed,
                C_STEAM, random.uniform(3,8), 1.0, 0.008, 'steam', glow=True
            ))

    # ── Spawn physics particles ───────────────────────────────────────────────
    def _emit(self):
        stage = self.stage
        mult  = self.neutron_mult

        if self.exploded and stage not in (Stage.EXPLOSION, Stage.AFTERMATH):
            return

        # Rate of neutron emission based on stage
        rates = {
            Stage.NORMAL:       3,
            Stage.XENON_POISON: 0,
            Stage.ROD_WITHDRAW: 1,
            Stage.VOID_COEFF:   4,
            Stage.GRAPHITE_TIP: 12,
            Stage.RUNAWAY:      30,
            Stage.EXPLOSION:    0,
            Stage.AFTERMATH:    1,
        }
        rate = rates.get(stage, 1)

        for _ in range(rate):
            # Pick a random fuel cell
            r = random.randint(0, ROWS-1)
            c = random.randint(0, COLS-1)
            cell = self.fuel[r][c]

            # Skip if cell is xenon-suppressed
            if stage == Stage.XENON_POISON and random.random() < cell.xenon:
                # Spawn xenon absorption event
                if random.random() < 0.3:
                    self.particles.append(Particle(
                        cell.cx + random.randint(-10,10),
                        cell.cy + random.randint(-10,10),
                        random.uniform(-0.3,0.3), random.uniform(-0.5,0.0),
                        C_XENON, random.uniform(3,6), 1.0, 0.02, 'xenon', glow=True
                    ))
                continue

            # Fission event — trigger cell flash
            cell.fissioning = random.randint(4, 10)
            cell.energy = min(1.0, cell.energy + 0.05 * mult)

            # Fission flash
            self.particles.append(Particle(
                cell.cx, cell.cy, 0, 0,
                C_FISSION, 10*mult, 1.0, 0.08, 'fission', glow=True
            ))

            # Emit 2-3 neutrons per fission
            n_neutrons = int(2 + mult * 0.5 + random.random())
            for _ in range(min(n_neutrons, 5)):
                angle = random.uniform(0, math.tau)
                spd   = random.uniform(2, 5) * min(mult, 4)
                self.particles.append(Particle(
                    cell.cx, cell.cy,
                    math.cos(angle)*spd, math.sin(angle)*spd,
                    C_NEUTRON, random.uniform(2,4), 1.0,
                    random.uniform(0.015, 0.04), 'neutron'
                ))

            # Gamma ray lines
            if random.random() < 0.4:
                angle = random.uniform(0, math.tau)
                spd   = 8
                self.particles.append(Particle(
                    cell.cx, cell.cy,
                    math.cos(angle)*spd, math.sin(angle)*spd,
                    C_GAMMA, 2, 1.0, 0.05, 'gamma'
                ))

            # Steam voids
            if stage in (Stage.VOID_COEFF, Stage.GRAPHITE_TIP, Stage.RUNAWAY):
                cell.steam = min(1.0, cell.steam + 0.02)
                if random.random() < 0.3:
                    self.particles.append(Particle(
                        cell.cx + random.randint(-CH_W//3, CH_W//3),
                        cell.cy + random.randint(-CH_H//3, CH_H//3),
                        random.uniform(-0.5,0.5), random.uniform(-2,-0.5),
                        C_STEAM, random.uniform(2,5), 0.8, 0.012, 'steam'
                    ))

        # Runaway: continuous chain cascade flood
        if stage == Stage.RUNAWAY:
            for _ in range(20):
                r = random.randint(0, ROWS-1)
                c = random.randint(0, COLS-1)
                cell = self.fuel[r][c]
                cell.energy = min(1.0, cell.energy + 0.08)
                cell.fissioning = 6
                angle = random.uniform(0, math.tau)
                spd = random.uniform(3, 9)
                self.particles.append(Particle(
                    cell.cx, cell.cy,
                    math.cos(angle)*spd, math.sin(angle)*spd,
                    random.choice([C_FISSION, C_PLASMA, (255,160,40)]),
                    random.uniform(3,8), 1.0, 0.025, 'fission', glow=True
                ))

        # Aftermath: radiation particles drifting up
        if stage == Stage.AFTERMATH:
            for _ in range(5):
                cx = CORE_X + random.randint(0, CORE_W)
                cy = CORE_Y + random.randint(0, CORE_H)
                self.particles.append(Particle(
                    cx, cy,
                    random.uniform(-1,1), random.uniform(-3,-0.5),
                    random.choice([(180,50,200),(220,80,50),(100,200,100)]),
                    random.uniform(2,4), 0.8, 0.005, 'gamma'
                ))

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self):
        self.frame += 1
        if self.shake > 0:
            self.shake -= 1

        # Smooth power display
        self.power_mw += (self.target_pw - self.power_mw) * 0.03

        # Fuel cell cooling/heating
        for row in self.fuel:
            for cell in row:
                if cell.fissioning > 0:
                    cell.fissioning -= 1
                stage_hot = self.stage in (Stage.RUNAWAY, Stage.GRAPHITE_TIP)
                if stage_hot:
                    cell.energy = min(1.0, cell.energy + 0.005)
                else:
                    cell.energy = max(0.0, cell.energy - 0.003)
                if self.stage == Stage.XENON_POISON:
                    cell.xenon = min(1.0, cell.xenon + 0.001)

        # Emit particles
        self._spawn_timer += 1
        if self._spawn_timer >= 1:
            self._spawn_timer = 0
            self._emit()

        # Update explosion
        if self.stage == Stage.EXPLOSION:
            self.explosion_t += 1
            if self.explosion_t % 3 == 0 and self.explosion_t < 120:
                cx = CORE_X + random.randint(0, CORE_W)
                cy = CORE_Y + random.randint(0, CORE_H)
                self.particles.append(Particle(
                    cx, cy,
                    random.uniform(-3,3), random.uniform(-6,-1),
                    random.choice([C_PLASMA, C_EXPLOSION, C_FISSION]),
                    random.uniform(5,12), 1.0, 0.006, 'debris', glow=True
                ))

        # Update particles
        self.particles = [p for p in self.particles if p.update()]

        # Cap particle count
        if len(self.particles) > 3000:
            self.particles = self.particles[-3000:]


# ══════════════════════════════════════════════════════════════════════════════
#  RENDERER
# ══════════════════════════════════════════════════════════════════════════════
class Renderer:
    def __init__(self, surf: pygame.Surface):
        self.surf  = surf
        self.font_title = pygame.font.SysFont("Courier New", 19, bold=True)
        self.font_body  = pygame.font.SysFont("Courier New", 15)
        self.font_big   = pygame.font.SysFont("Courier New", 24, bold=True)
        self.font_mono  = pygame.font.SysFont("Courier New", 16)

    def draw_core_grid(self, reactor: Reactor):
        s = self.surf
        # Vessel background
        pygame.draw.rect(s, C_VESSEL, (CORE_X-4, CORE_Y-4, CORE_W+8, CORE_H+8), 3, border_radius=8)
        pygame.draw.rect(s, (15, 18, 30), (CORE_X, CORE_Y, CORE_W, CORE_H))

        # Fuel cells
        for row in reactor.fuel:
            for cell in row:
                x = CORE_X + cell.col * CH_W
                y = CORE_Y + cell.row * CH_H
                col = cell.color()

                # Xenon tint overlay
                if cell.xenon > 0.1:
                    r2 = int(col[0] * (1-cell.xenon*0.6) + 80*cell.xenon)
                    g2 = int(col[1] * (1-cell.xenon*0.6) + 20*cell.xenon)
                    b2 = int(col[2] * (1-cell.xenon*0.6) + 180*cell.xenon)
                    col = (r2, g2, b2)

                # Steam void: desaturate
                if cell.steam > 0.2:
                    avg = int((col[0]+col[1]+col[2])//3)
                    col = (
                        int(col[0]*(1-cell.steam*0.4) + avg*cell.steam*0.4),
                        int(col[1]*(1-cell.steam*0.4) + avg*cell.steam*0.4),
                        int(col[2]*(1-cell.steam*0.4) + avg*cell.steam*0.4),
                    )

                pygame.draw.rect(s, col, (x+1, y+1, CH_W-2, CH_H-2))

                # Grid lines
                pygame.draw.rect(s, C_GRID, (x, y, CH_W, CH_H), 1)

        # Control rods
        rod_col = COLS
        rod_spacing = CORE_W / rod_col
        inserted = reactor.rod_frac
        rod_h    = int(CORE_H * inserted)

        for i in range(rod_col):
            rx = CORE_X + int(i * rod_spacing) + 3
            # Graphite tip (orange) when being inserted in graphite-tip stage
            if reactor.stage == Stage.GRAPHITE_TIP and inserted > 0.1:
                tip_h = min(20, rod_h)
                pygame.draw.rect(s, C_ROD_HOT, (rx, CORE_Y, rod_spacing-6, tip_h), border_radius=2)
                pygame.draw.rect(s, C_ROD,     (rx, CORE_Y+tip_h, rod_spacing-6, max(0,rod_h-tip_h)), border_radius=2)
            else:
                pygame.draw.rect(s, C_ROD,     (rx, CORE_Y, rod_spacing-6, rod_h), border_radius=2)

        # Core label
        lbl = self.font_body.render("RBMK-1000 CORE  (" + str(COLS) + "×" + str(ROWS) + " channels)", True, C_TEXT_LO)
        self.surf.blit(lbl, (CORE_X, CORE_Y + CORE_H + 6))

    def draw_particles(self, reactor: Reactor):
        for p in reactor.particles:
            p.draw(self.surf)

    def draw_explosion_overlay(self, reactor: Reactor):
        if not reactor.exploded:
            return
        t = min(1.0, reactor.explosion_t / 60) if reactor.stage == Stage.EXPLOSION else 0.4
        if t > 0:
            flash = pygame.Surface((W, H), pygame.SRCALPHA)
            flash.fill((255, 140, 30, int(t * 120)))
            self.surf.blit(flash, (0, 0))

    def draw_panel(self, reactor: Reactor, stage_idx: int):
        info  = STAGE_INFO[reactor.stage]
        px    = CORE_X + CORE_W + 20
        pw    = W - px - 10
        py    = 10

        # Panel bg
        pygame.draw.rect(self.surf, C_PANEL, (px, py, pw, H-20), border_radius=8)
        pygame.draw.rect(self.surf, C_BORDER, (px, py, pw, H-20), 1, border_radius=8)

        y = py + 14

        # Stage number
        stg_txt = self.font_title.render(f"STAGE {stage_idx+1} / {len(Stage)}", True, C_TEXT_LO)
        self.surf.blit(stg_txt, (px+12, y))
        y += 20

        # Title
        title_lines = info["title"].split("  ")
        for tl in title_lines:
            t = self.font_big.render(tl, True, info["color"])
            self.surf.blit(t, (px+12, y))
            y += 22
        y += 4

        # Time
        tc = self.font_mono.render(info["time"], True, (180, 160, 100))
        self.surf.blit(tc, (px+12, y))
        y += 20

        # Divider
        pygame.draw.line(self.surf, C_BORDER, (px+12, y), (px+pw-12, y))
        y += 10

        # Description
        for line in info["desc"]:
            dl = self.font_body.render(line, True, C_TEXT_LO)
            self.surf.blit(dl, (px+12, y))
            y += 22
        y += 10

        # Physics equation
        pygame.draw.line(self.surf, C_BORDER, (px+12, y), (px+pw-12, y))
        y += 8
        eq = self.font_mono.render(info["physics"], True, (120, 200, 130))
        self.surf.blit(eq, (px+12, y))
        y += 24

        # ── Power meter ──
        pygame.draw.line(self.surf, C_BORDER, (px+12, y), (px+pw-12, y))
        y += 10
        pw_label = self.font_body.render("REACTOR POWER", True, C_TEXT_LO)
        self.surf.blit(pw_label, (px+12, y))
        y += 16
        max_mw = 32000
        bar_w  = pw - 24
        frac   = min(1.0, reactor.power_mw / max_mw)
        bar_col = C_GREEN if frac < 0.15 else C_AMBER if frac < 0.6 else C_RED
        pygame.draw.rect(self.surf, C_GRID,  (px+12, y, bar_w, 18), border_radius=4)
        pygame.draw.rect(self.surf, bar_col, (px+12, y, int(bar_w*frac), 18), border_radius=4)
        pval = f"{int(reactor.power_mw):,} MW" if reactor.power_mw > 1 else "< 1 MW"
        pv   = self.font_body.render(pval, True, bar_col)
        self.surf.blit(pv, (px+12, y+20))
        y += 46

        # ── Control rod status ──
        cr_label = self.font_body.render("CONTROL RODS INSERTED", True, C_TEXT_LO)
        self.surf.blit(cr_label, (px+12, y))
        y += 16
        frac_r = reactor.rod_frac
        rod_col = C_GREEN if frac_r > 0.5 else C_AMBER if frac_r > 0.15 else C_RED
        pygame.draw.rect(self.surf, C_GRID, (px+12, y, bar_w, 18), border_radius=4)
        pygame.draw.rect(self.surf, rod_col, (px+12, y, int(bar_w*frac_r), 18), border_radius=4)
        rv = self.font_body.render(f"{frac_r*100:.0f}%  ({int(frac_r*211)}/211 rods)", True, rod_col)
        self.surf.blit(rv, (px+12, y+20))
        y += 46

        # ── Legend ──
        pygame.draw.line(self.surf, C_BORDER, (px+12, y), (px+pw-12, y))
        y += 8
        leg = self.font_body.render("LEGEND", True, C_TEXT_LO)
        self.surf.blit(leg, (px+12, y))
        y += 16
        legend_items = [
            (C_NEUTRON, "Neutron"),
            (C_FISSION, "Fission event"),
            (C_XENON,   "Xenon absorption"),
            (C_STEAM,   "Steam void"),
            (C_GAMMA,   "Gamma radiation"),
            (C_ROD,     "Control rod"),
            (C_ROD_HOT, "Graphite tip"),
            (C_PLASMA,  "Plasma / explosion"),
        ]
        for col, name in legend_items:
            pygame.draw.circle(self.surf, col, (px+20, y+7), 6)
            nl = self.font_body.render(name, True, C_TEXT_LO)
            self.surf.blit(nl, (px+34, y))
            y += 22
        y += 6

        # ── Navigation hint ──
        pygame.draw.line(self.surf, C_BORDER, (px+12, y), (px+pw-12, y))
        y += 8
        nh = self.font_body.render("← → Arrow keys  /  1-8  /  SPACE", True, (80,90,110))
        self.surf.blit(nh, (px+12, y))
        y += 14
        nh2 = self.font_body.render("to advance stages", True, (80,90,110))
        self.surf.blit(nh2, (px+12, y))

    def draw_hud(self, reactor: Reactor):
        # Top-left: particle count
        pc = self.font_body.render(f"particles: {len(reactor.particles)}", True, (50,60,80))
        self.surf.blit(pc, (CORE_X, 8))

    def draw_xenon_cloud(self, reactor: Reactor):
        """Visualise xenon as a semi-transparent purple wash over the core."""
        if reactor.stage not in (Stage.XENON_POISON, Stage.ROD_WITHDRAW):
            return
        total_xe = sum(cell.xenon for row in reactor.fuel for cell in row)
        avg_xe   = total_xe / (COLS * ROWS)
        if avg_xe < 0.05:
            return
        xesurf = pygame.Surface((CORE_W, CORE_H), pygame.SRCALPHA)
        xesurf.fill((80, 0, 160, int(avg_xe * 60)))
        self.surf.blit(xesurf, (CORE_X, CORE_Y))


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    pygame.init()
    pygame.display.set_caption("Chernobyl Reactor No.4 — Nuclear Physics Simulation")

    screen = pygame.display.set_mode((W, H))
    clock  = pygame.time.Clock()

    reactor  = Reactor()
    renderer = Renderer(screen)

    stage_list = list(Stage)
    stage_idx  = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_SPACE):
                    stage_idx = min(len(stage_list)-1, stage_idx+1)
                    reactor.set_stage(stage_list[stage_idx])
                elif event.key == pygame.K_LEFT:
                    stage_idx = max(0, stage_idx-1)
                    reactor.set_stage(stage_list[stage_idx])
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_1, pygame.K_KP1): stage_idx=0; reactor.set_stage(stage_list[0])
                elif event.key in (pygame.K_2, pygame.K_KP2): stage_idx=1; reactor.set_stage(stage_list[1])
                elif event.key in (pygame.K_3, pygame.K_KP3): stage_idx=2; reactor.set_stage(stage_list[2])
                elif event.key in (pygame.K_4, pygame.K_KP4): stage_idx=3; reactor.set_stage(stage_list[3])
                elif event.key in (pygame.K_5, pygame.K_KP5): stage_idx=4; reactor.set_stage(stage_list[4])
                elif event.key in (pygame.K_6, pygame.K_KP6): stage_idx=5; reactor.set_stage(stage_list[5])
                elif event.key in (pygame.K_7, pygame.K_KP7): stage_idx=6; reactor.set_stage(stage_list[6])
                elif event.key in (pygame.K_8, pygame.K_KP8): stage_idx=7; reactor.set_stage(stage_list[7])

        reactor.update()

        # Screen shake offset
        ox, oy = 0, 0
        if reactor.shake > 0:
            ox = random.randint(-5, 5)
            oy = random.randint(-4, 4)

        draw_surf = screen
        if reactor.shake > 0:
            draw_surf = pygame.Surface((W, H))
            draw_surf.fill(C_BG)
        else:
            screen.fill(C_BG)

        renderer.surf = draw_surf
        renderer.draw_core_grid(reactor)
        renderer.draw_xenon_cloud(reactor)
        renderer.draw_particles(reactor)
        renderer.draw_explosion_overlay(reactor)
        renderer.draw_panel(reactor, stage_idx)
        renderer.draw_hud(reactor)

        if reactor.shake > 0:
            screen.blit(draw_surf, (ox, oy))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()