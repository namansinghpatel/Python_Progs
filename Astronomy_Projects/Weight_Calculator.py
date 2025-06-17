# Planet gravity in m/s²
import time

planet_gravity = {
    "Mercury": 3.7,
    "Venus": 8.87,
    "Earth": 9.8,
    "Mars": 3.71,
    "Jupiter": 24.8,
    "Saturn": 10.44,
    "Uranus": 8.69,
    "Neptune": 11.15,
    "Pluto": 0.62,
}

try:
    while True:
        weight_earth = float(input("\nEnter your weight on Earth (kg): "))
        for planet, gravity in planet_gravity.items():
            weight_on_planet = weight_earth * gravity / planet_gravity["Earth"]
            print(f"Your weight on {planet}: {weight_on_planet:.2f} kg")
        print("Press Ctrl + C to exit or try again with another weight.\n")

except KeyboardInterrupt:
    print("\nGoodbye! Program terminated by user.")
