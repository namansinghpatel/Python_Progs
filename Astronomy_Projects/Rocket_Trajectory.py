import pygame
import math

# --- Window & colors ---
WIDTH, HEIGHT = 900, 620
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 80, 80)
GREEN = (120, 220, 120)
YELLOW= (240, 220, 60)
GRAY  = (160, 160, 160)

# --- Physics ---
GRAVITY = 9.81     # m/s^2 downward
SCALE   = 2.0      # pixels per meter

# === Ask player for rocket parameters before launch ===
mass = float(input("Enter rocket mass (kg) [400]: ") or 400)
max_thrust = float(input("Enter maximum thrust (N) [20000]: ") or 20000)
burn_time_ascent = float(input("Enter ascent burn time (seconds) [3]: ") or 3)
burn_time_landing = float(input("Enter landing burn time (seconds) [20]: ") or 20)
flare_alt = float(input("Enter landing trigger altitude (m) [310]: ") or 310)

print(f"[DEBUG] Parameters set: mass={mass}, max_thrust={max_thrust}, "
      f"burn_time_ascent={burn_time_ascent}, burn_time_landing={burn_time_landing}, flare_alt={flare_alt}")

launch_angle_deg = 88  # stays constant

# Controls for landing autopilot
K_vy   = 0.35  # vertical damping
K_vx   = 0.15  # horizontal damping
soft_land_vy = 5   # m/s
soft_land_vx = 5   # m/s

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Auto-Lander: Retro-Thrust Smooth Landing (85°)")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# Initial state
x, y = 120.0, 0.0
vx, vy = 0.0, 0.0
fuel_ascent  = burn_time_ascent
fuel_landing = burn_time_landing
angle = math.radians(launch_angle_deg)
path = []
running = True
landed = False
crashed = False
status_msg = "ASCENT"

def thrust_available():
    available = (fuel_ascent > 0.0) or (fuel_landing > 0.0)
    print(f"[DEBUG] Thrust available: {available}")
    return available

def apply_thrust(ax_req, ay_req, dt, use_landing=False):
    global fuel_ascent, fuel_landing

    print(f"[DEBUG] Requested thrust: ax_req={ax_req:.3f}, ay_req={ay_req:.3f}, dt={dt:.3f}, use_landing={use_landing}")
    a_req_mag = math.sqrt(ax_req**2 + ay_req**2)
    a_max = max_thrust / mass

    if a_req_mag <= 1e-6 or not thrust_available():
        return 0.0, 0.0

    scale = min(1.0, a_max / a_req_mag)
    ax, ay = ax_req * scale, ay_req * scale
    print(f"[DEBUG] Applied thrust: ax={ax:.3f}, ay={ay:.3f}, scale={scale:.3f}")

    use = dt * abs(scale)
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

    print(f"[DEBUG] Fuel after thrust: ascent={fuel_ascent:.2f}, landing={fuel_landing:.2f}")
    return ax, ay

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not (landed or crashed):
        ax, ay = 0.0, -GRAVITY

        if fuel_ascent > 0.0:
            status_msg = "ASCENT"
            a_engine = max_thrust / mass
            ax_req = a_engine * math.cos(angle)
            ay_req = a_engine * math.sin(angle)
            print(f"[DEBUG] ASCENT phase: ax_req={ax_req:.3f}, ay_req={ay_req:.3f}")
            thx, thy = apply_thrust(ax_req, ay_req, dt, use_landing=False)
            ax += thx
            ay += thy
        else:
            descending = vy < 0.0
            if y <= flare_alt and descending:
                status_msg = "AUTO-LAND"
                ay_req = (K_vy * abs(vy)) + GRAVITY
                ax_req = -K_vx * vx
                print(f"[DEBUG] AUTO-LAND phase: ax_req={ax_req:.3f}, ay_req={ay_req:.3f}")
                thx, thy = apply_thrust(ax_req, ay_req, dt, use_landing=True)
                ax += thx
                ay += thy
            else:
                status_msg = "COAST"

        vx += ax * dt
        vy += ay * dt
        x  += vx * dt
        y  += vy * dt
        print(f"[DEBUG] Position updated: x={x:.2f}, y={y:.2f}, vx={vx:.2f}, vy={vy:.2f}")

        if y <= 0.0:
            y = 0.0
            if abs(vy) <= soft_land_vy and abs(vx) <= soft_land_vx:
                landed = True
                status_msg = "LANDED (soft)"
                print("[DEBUG] LANDING SUCCESSFUL: Soft landing achieved")
            else:
                crashed = True
                status_msg = "CRASHED"
                print("[DEBUG] CRASH DETECTED: Impact velocity too high")
            vx = vy = 0.0

        path.append((int(x * SCALE), HEIGHT - int(y * SCALE)))

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


