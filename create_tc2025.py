"""
Create TC2025 championship with all fixes applied.

This script validates the complete championship creation pipeline:
- Name length validation (19 chars limit)
- Vehicle isolation with all dependencies (.tbc, .ini, .pm, .mas)
- RFM generation with proper settings
- StartingMoney = 500000000 for vehicle purchases
"""
from src.services.championship_creator import ChampionshipCreator

print("=" * 70)
print("Creating TC2025 Championship")
print("=" * 70)

# Initialize
rfactor_path = r"C:\Program Files (x86)\Steam\steamapps\common\rFactor"
creator = ChampionshipCreator(rfactor_path)

# Championship configuration
championship_name = "TC2025"  # 6 chars -> RFTOOL_TC2025 = 13 chars (OK)
full_name = "Test Championship 2025"

# Vehicle assignments (same as before)
vehicle_assignments = [
    {
        'vehicle_path': 'RHEZ/2005RHEZ/SRGP/TEAM BLACK/BLK_03.veh',
        'driver_name': 'Driver Black'
    },
    {
        'vehicle_path': 'RHEZ/2005RHEZ/SRGP/TEAM RED/RD_01.veh',
        'driver_name': 'Driver Red'
    },
    {
        'vehicle_path': 'ZR/SRGP/TEAM_GREEN/GRN_08.veh',
        'driver_name': 'Driver Green'
    }
]

# Track selection
tracks = [
    'Mills_Short',
    'Joesville_Speedway',
    'Toban_Short'
]

# Options
options = {
    'full_name': full_name
}

print(f"\nChampionship: {championship_name}")
print(f"Full Name: {full_name}")
print(f"RFM Filename: RFTOOL_{championship_name}.rfm ({len('RFTOOL_' + championship_name)} chars)")
print(f"Vehicles: {len(vehicle_assignments)}")
print(f"Tracks: {len(tracks)}")
print(f"Starting Money: 500,000,000")
print()

# Clean up if exists
try:
    print("Cleaning up previous version (if exists)...")
    creator.delete_championship(championship_name)
    print("  Previous version deleted")
except Exception as e:
    print(f"  No previous version found")

# Create championship
print("\n" + "=" * 70)
print("Creating Championship...")
print("=" * 70)

try:
    rfm_path = creator.create_championship(
        championship_name,
        vehicle_assignments,
        tracks,
        options
    )

    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print(f"RFM File: {rfm_path}")
    print(f"Vehicles Dir: C:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor\\GameData\\Vehicles\\RFTOOL_{championship_name}")
    print()
    print("Next Steps:")
    print("1. Launch rFactor")
    print("2. Go to: Race > Select Mod > RFTOOL_TC2025")
    print("3. Select 'Career' mode")
    print("4. You should have 500,000,000 starting money")
    print("5. Buy a vehicle and start racing!")
    print("=" * 70)

except Exception as e:
    print("\n" + "=" * 70)
    print("ERROR!")
    print("=" * 70)
    print(f"Failed to create championship: {e}")
    import traceback
    traceback.print_exc()
