try:
    while True:
        mass = float(input("Enter mass of the asteroid (in kg, e.g. 1e9): "))
        velocity = float(input("Enter velocity of the asteroid (in m/s, e.g. 25000): "))

        # Calculate energy using the formula E = 0.5 * m * v^2
        energy = 0.5 * mass * velocity**2

        # Convert to megatons of TNT (optional)
        # 1 Megaton TNT = 4.184e15 Joules
        energy_megatons = energy / 4.184e15

        print(f"\nImpact Energy = {energy:.3e} Joules")
        print(f"Equivalent to ≈ {energy_megatons:.2f} megatons of TNT")
        print("Press Ctrl + C to exit or try again with new values.\n")

except KeyboardInterrupt:
    print("\nGoodbye! Program terminated by user.")
