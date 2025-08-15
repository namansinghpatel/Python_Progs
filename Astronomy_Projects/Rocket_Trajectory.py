import pygame
import math

# ==== DEFAULT VALUES ====
DEFAULTS = {
    "thrust": 3000,                 # N
    "mass": 500,                    # kg
    "burn_time": 5,                  # s
    "landing_burn_time": 4,          # s
    "landing_trigger_height": 50,    # m
    "launch_angle": 85               # degrees
}

# ==== GET USER VALUES ====
def get_user_inputs():
    thrust = float(input(f"Enter launch thrust (N) [{DEFAULTS['thrust']}]: ") or DEFAULTS['thrust'])
    mass = float(input(f"Enter rocket mass (kg) [{DEFAULTS['mass']}]: ") or DEFAULTS['mass'])
    burn_time = float(input(f"Enter ascent burn time (seconds) [{DEFAULTS['burn_time']}]: ") or DEFAULTS['burn_time'])
    landing_burn_time = float(input(f"Enter landing burn duration (seconds) [{DEFAULTS['landing_burn_time']}]: ") or DEFAULTS['landing_burn_time'])
    landing_trigger_height = float(input(f"Enter landing trigger height (m) [{DEFAULTS['landing_trigger_height']}]: ") or DEFAULTS['landing_trigger_height'])
    return thrust, mass, burn_time, landing_burn_time, landing_trigger_height

# ==== CONSTANTS ====
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
RED   = (255, 80, 80)
GREEN = (120, 220, 120)
YELLOW= (240, 220, 60)
GRAY  = (160, 160, 160)

# --- Physics ---
GRAVITY = 9.81     # m/s^2 downward
SCALE   = 2.0      # pixels per meter

# === Ask player for rocket parameters before launch ===
mass = float(input("Enter rocket mass (kg): "))
max_thrust = float(input("Enter maximum thrust (N): "))
burn_time_ascent = float(input("Enter ascent burn time (seconds): "))
burn_time_landing = float(input("Enter landing burn time (seconds): "))
flare_alt = float(input("Enter landing trigger altitude (m): "))

launch_angle_deg = 88  # stays constant

# Controls for landing autopilot
K_vy   = 0.35  # vertical damping
K_vx   = 0.15  # horizontal damping
soft_land_vy = 2.0   # m/s vertical speed threshold for "soft"
soft_land_vx = 2.0   # m/s horizontal threshold for "soft"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Trajectory - Custom Launch")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# Initial state (ground at y=0)
x = 120.0   # m
y = 0.0     # m altitude
vx = 0.0
vy = 0.0

# Fuel "seconds" pool (simple model proportional to throttle usage)
fuel_ascent  = burn_time_ascent
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
    a_req_mag = math.sqrt(ax_req*ax_req + ay_req*ay_req)
    a_max = max_thrust / mass

    if a_req_mag <= 1e-6 or not thrust_available():
        return 0.0, 0.0

    # Cap to engine capability
    scale = min(1.0, a_max / a_req_mag)
    ax = ax_req * scale
    ay = ay_req * scale

    # Consume fuel seconds by throttle usage (scale ~ throttle)
    use = dt * abs(scale)  # proportional to throttle
    if use_landing:
        take = min(use, fuel_landing)
        fuel_landing -= take
        if take < use and fuel_ascent > 0.0:
            fuel_ascent = max(0.0, fuel_ascent - (use - take))
    else:
        take = min(use, fuel_ascent)
        fuel_ascent -= take
        if take < use and fuel_landing > 0.0:
            fuel_landing = max(0.0, fuel_landing - (use - take))

    return ax, ay

while running:
    dt = clock.tick(60) / 1000.0  # seconds/frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    if not (landed or crashed):
        ax = 0.0
        ay = -GRAVITY

        if fuel_ascent > 0.0:
            status_msg = "ASCENT"
            a_engine = (max_thrust / mass)
            ax_req = a_engine * math.cos(angle)
            ay_req = a_engine * math.sin(angle)
            thx, thy = apply_thrust(ax_req, ay_req, dt, use_landing=False)
            ax += thx
            ay += thy
        else:
            descending = vy < 0.0
            if y <= flare_alt and descending:
                status_msg = "AUTO-LAND"
                ay_req = (K_vy * abs(vy)) + GRAVITY
                ax_req = -K_vx * vx
                thx, thy = apply_thrust(ax_req, ay_req, dt, use_landing=True)
                ax += thx
                ay += thy
            else:
                status_msg = "COAST"

        vx += ax * dt
        vy += ay * dt
        x  += vx * dt
        y  += vy * dt

        if y <= 0.0:
            y = 0.0
            if abs(vy) <= soft_land_vy and abs(vx) <= soft_land_vx:
                landed = True
                status_msg = "LANDED (soft)"
            else:
                crashed = True
                status_msg = "CRASHED"
            vx = vy = 0.0

        path.append((int(pos_x * SCALE), HEIGHT - int(pos_y * SCALE)))

    # --- Draw ---
    screen.fill(BLACK)

    pygame.draw.line(screen, GRAY, (0, HEIGHT), (WIDTH, HEIGHT), 2)

    for p in path[-2000:]:
        if 0 <= p[0] < WIDTH and 0 <= p[1] < HEIGHT:
            pygame.draw.circle(screen, WHITE, p, 1)

    rx = int(x * SCALE)
    ry = HEIGHT - int(y * SCALE)
    pygame.draw.rect(screen, RED if not landed else GREEN, (rx - 6, ry - 24, 12, 24))

    if status_msg in ("ASCENT", "AUTO-LAND") and thrust_available():
        pygame.draw.polygon(screen, YELLOW, [(rx, ry),
                                             (rx - 4, ry + 16),
                                             (rx + 4, ry + 16)])

    def txt(t, yoff):
        screen.blit(font.render(t, True, WHITE), (10, yoff))

    speed = math.hypot(vx, vy)
    txt(f"Mode: {status_msg}", 10)
    txt(f"Altitude: {y:7.2f} m", 40)
    txt(f"Speed:    {speed:7.2f} m/s (vx={vx:+.2f}, vy={vy:+.2f})", 70)
    txt(f"Ascent fuel:  {max(0.0, fuel_ascent):.2f}s   Landing fuel: {max(0.0, fuel_landing):.2f}s", 100)
    txt(f"Angle: {launch_angle_deg}°   g: {GRAVITY} m/s²   Scale: {SCALE} px/m", 130)

    if crashed:
        screen.blit(font.render("CRASHED – try more landing fuel or higher K_vy.", True, RED), (10, 170))
    elif landed:
        screen.blit(font.render("LANDED SOFT – nice!", True, GREEN), (10, 170))

        pygame.display.flip()

pygame.quit()

# ==== START ====
params = menu_screen()
run_game(*params, DEFAULTS['launch_angle'])


