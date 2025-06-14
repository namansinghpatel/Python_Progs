import time

LIGHT_YEAR_KM = 9.461e12
KM_TO_METERS = 1000  

star_distances_ly = {
    "Alpha Centauri": 4.367,
    "Sirius": 8.6,
    "Betelgeuse": 642.5,
    "Vega": 25.0,
    "Proxima Centauri": 4.24
}

try:
    while True:
        print("Distance from Earth to some stars:\n")
        for star, ly in star_distances_ly.items():
            distance_km = ly * LIGHT_YEAR_KM
            distance_m = distance_km * KM_TO_METERS
            print(f"{star}:")
            print(f"  {ly} light-years")
            print(f"  {distance_km:.3e} kilometers")
            print(f"  {distance_m:.3e} meters\n")
        print("Press Ctrl + C to exit or wait 20 seconds to see again...\n")
        time.sleep(20)

except KeyboardInterrupt:
    print("\nGoodbye! Program terminated by user.")
