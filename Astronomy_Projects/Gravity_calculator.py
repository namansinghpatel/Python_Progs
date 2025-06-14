import time

G = 6.674e-11  # in N·m²/kg²

try:
    while True:
        mass1 = float(input("Enter mass of first object (kg): "))  # e.g., 5.972e24 (Earth)
        mass2 = float(input("Enter mass of second object (kg): "))  # e.g., 7.348e22 (Moon)
        distance = float(input("Enter distance between objects (meters): "))  # e.g., 3.844e8

        force = G * (mass1 * mass2) / (distance ** 2)
        print(f"\nGravitational Force = {force:.3e} Newtons")
        print("Press Ctrl + C to exit or try again.\n")
        time.sleep(20)

except KeyboardInterrupt:
    print("\nGoodbye! Program terminated by user.")
