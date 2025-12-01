"""
Demonstration script for creating a custom championship.

This script shows how to use the ChampionshipCreator service to create
a complete custom championship with isolated vehicles.
"""

from src.services.championship_creator import ChampionshipCreator
from src.utils.config import get_config


def main():
    """Create a demo championship."""
    # Get rFactor path from configuration
    config = get_config()
    if not config.is_configured():
        print("ERROR: rFactor path not configured")
        print("Please configure the path in config.json")
        return

    rfactor_path = config.get_rfactor_path()
    print(f"Using rFactor path: {rfactor_path}")
    print()

    # Initialize creator
    creator = ChampionshipCreator(rfactor_path)

    # Championship configuration
    championship_name = "DemoChampionship2025"
    print(f"Creating championship: {championship_name}")
    print()

    # Check if name is available
    if not creator.validate_championship_name(championship_name):
        print(f"WARNING: Championship '{championship_name}' already exists")
        response = input("Delete existing championship? (y/n): ")
        if response.lower() == 'y':
            creator.delete_championship(championship_name)
            print(f"Deleted existing championship")
        else:
            print("Aborted")
            return

    # Vehicle assignments (vehicle_path + driver_name)
    # Note: Paths are case-sensitive and must match actual file structure
    vehicle_assignments = [
        {
            'vehicle_path': 'Rhez/2005Rhez/GT3/Team Blue/BLU_08.veh',
            'driver_name': 'John Doe'
        },
        {
            'vehicle_path': 'Rhez/2005Rhez/SRGP/Team Red/Rd_01.veh',
            'driver_name': 'Jane Smith'
        },
        {
            'vehicle_path': 'Rhez/2005Rhez/SRGP/Campana/Campa_27.veh',
            'driver_name': 'Bob Johnson'
        },
    ]

    print("Vehicle assignments:")
    for assignment in vehicle_assignments:
        print(f"  - {assignment['vehicle_path']} -> {assignment['driver_name']}")
    print()

    # Track selection
    tracks = [
        'Mills_Short',
        'Toban_Long',
        'Joesville_Speedway',
    ]

    print("Tracks:")
    for i, track in enumerate(tracks, 1):
        print(f"  {i}. {track}")
    print()

    # Options
    options = {
        'full_name': 'Demo Championship 2025',
    }

    # Create championship
    print("Creating championship...")
    print("-" * 50)

    try:
        rfm_path = creator.create_championship(
            championship_name,
            vehicle_assignments,
            tracks,
            options
        )

        print("-" * 50)
        print()
        print("SUCCESS!")
        print()
        print(f"RFM file created: {rfm_path}")
        print(f"Isolated vehicles in: GameData/Vehicles/RFTOOL_{championship_name}/")
        print()
        print("You can now:")
        print("  1. Launch rFactor")
        print("  2. Select the championship from the list")
        print("  3. rFactor will automatically create the .cch file")

    except Exception as e:
        print()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
