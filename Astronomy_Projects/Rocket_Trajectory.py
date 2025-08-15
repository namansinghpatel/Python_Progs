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
RED = (255, 0, 0)
GRAVITY = 9.81
SCALE = 1.5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Trajectory - Custom Launch")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 50)

# ==== MENU LOOP ====
def menu_screen():
    while True:
        screen.fill(BLACK)
        title = big_font.render("Rocket Launch Simulator", True, WHITE)
        opt1 = font.render("Press ENTER to launch with default values", True, WHITE)
        opt2 = font.render("Press C to enter custom values", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        screen.blit(opt1, (WIDTH//2 - opt1.get_width()//2, 300))
        screen.blit(opt2, (WIDTH//2 - opt2.get_width()//2, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Default
                    return DEFAULTS['thrust'], DEFAULTS['mass'], DEFAULTS['burn_time'], DEFAULTS['landing_burn_time'], DEFAULTS['landing_trigger_height']
                elif event.key == pygame.K_c:  # Custom
                    pygame.display.iconify()  # Minimize window for input
                    return get_user_inputs()

# ==== TRAJECTORY PREDICTION ====
def predict_trajectory(thrust, mass, burn_time, landing_burn_time, landing_trigger_height, launch_angle):
    angle_rad = math.radians(launch_angle)
    temp_x, temp_y = 100, 0
    temp_vx, temp_vy = 0, 0
    prediction = []
    sim_time = 0
    dt = 0.05
    landing_started = False
    landing_thrust = thrust / 2

    while temp_y >= 0 and sim_time < 300:
        if sim_time <= burn_time:
            acceleration = thrust / mass
            acc_x = acceleration * math.cos(angle_rad)
            acc_y = acceleration * math.sin(angle_rad) - GRAVITY
        elif temp_y <= landing_trigger_height and not landing_started:
            landing_started = True
            landing_time = 0
            acc_x = (landing_thrust / mass) * math.cos(angle_rad)
            acc_y = (landing_thrust / mass) * math.sin(angle_rad) - GRAVITY
        elif landing_started and landing_time < landing_burn_time:
            landing_time += dt
            acc_x = (landing_thrust / mass) * math.cos(angle_rad)
            acc_y = (landing_thrust / mass) * math.sin(angle_rad) - GRAVITY
        else:
            acc_x = 0
            acc_y = -GRAVITY

        temp_vx += acc_x * dt
        temp_vy += acc_y * dt
        temp_x += temp_vx * dt
        temp_y += temp_vy * dt
        prediction.append((int(temp_x * SCALE), HEIGHT - int(temp_y * SCALE)))
        sim_time += dt
    return prediction

# ==== MAIN GAME ====
def run_game(thrust, mass, burn_time, landing_burn_time, landing_trigger_height, launch_angle):
    angle_rad = math.radians(launch_angle)
    pos_x, pos_y = 100, 0
    vel_x, vel_y = 0, 0
    time_elapsed = 0
    landing_time_elapsed = 0
    landing_started = False
    landing_thrust = thrust / 2
    path = []
    predicted_path = predict_trajectory(thrust, mass, burn_time, landing_burn_time, landing_trigger_height, launch_angle)

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time_elapsed += dt

        if time_elapsed <= burn_time:
            acceleration = thrust / mass
            acc_x = acceleration * math.cos(angle_rad)
            acc_y = acceleration * math.sin(angle_rad) - GRAVITY
        elif pos_y <= landing_trigger_height and not landing_started:
            landing_started = True
            landing_time_elapsed = 0
            acceleration = landing_thrust / mass
            acc_x = acceleration * math.cos(angle_rad)
            acc_y = acceleration * math.sin(angle_rad) - GRAVITY
        elif landing_started and landing_time_elapsed < landing_burn_time:
            landing_time_elapsed += dt
            acceleration = landing_thrust / mass
            acc_x = acceleration * math.cos(angle_rad)
            acc_y = acceleration * math.sin(angle_rad) - GRAVITY
        else:
            acc_x = 0
            acc_y = -GRAVITY

        vel_x += acc_x * dt
        vel_y += acc_y * dt
        pos_x += vel_x * dt
        pos_y += vel_y * dt

        if pos_y < 0:
            pos_y = 0
            vel_x = vel_y = 0

        path.append((int(pos_x * SCALE), HEIGHT - int(pos_y * SCALE)))

        screen.fill(BLACK)
        for p in predicted_path:
            pygame.draw.circle(screen, GRAY, p, 2)
        for p in path:
            pygame.draw.circle(screen, WHITE, p, 2)
        pygame.draw.rect(screen, RED, (int(pos_x * SCALE) - 5, HEIGHT - int(pos_y * SCALE) - 20, 10, 20))

        alt_text = font.render(f"Altitude: {pos_y:.1f} m", True, WHITE)
        dist_text = font.render(f"Distance: {pos_x - 100:.1f} m", True, WHITE)
        vel_text = font.render(f"Velocity: {math.sqrt(vel_x**2 + vel_y**2):.1f} m/s", True, WHITE)
        screen.blit(alt_text, (10, 10))
        screen.blit(dist_text, (10, 40))
        screen.blit(vel_text, (10, 70))

        pygame.display.flip()

    pygame.quit()

# ==== START ====
params = menu_screen()
run_game(*params, DEFAULTS['launch_angle'])


