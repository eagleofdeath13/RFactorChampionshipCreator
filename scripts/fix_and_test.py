"""
Complete fix: patch both issues and recreate championship
"""
import sys
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.championship_creator import ChampionshipCreator
from src.services.vehicle_isolation_service import VehicleIsolationService
from src.models.rfm import CareerSettings, PitGroup, RFMod, Season

print("=" * 70)
print("APPLYING PATCHES")
print("=" * 70)

# =======================
# PATCH 1: Fix _copy_vehicle_assets to skip .veh files
# =======================
original_copy_assets = VehicleIsolationService._copy_vehicle_assets

def patched_copy_vehicle_assets(self, source_dir, dest_dir, original_veh_name, vehicle_prefix):
    """Patched version that skips .veh files."""
    veh_base = Path(original_veh_name).stem
    rename_extensions = ['.dds', '.tga', '.bmp', '.txt']
    copied_files = set()

    for asset_file in source_dir.iterdir():
        if not asset_file.is_file():
            continue

        # PATCH: Skip .veh files - they are handled separately
        if asset_file.suffix.lower() == '.veh':
            continue

        file_key = asset_file.name.lower()
        if file_key in copied_files:
            continue

        ext_lower = asset_file.suffix.lower()

        # Determine if this file should be renamed
        should_rename = False
        if ext_lower in rename_extensions:
            if asset_file.stem.upper() == veh_base.upper():
                should_rename = True

        # Determine destination filename
        if should_rename:
            new_name = f"{vehicle_prefix}_{asset_file.name}"
        else:
            new_name = asset_file.name

        dest_file = dest_dir / new_name

        # Copy file
        try:
            if not dest_file.exists():
                shutil.copy2(asset_file, dest_file)
                copied_files.add(file_key)
        except Exception as e:
            print(f"Warning: Failed to copy {asset_file.name}: {e}")

VehicleIsolationService._copy_vehicle_assets = patched_copy_vehicle_assets
print("[PATCH 1] Applied: _copy_vehicle_assets now skips .veh files")

# =======================
# PATCH 2: Fix _create_rfm to accept isolated_paths and extract vehicle names
# =======================
def patched_create_rfm(self, championship_name, tracks, isolated_paths, options):
    """Patched version that extracts vehicle names from paths."""

    # Extract vehicle names for StartingVehicle
    num_vehicles = len(isolated_paths)
    starting_vehicles = []

    for veh_path in isolated_paths:
        veh_file = Path(veh_path).stem
        starting_vehicles.append(veh_file.lower())

    print(f"[PATCH 2] Extracted {len(starting_vehicles)} vehicle names:")
    for veh in starting_vehicles:
        print(f"  - {veh}")

    # Create vehicle filter
    vehicle_filter = championship_name
    max_opponents = num_vehicles - 1
    if max_opponents < 1:
        max_opponents = 1

    full_name = options.get('full_name', championship_name)

    # Create career settings with starting vehicles
    career_settings = CareerSettings(starting_vehicles=starting_vehicles)

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

ChampionshipCreator._create_rfm = patched_create_rfm
print("[PATCH 2] Applied: _create_rfm now extracts vehicle names for StartingVehicle")

print("\n" + "=" * 70)
print("CLEANING UP OLD CHAMPIONSHIP")
print("=" * 70)

# Configuration
RFACTOR_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\rFactor"
CHAMPIONSHIP_NAME = "TestChampionship2025"

# Delete old championship
vehicles_folder = Path(RFACTOR_PATH) / "GameData" / "Vehicles" / f"RFTOOL_{CHAMPIONSHIP_NAME}"
if vehicles_folder.exists():
    print(f"Deleting: {vehicles_folder}")
    shutil.rmtree(vehicles_folder)

rfm_file = Path(RFACTOR_PATH) / "rFm" / f"RFTOOL_{CHAMPIONSHIP_NAME}.rfm"
if rfm_file.exists():
    print(f"Deleting: {rfm_file}")
    rfm_file.unlink()

rfm_bak = Path(RFACTOR_PATH) / "rFm" / f"RFTOOL_{CHAMPIONSHIP_NAME}.rfm_bak"
if rfm_bak.exists():
    print(f"Deleting: {rfm_bak}")
    rfm_bak.unlink()

userdata_folder = Path(RFACTOR_PATH) / "UserData"
for player_folder in userdata_folder.glob("*"):
    if player_folder.is_dir():
        cch_file = player_folder / f"RFTOOL_{CHAMPIONSHIP_NAME}.cch"
        if cch_file.exists():
            print(f"Deleting: {cch_file}")
            cch_file.unlink()

print("\n" + "=" * 70)
print("CREATING NEW CHAMPIONSHIP")
print("=" * 70)

# Create championship
creator = ChampionshipCreator(RFACTOR_PATH)

vehicle_assignments = [
    {'vehicle_path': 'ZR/SRGP/Team_Green/GRN_08.veh', 'driver_name': 'John Doe'},
    {'vehicle_path': 'Rhez/2005Rhez/SRGP/Team Red/Rd_01.veh', 'driver_name': 'Jane Smith'},
    {'vehicle_path': 'Rhez/2005Rhez/SRGP/Team Black/BLK_03.veh', 'driver_name': 'Bob Johnson'},
]

tracks = ['Mills_Short', 'Joesville_Speedway', 'Toban_Short']

try:
    rfm_path = creator.create_championship(
        championship_name=CHAMPIONSHIP_NAME,
        vehicle_assignments=vehicle_assignments,
        tracks=tracks,
        options={'full_name': 'Test Championship 2025'}
    )

    print(f"\n[SUCCESS] Championship created: {rfm_path}")

    # Verify
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)

    with open(rfm_path, 'r', encoding='windows-1252') as f:
        content = f.read()
        if 'StartingVehicle' in content:
            print("\n[OK] StartingVehicle found in RFM:")
            for line in content.split('\n'):
                if 'StartingVehicle' in line:
                    print(f"  {line}")
        else:
            print("\n[ERROR] StartingVehicle NOT found in RFM!")

    vehicles_folder = Path(RFACTOR_PATH) / "GameData" / "Vehicles" / f"RFTOOL_{CHAMPIONSHIP_NAME}"
    veh_files = sorted(vehicles_folder.glob("**/*.veh"), key=lambda x: x.name)
    print(f"\n[INFO] Found {len(veh_files)} .veh file(s):")
    for veh in veh_files:
        rel_path = veh.relative_to(vehicles_folder)
        print(f"  - {rel_path}")

    if len(veh_files) == 3:
        print("\n[OK] Correct number of vehicles (3)")
    else:
        print(f"\n[WARNING] Expected 3 vehicles, found {len(veh_files)}")

    print("\n" + "=" * 70)
    print("TEST IN RFACTOR")
    print("=" * 70)
    print("1. Launch rFactor")
    print("2. Go to: Race -> Championship")
    print("3. Select: Test Championship 2025")
    print("4. Go to: Vehicles menu")
    print("5. Check if vehicles appear for purchase")
    print("=" * 70)

except Exception as e:
    print(f"\n[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()
