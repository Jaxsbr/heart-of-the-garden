

HeartOfTheGarden/
├── assets/                   # Holds all graphical and visual assets
│   ├── images/               # Subfolder for image files (e.g., tiles, characters, plants)
│   └── tiles/                # Terrain tiles (soil, water, rocks)
├── config/                   # Configuration files and constants
│   ├── game_settings.py      # Contains game-wide settings (e.g., screen size, tile size)
│   └── level_data.py         # Predefined levels and enemy wave configurations
├── core/                     # Core game logic
│   ├── game_manager.py       # Controls game loop and state transitions
│   ├── protector.py          # Handles Protector movement and actions
│   ├── plant.py              # Defines the defensive plant mechanics
│   ├── enemy.py              # Implements enemy behavior and wave logic
│   └── heart.py              # Manages the Heart’s health and win/loss conditions
├── ├── resources/         # Resource management logic
│   │   ├── __init__.py
│   │   ├── resource_manager.py # Core resource management
│   │   ├── asset_loader.py     # Helper for loading assets (e.g., images, sounds)
│   │   ├── cache.py            # Asset caching utilities
│   │   └── manifest.py         # Asset manifest handling
├── ui/                       # Handles user interface components
│   ├── hud.py                # Heads-up display (Heart health, wave timer)
│   └── screen_manager.py     # Manages transitions between screens (future-proofing)
├── maps/                     # Stores tile maps for levels
│   ├── map_1.json            # Example JSON file defining the first level's layout
├── tests/                    # Test cases for key features
│   ├── test_protector.py     # Test Protector movement and actions
│   ├── test_enemy.py         # Test enemy behavior and pathfinding
│   ├── test_plant.py         # Test planting mechanics
│   └── test_game_loop.py     # Test overall game loop and win/loss logic
├── main.py                   # Entry point for the game
└── README.md                 # Project description and setup instructions
