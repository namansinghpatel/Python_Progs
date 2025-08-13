import pygame
import math

# --- Window & colors ---
WIDTH, HEIGHT = 1200, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
GREEN = (120, 220, 120)
YELLOW = (240, 220, 60)
GRAY = (160, 160, 160)

# --- Physics ---
GRAVITY = 9.81  # m/s^2 downward
SCALE = 2.0  # pixels per meter

# --- Rocket params ---
mass = 500  # kg
max_thrust = 22000.0  # N (main engine)
burn_time_ascent = 4.0  # s of thrust for ascent
burn_time_landing = 30  # s of thrust reserved for landing/retro
launch_angle_deg = 88  # degrees from horizontal

# Controls for landing autopilot
K_vy = 0.35  # vertical damping (larger => stronger braking)
K_vx = 0.15  # horizontal damping (reduce sideways drift)
soft_land_vy = 5  # m/s vertical speed threshold for "soft"
soft_land_vx = 5  # m/s horizontal threshold for "soft"
flare_alt = 380  # m: start active landing control below this altitude

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Auto-Lander: Retro-Thrust Smooth Landing (85°)")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# Initial state (ground at y=0)
x = 120.0  # m
y = 0.0  # m altitude
vx = 0.0
vy = 0.0

# Fuel "seconds" pool (simple model proportional to throttle usage)
fuel_ascent = burn_time_ascent
fuel_landing = burn_time_landing

angle = math.radians(launch_angle_deg)

path = []
running = True
landed = False
crashed = False
status_msg = "ASCENT"


def thrust_available():
    return (fuel_ascent > 0.0) or (fuel_landing > 0.0)


def apply_thrust(ax_req, ay_req, dt, use_landing=False):
    """
    Apply thrust to approximate requested accelerations (limited by engine).
    Consumes fuel bucket (ascent or landing) proportionally to throttle.
    Returns actual ax, ay applied.
    """
    global fuel_ascent, fuel_landing

    # Required total acceleration due to engine (vector magnitude)
    a_req_mag = math.sqrt(ax_req * ax_req + ay_req * ay_req)
    a_max = max_thrust / mass

    if a_req_mag <= 1e-6 or not thrust_available():
        return 0.0, 0.0

    # Cap to engine capability
    scale = min(1.0, a_max / a_req_mag)
    ax = ax_req * scale
    ay = ay_req * scale

    # Consume fuel seconds by throttle usage (scale ~ throttle)
    use = dt * (abs(scale))  # simple proportional model
    if use_landing:
        take = min(use, fuel_landing)
        fuel_landing -= take
        # If landing bucket empty, try ascent if any leftover
        if take < use and fuel_ascent > 0.0:
            fuel_ascent = max(0.0, fuel_ascent - (use - take))
    else:
        take = min(use, fuel_ascent)
        fuel_ascent -= take
        # If ascent bucket empty, try landing if any leftover
        if take < use and fuel_landing > 0.0:
            fuel_landing = max(0.0, fuel_landing - (use - take))

    return ax, ay


while running:
    dt = clock.tick(60) / 1000.0  # seconds/frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not (landed or crashed):
        # --- Default accelerations: gravity only ---
        ax = 0.0
        ay = -GRAVITY

        # --- Phase logic ---
        if fuel_ascent > 0.0:
            # ASCENT PHASE: thrust along launch angle
            status_msg = "ASCENT"
            a_engine = max_thrust / mass  # we'll cap with apply_thrust anyway
            ax_req = a_engine * math.cos(angle)
            ay_req = a_engine * math.sin(angle)
            thx, thy = apply_thrust(ax_req, ay_req, dt, use_landing=False)
            ax += thx
            ay += thy
        else:
            # POST-ASCENT (coast/descend). If descending and low altitude, auto land.
            descending = vy < 0.0
            if y <= flare_alt and descending:
                status_msg = "AUTO-LAND"
                # Target: reduce vertical speed to small value as approaching ground
                # Simple proportional braking: request upward accel to kill vy
                # Also ensure we at least counter gravity
                ay_req = (K_vy * abs(vy)) + GRAVITY

                # Small sideways damping to reduce horizontal drift
                ax_req = -K_vx * vx

                # Use landing fuel bucket
                thx, thy = apply_thrust(ax_req, ay_req, dt, use_landing=True)
                ax += thx
                ay += thy
            else:
                status_msg = "COAST"

        # Integrate motion
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        # Ground interaction
        if y <= 0.0:
            y = 0.0
            # Touchdown condition
            if abs(vy) <= soft_land_vy and abs(vx) <= soft_land_vx:
                landed = True
                status_msg = "LANDED (soft)"
                vx = vy = 0.0
            else:
                crashed = True
                status_msg = "CRASHED"
                vx = vy = 0.0

        # Keep path
        path.append((int(x * SCALE), HEIGHT - int(y * SCALE)))

    # --- Draw ---
    screen.fill(BLACK)

    # Ground line
    pygame.draw.line(
        screen, GRAY, (0, HEIGHT - int(0 * SCALE)), (WIDTH, HEIGHT - int(0 * SCALE)), 2
    )

    # Trajectory
    for p in path[-2000:]:
        if 0 <= p[0] < WIDTH and 0 <= p[1] < HEIGHT:
            pygame.draw.circle(screen, WHITE, p, 1)

    # Rocket (simple rectangle)
    rx = int(x * SCALE)
    ry = HEIGHT - int(y * SCALE)
    pygame.draw.rect(screen, RED if not landed else GREEN, (rx - 6, ry - 24, 12, 24))

    # Flame hint if thrusting this frame (approx by status & fuel movement)
    if status_msg in ("ASCENT", "AUTO-LAND") and thrust_available():
        pygame.draw.polygon(
            screen, YELLOW, [(rx, ry), (rx - 4, ry + 16), (rx + 4, ry + 16)]
        )

    # HUD
    def txt(t, yoff):
        screen.blit(font.render(t, True, WHITE), (10, yoff))

    speed = math.hypot(vx, vy)
    txt(f"Mode: {status_msg}", 10)
    txt(f"Altitude: {y:7.2f} m", 40)
    txt(f"Speed:    {speed:7.2f} m/s (vx={vx:+.2f}, vy={vy:+.2f})", 70)
    txt(
        f"Ascent fuel:  {max(0.0, fuel_ascent):.2f}s   Landing fuel: {max(0.0, fuel_landing):.2f}s",
        100,
    )
    txt(f"Angle: {launch_angle_deg}°   g: {GRAVITY} m/s²   Scale: {SCALE} px/m", 130)

    if crashed:
        screen.blit(
            font.render("CRASHED – try more landing fuel or higher K_vy.", True, RED),
            (10, 170),
        )
    elif landed:
        screen.blit(font.render("LANDED SOFT – nice!", True, GREEN), (10, 170))

    pygame.display.flip()

pygame.quit()
