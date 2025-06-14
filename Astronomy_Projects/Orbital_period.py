import math
import time

# Dictionary of planets and their average distance from the Sun (in AU)
planet_distances = {
    "Mercury": 0.39,
    "Venus": 0.72,
    "Earth": 1.00,
    "Mars": 1.52,
    "Jupiter": 5.20,
    "Saturn": 9.58,
    "Uranus": 19.2,
    "Neptune": 30.1
}

try:
    while True:
        print("Orbital Period of Planets Around the Sun:\n")
        for planet, R in planet_distances.items():
            T = math.sqrt(R ** 3)
            print(f"{planet}: {T:.2f} Earth years")
        print("\nPress Ctrl + C to exit or wait 20 seconds to see again...\n")
        time.sleep(20)

except KeyboardInterrupt:
    print("\nGoodbye! Program terminated by user.")
