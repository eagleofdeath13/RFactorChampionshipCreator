"""
Script to clean up and recreate Test Championship
"""
import sys
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.championship_creator import ChampionshipCreator

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

    # Initialize creator
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

        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to create championship: {e}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CLEANUP AND RECREATE TEST CHAMPIONSHIP")
    print("=" * 60)

    # Step 1: Cleanup
    cleanup_old_championship()

    # Step 2: Recreate
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
