"""
Script to clean up and recreate Test Championship with StartingVehicle patch
"""
import sys
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.championship_creator import ChampionshipCreator
from src.models.rfm import CareerSettings

# Patch the _create_rfm method to add starting_vehicles
original_create_rfm = ChampionshipCreator._create_rfm

def patched_create_rfm(self, championship_name, tracks, num_or_paths, options):
    """Patched version that extracts vehicle names from paths."""

    # Check if num_or_paths is a list of paths or just a number
    if isinstance(num_or_paths, list):
        # It's a list of paths - extract vehicle names
        isolated_paths = num_or_paths
        num_vehicles = len(isolated_paths)

        # Extract vehicle names for StartingVehicle
        starting_vehicles = []
        for veh_path in isolated_paths:
            veh_file = Path(veh_path).stem
            starting_vehicles.append(veh_file.lower())

        print(f"  [PATCH] Extracted {len(starting_vehicles)} vehicle names for StartingVehicle:")
        for veh in starting_vehicles:
            print(f"    - {veh}")
    else:
        # It's just a number (old behavior)
        num_vehicles = num_or_paths
        starting_vehicles = []
        print(f"  [PATCH] No vehicle paths provided, StartingVehicle list will be empty")

    # Create vehicle filter
    vehicle_filter = championship_name
    max_opponents = num_vehicles - 1
    if max_opponents < 1:
        max_opponents = 1

    full_name = options.get('full_name', championship_name)

    # Create career settings with starting vehicles
    career_settings = CareerSettings(starting_vehicles=starting_vehicles)

    # Import necessary models
    from src.models.rfm import RFMod, Season, PitGroup

    # Create RFMod with career settings
    rfm = RFMod(
        mod_name=full_name,
        vehicle_filter=vehicle_filter,
        track_filter="*",
        max_opponents=max_opponents,
        min_championship_opponents=min(3, max_opponents),
        career_settings=career_settings
    )

    # Create season
    season = Season(
        name=f"{full_name} Season",
        vehicle_filter=vehicle_filter,
        scene_order=tracks,
        min_championship_opponents=min(3, max_opponents)
    )
    rfm.add_season(season)

    # Set scoring if provided
    if 'default_scoring' in options:
        rfm.default_scoring = options['default_scoring']
    if 'season_scoring' in options:
        rfm.season_scoring_info = options['season_scoring']

    # Set pit groups if provided
    if 'pit_groups' in options:
        rfm.pit_group_order = options['pit_groups']
    else:
        # Generate default pit groups
        pit_groups = []
        for i in range(num_vehicles):
            pit_groups.append(PitGroup(1, f"Group{i + 1}"))
        rfm.pit_group_order = pit_groups

    # Set scene order
    rfm.scene_order = tracks

    return rfm

# Apply the patch
ChampionshipCreator._create_rfm = patched_create_rfm

# Configuration
RFACTOR_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\rFactor"
CHAMPIONSHIP_NAME = "TestChampionship2025"

def cleanup_old_championship():
    """Delete all files related to old championship."""
    print(f"\n=== Cleaning up old championship '{CHAMPIONSHIP_NAME}' ===\n")

    # 1. Delete vehicles folder
    vehicles_folder = Path(RFACTOR_PATH) / "GameData" / "Vehicles" / f"RFTOOL_{CHAMPIONSHIP_NAME}"
    if vehicles_folder.exists():
        print(f"Deleting vehicles folder: {vehicles_folder}")
        shutil.rmtree(vehicles_folder)
        print("  [OK] Deleted\n")
    else:
        print(f"Vehicles folder not found (already deleted?): {vehicles_folder}\n")

    # 2. Delete RFM file
    rfm_file = Path(RFACTOR_PATH) / "rFm" / f"RFTOOL_{CHAMPIONSHIP_NAME}.rfm"
    if rfm_file.exists():
        print(f"Deleting RFM file: {rfm_file}")
        rfm_file.unlink()
        print("  [OK] Deleted\n")
    else:
        print(f"RFM file not found (already deleted?): {rfm_file}\n")

    # 3. Delete RFM backup if exists
    rfm_bak = Path(RFACTOR_PATH) / "rFm" / f"RFTOOL_{CHAMPIONSHIP_NAME}.rfm_bak"
    if rfm_bak.exists():
        print(f"Deleting RFM backup: {rfm_bak}")
        rfm_bak.unlink()
        print("  [OK] Deleted\n")

    # 4. Delete CCH file (player progress)
    userdata_folder = Path(RFACTOR_PATH) / "UserData"
    for player_folder in userdata_folder.glob("*"):
        if player_folder.is_dir():
            cch_file = player_folder / f"RFTOOL_{CHAMPIONSHIP_NAME}.cch"
            if cch_file.exists():
                print(f"Deleting CCH file: {cch_file}")
                cch_file.unlink()
                print("  [OK] Deleted\n")

    print("=== Cleanup complete ===\n")

def create_new_championship():
    """Create a fresh championship."""
    print(f"\n=== Creating new championship '{CHAMPIONSHIP_NAME}' ===\n")

    # Initialize creator (with patched method)
    creator = ChampionshipCreator(RFACTOR_PATH)

    # Define vehicles (3 vehicles as requested)
    vehicle_assignments = [
        {'vehicle_path': 'ZR/SRGP/Team_Green/GRN_08.veh', 'driver_name': 'John Doe'},
        {'vehicle_path': 'Rhez/2005Rhez/SRGP/Team Red/Rd_01.veh', 'driver_name': 'Jane Smith'},
        {'vehicle_path': 'Rhez/2005Rhez/SRGP/Team Black/BLK_03.veh', 'driver_name': 'Bob Johnson'},
    ]

    # Define tracks
    tracks = [
        'Mills_Short',
        'Joesville_Speedway',
        'Toban_Short',
    ]

    # Create championship
    try:
        rfm_path = creator.create_championship(
            championship_name=CHAMPIONSHIP_NAME,
            vehicle_assignments=vehicle_assignments,
            tracks=tracks,
            options={'full_name': 'Test Championship 2025'}
        )
        print(f"\n[SUCCESS] Championship created: {rfm_path}\n")

        # Verify starting vehicles were added
        print("=== Verifying RFM content ===")
        with open(rfm_path, 'r', encoding='windows-1252') as f:
            content = f.read()
            if 'StartingVehicle' in content:
                print("  [OK] StartingVehicle parameters found in RFM")
                # Show the lines
                for line in content.split('\n'):
                    if 'StartingVehicle' in line:
                        print(f"    {line}")
            else:
                print("  [WARNING] StartingVehicle NOT found in RFM!")

        # Verify isolated vehicles
        print("\n=== Verifying isolated vehicles ===")
        vehicles_folder = Path(RFACTOR_PATH) / "GameData" / "Vehicles" / f"RFTOOL_{CHAMPIONSHIP_NAME}"
        veh_files = list(vehicles_folder.glob("**/*.veh"))
        print(f"  Found {len(veh_files)} .veh files:")
        for veh in veh_files:
            print(f"    - {veh.name}")

        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to create championship: {e}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CLEANUP AND RECREATE TEST CHAMPIONSHIP (WITH PATCH)")
    print("=" * 60)

    # Step 1: Cleanup
    cleanup_old_championship()

    # Step 2: Recreate with patch
    success = create_new_championship()

    if success:
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Launch rFactor")
        print("2. Go to: Race -> Championship")
        print("3. Select: Test Championship 2025")
        print("4. Go to: Vehicles menu")
        print("5. Check if vehicles are available for purchase")
        print("=" * 60)
    else:
        print("\n[FAILED] Championship creation failed. Check errors above.")
