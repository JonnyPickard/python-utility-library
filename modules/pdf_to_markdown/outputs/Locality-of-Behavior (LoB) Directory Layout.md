## **Locality-of-Behavior (LoB) Directory Layout**

```
res://
├── addons/ # Third-party plugins (e.g. GUT)
│ └── gut/ # Godot Unit Test plugin
│ └── ...
├── features/ # Features/modules, co-locating code, assets, and 
tests
│ ├── world/ # Example feature: world generation and streaming
│ │ ├── world.tscn # Scene for the world (chunk manager)
│ │ ├── world.gd # Controller script for world logic
│ │ ├── world_data.tres # Resource for world settings (hex size, etc.)
│ │ ├── world_assets/ # Assets used exclusively by this world feature
│ │ │ ├── hex_tiles.png
│ │ │ └── terrain_material.tres
│ │ └── tests/ # Unit tests for this feature
│ │ ├── test_world_chunk_loading.gd
│ │ └── test_hex_grid_navigation.gd
│ ├── player/ # Feature: player entity
│ │ ├── player.tscn
│ │ ├── player.gd
│ │ ├── player_assets/
│ │ │ ├── player_model.glb
│ │ │ └── player_textures.png
│ │ └── tests/
│ │ └── test_player_movement.gd
│ ├── pathfinding/ # Feature: hex grid and pathfinding system
│ │ ├── hex_grid.gd # Hex grid coordinate system and navigation
│ │ ├── pathfinder.gd # A* pathfinding logic on hex grid
│ │ └── tests/
│ │ └── test_pathfinding.gd
│ ├── combat/ # Feature: combat mechanics
│ │ ├── combat.tscn # Scene for combat encounters (if needed)
│ │ ├── combat.gd # Combat logic (attacks, hit resolution)
│ │ ├── combat_assets/
│ │ │ └── attack_effects.png
│ │ └── tests/
│ │ └── test_damage_calculation.gd
│ └── ... # More features (inventory, AI, UI, etc.), each 
with its own code, assets, tests
├── global/ # Cross-cutting code (systems and singletons)
│ ├── networking/ # Network layer (network managers, RPC handlers)
```

```
│ │ ├── network_manager.gd # Manages ENet/WebSocket connections
│ │ ├── message_definitions.tres
│ │ └── ...
│ ├── simulation/ # Tick-based simulation core
│ │ ├── tick_manager.gd # Fixed-timestep driver
│ │ └── ...
│ └── common/ # Shared utilities and resources
│ ├── util.gd # Miscellaneous helper functions
│ ├── data_models.gd # Shared DataResources or definitions
│ └── ...
├── tools/ # Editor plugins and external tooling
│ ├── map_editor/ # Custom map editor plugin (e.g. hex pattern 
design)
│ │ ├── map_editor_plugin.gd
│ │ └── plugin.cfg
│ ├── chunk_loader.gd # Standalone script or scene to preprocess chunk 
data
│ └── ...
├── tests/ # (Optional) Global test suites or integration 
tests
│ ├── integration/
│ └── utility_tests/
├── project.godot # Godot project file
└── README.md
```

- **Features/**: Under LoB, each major feature or game system (world streaming, player, combat, etc.) has its own folder. *Code, scenes, assets, and tests that implement that feature live together*, making behavior self-contained . • [1](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k#:~:text=Here%E2%80%99s%20what%20it%20is%20about%3A) [2](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html#:~:text=It%E2%80%99s%20generally%20a%20better%20idea,based%20organization%2C%20something%20like%20this)
- **Feature subfolders** (e.g. world/ , player/ , pathfinding/ ): Each contains a main scene file ( .tscn ), its controller script(s) ( .gd ), any feature-specific resource files, and an assets/ subfolder for art/audio used only by that feature. Names use **snake\_case** for files and folders as per Godot conventions . • [3](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=This%20section%20,instead)
- **Tests**: Following GUT guidelines , unit tests for a feature are placed in a tests/ subfolder of that feature. For example, features/world/tests/test\_world\_chunk\_loading.gd would contain tests extending GutTest . This co-location keeps tests near the code they verify, satisfying LoB. GUT's quickstart recommends separating unit and integration tests (e.g. test/unit vs test/integration ), but here we localize them by feature for modularity . • [4](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,as%20often%20as%20is%20useful) [4](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,as%20often%20as%20is%20useful)
- **addons/**: Holds third-party plugins. For example, GUT is installed here ( addons/gut/ ) so the test runner is available. •
- **global/**: Contains cross-cutting systems (network manager, tick manager, utility scripts) and autoload singletons. For example, simulation/tick\_manager.gd is an autoloaded script that drives a fixed timestep simulation loop for the whole game. •
- **tools/**: Contains editor scripts and external utilities. Custom editors (e.g. a hex-map editor plugin), import scripts (e.g. a tool to bake raw heightmap data into chunks), or level preprocessors go here. •
- **Naming Conventions**: Use *snake\_case* for directories and GDScript file names, *PascalCase* for any C# scripts. Scene files ( .tscn ) and resource files ( .tres ) are typically lower\_snake (as they are files). •

Each controller script/class should be named after its scene and scene root node (e.g. world.tscn with a world.gd script attached to root node "World"). This makes behavior obvious from the code location . 5 [1](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k#:~:text=Here%E2%80%99s%20what%20it%20is%20about%3A) [5](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=,This%20keeps)

### **GUT Testing Integration**

Unit and integration tests live alongside feature code: e.g. features/player/tests/test\_movement.gd . Each test script extends GutTest and is autodiscovered by GUT when placed in the project. Tests must be named with the test\_ prefix or configured accordingly. You should configure GUT (in the editor panel) to include all \*/tests/ directories. Optionally, have top-level tests/unit/ and tests/integration/ dirs for broad tests (as GUT recommends) ; these can import features from their folders. This structure keeps tests near code for quick understanding (LoB principle) while allowing global test runs. [6](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,script%20supplied%20by%20GUT) [4](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,as%20often%20as%20is%20useful)

## **Asset Pipeline and Chunk Streaming**

A key workflow is building the world in chunks. The **map design pipeline** might use:

- **External tools**: Designers use a hex-map editor (Tiled, or a custom Godot tool in tools/ map\_editor/ ) to lay out terrain, placing hex-tile IDs on a grid. These raw maps (e.g. .tmx or JSON) are kept outside the game/ folder (per Godot best practice) to avoid exporting source assets . • [7](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html#:~:text=It%20is%20very%20often%20necessary,recognize%20them%20and%20export%20both)
- **Import**: A Godot import script or autoload in tools/ converts the raw map into Godot resources. For example, an editor plugin reads the map and splits it into region-based scenes ( scenes/ levels/hex\_chunk\_001.tscn , etc.), each with a TileMap or Mesh. These "chunk" scenes are saved in scenes/levels/ . •
- **Runtime streaming**: The world root node (controlled by world.gd ) holds an instance of ChunkManager . As the player moves, the ChunkManager determines which adjacent chunks should be loaded (e.g. within a 3×3 grid around the player). It uses PackedScene.instance() or ResourceLoader.load\_interactive() to load chunk scenes asynchronously (in a background thread) . Chunks moving out of range are removed from the SceneTree and freed to save memory. The **background loading** approach (supported by Godot) ensures smooth transitions: "A background game thread could be used to manage preloading and unloading nearby scenes asynchronously based on player movement" . In code, chunk scenes live under scenes/ levels/ and are instanced by path or preload. • [8](https://www.reddit.com/r/godot/comments/198tsu8/how_would_you_approach_an_seamless_openworld_map/#:~:text=A%20background%20game%20thread%20could,main%20node%20tree%20when%20appropriate) [8](https://www.reddit.com/r/godot/comments/198tsu8/how_would_you_approach_an_seamless_openworld_map/#:~:text=A%20background%20game%20thread%20could,main%20node%20tree%20when%20appropriate)
- **LODs**: You can supply low-detail and high-detail chunk variants. Faraway chunks can be swapped with lower-detail scenes (or simply have fewer objects) and replaced with high-detail when the player is nearby . • [9](https://www.reddit.com/r/godot/comments/198tsu8/how_would_you_approach_an_seamless_openworld_map/#:~:text=Dziadzios)
- **Memory**: Each chunk scene is a moderate-size node hierarchy. Unloading is done via queue\_free() when out of range. Use Godot's ResourceLoader to free unused resources. Keep dynamic data out of scenes if possible (use Resources for terrain height, etc., so it can be shared or reused). For very large worlds, consider manually freeing unused scripts and textures, or use Godot 4's **reference-counted resources** (like ImageTexture.unload() ). •

## **Tick-Based Simulation**

An MMO needs a deterministic, fixed-timestep simulation. In this layout, a single **TickManager** (autoloaded from global/simulation/tick\_manager.gd ) drives the game loop at, say, 20 or 30 ticks per second. All game logic that needs to be deterministic (NPC AI, physics, etc.) is updated by the TickManager rather than relying on frame rate. Entities register with TickManager and implement a tick(delta) function. This central manager can also emit a "world\_tick" signal each step. Input and rendering still happen on \_process() , but authoritative game state changes on ticks. A possible organization: - **TickManager.gd**: emits world\_tick every fixed interval (set by project settings or custom timer).

- Each entity node (in features/ ) has a script that listens to world\_tick and updates position/logic.

- On the server (authoritative), the TickManager runs and sends new states to clients after each tick. Clients interpolate between states for smoothness.

This enforces synchronous simulation. All tick-related code (scheduling events, processing queued commands, advancing game time) belongs under global/simulation/ or within the relevant feature scripts but triggered by the TickManager.

## **Hex Grid Navigation and Multi-Layer Movement**

The **hex grid system** is typically encapsulated in a feature (e.g. features/pathfinding/hex\_grid.gd ). This code handles coordinate conversions (axial/cube coords) and neighbor offsets. For example, the [GDHexGrid](https://github.com/romlok/godot-gdhexgrid) library shows how to map flat-topped hexes and even includes A *pathfinding on a hex grid . We adopt a similar approach: our HexGrid class has methods to get adjacent hexes, compute distances, and convert hex coordinates to world positions. Pathfinding uses A* on a 2D grid of hex cells (flagging obstacles), as outlined in Red Blob Games guides . *[10](https://github.com/romlok/godot-gdhexgrid#:~:text=HexGrid%20pathfinding)* [10](https://github.com/romlok/godot-gdhexgrid#:~:text=HexGrid%20pathfinding)

**Multi-layer movement** (e.g. ground vs. mountain vs. air): We treat layers as separate path graphs or use Godot's Navigation2D with layers. In Godot 4, you can assign different tilemaps or navigation meshes to navigation layers (like physics layers for agents) to constrain movement . For example, flying units might use a "sky" NavMap, while ground units use a "ground" NavMap. Godot's NavigationRegion and NavigationLink (in 3D) or TileMap navigation (in 2D) support multiple layers. The navigation logic resides in the same feature (pathfinding) – e.g. a NavManager script that queries NavigationServer2D with specific layer masks. Godot docs note that tilemap navigation layers needed a PR to work correctly, essentially placing each layer on separate navigation maps . In practice, we might bake multiple navmeshes (one per layer) and switch the agent's map or layer\_mask as needed. [11](https://www.reddit.com/r/godot/comments/11z9ntk/godot_4_2d_only_first_tilemap_navigation_layers/#:~:text=In%20general%20navigation%20is%20not,no%20matter%20the%20navigation%20layers) [11](https://www.reddit.com/r/godot/comments/11z9ntk/godot_4_2d_only_first_tilemap_navigation_layers/#:~:text=In%20general%20navigation%20is%20not,no%20matter%20the%20navigation%20layers)

### **Streaming and Memory Management**

The LoB structure encourages each feature to manage its own memory. For example, the world feature loads/unloads chunk scenes and is responsible for freeing them. The pathfinding feature may load path mesh data only when needed. General strategies: - **Chunk pooling**: Instead of freeing, you could keep a pool of recently used chunks and reuse them to reduce allocation cost.

- **View frustum culling**: Non-active areas of world remain unloaded.

- **Godot Resources**: Use @export var preload\_scene: PackedScene or .tres resources for lightweight data.

- **Threading**: Long operations (like baking navmesh or loading large scenes) run via Thread or background\_loader to avoid hitches, as suggested by Godot background loading docs.

Memory profiling and leak testing are done via GUT's leak testing features or Godot's built-in Profiler. Each feature's tests can include leak checks after loading/unloading. 12

## **Networking (Client-Server)**

In LoB layout, network code (RPCs, sync) often sits in the feature or global scripts that are network-aware. For instance: - **NetworkManager** ( global/networking/network\_manager.gd ): A singleton that sets up the MultiplayerPeer (ENet or WebSocket) and handles connection/disconnection. It may use Godot 4's MultiplayerSynchronizer nodes inside scenes to replicate state . [13](https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/#:~:text=,be%20synchronized%20by%20which%20peer)

- **Scenes**: Networked scenes use MultiplayerSpawner and MultiplayerSynchronizer nodes as shown in Godot's official guide . For example, a player character scene might have a MultiplayerSynchronizer to sync its position and health. The features/player/player.gd script can check is\_multiplayer\_authority() for server-side logic. [13](https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/#:~:text=,be%20synchronized%20by%20which%20peer)

- **Separation**: On a dedicated server, many visuals/scripts (UI, effects) are omitted. The same project can run as headless for the server. Code that only runs on server (AI simulation) is behind if multiplayer.is\_server(): checks.

Data flow: client inputs (move, actions) are sent to server (via RPC or custom packets), server updates authoritative state on ticks, and syncs back to clients. Network messages (e.g. chat, action commands) use custom Resource data (in global/networking/message\_definitions.tres ) so they can be versioned and extended.

Godot's built-in ENet can handle up to **~4096 simultaneous clients** (practical limit imposed by the library) . For a large MMO, this implies either sharding across multiple servers or using a lower-level/more scalable networking stack. In our design, the LoB structure still allows hooking in an external server: e.g. using Godot's WebSocketClient to connect to a Node.js backend, as done by community projects . [14](https://www.reddit.com/r/godot/comments/1jobzmg/can_i_start_worrying_about_the_4k_user_limit_on/#:~:text=Godot%27s%20EnetMultiplayer%20Server%20supports%20up,IIRC%29%20clients%20connections) [15](https://www.reddit.com/r/godot/comments/tpudwy/i_have_been_working_on_a_simple_online/#:~:text=I%27m%20planning%20to%20do%20a,now%20it%27s%20just%20a%20prototype)

# **Industry-Standard Large-Scale MMO Architecture Layout**

| res://                       |                                          |
|------------------------------|------------------------------------------|
| ├── addons/                  | # Third-party plugins (GUT, etc.)        |
| │<br>└── gut/                |                                          |
| ├── assets/                  | # All raw assets (imported into Godot)   |
| │<br>├── textures/           |                                          |
| │<br>├── models/             |                                          |
| │<br>├── audio/              |                                          |
| │<br>├── fonts/              |                                          |
| │<br>└── data/               | # JSON/CSV config, skill/item data, etc. |
| ├── scenes/                  | # All Godot scenes (.tscn files)         |
| │<br>├── levels/             | # Level and chunk scenes                 |
| ├── chunk_001.tscn<br>│<br>│ |                                          |
| │<br>│<br>├── chunk_002.tscn |                                          |
| │<br>│<br>└──                |                                          |

| │<br>├── entities/                  | # Scene prefabs for entities                      |
|-------------------------------------|---------------------------------------------------|
| │<br>│<br>├── player/               |                                                   |
| ├── player_body.tscn<br>│<br>│<br>│ | ly.tscn                                           |
| │<br>│<br>│<br>└──                  |                                                   |
| │<br>│<br>├── npc/                  |                                                   |
| │<br>│<br>├── items/                |                                                   |
| │<br>│<br>└──                       |                                                   |
| │<br>├── ui/                        | # UI screens and windows                          |
| │<br>│<br>├── main_menu.tscn        |                                                   |
| │<br>│<br>├── hud.tscn              |                                                   |
| │<br>│<br>└──                       |                                                   |
| │<br>├── world/                     | # Global scenes (game root, server-only, etc.)    |
| │<br>│<br>├── server_root.tscn      | cn                                                |
| │<br>│<br>└── client_root.tscn      | cn                                                |
| │<br>└──                            |                                                   |
| ├── scripts/                        | # GDScript (or C#) code, organized by category    |
| │<br>├── ai/                        | # AI behaviors and state machines                 |
| │<br>├── gameplay/                  | # Core mechanics (combat, inventory, skills)      |
| ├── navigation/<br>│                | # Pathfinding and navmesh scripts                 |
| │<br>│<br>└── hex_nav.gd            | # Hex grid navigation helper                      |
| │<br>├── networking/                | # Low-level network code                          |
| │<br>│<br>├── client.gd             | # Client-side net manager                         |
| │<br>│<br>├── server.gd             | # Server-side net manager (headless)              |
| │<br>│<br>└── protocol.gd           | # Message serialization/deserialization           |
| │<br>├── systems/                   | # ECS-like or manager systems (if used)           |
| │<br>├── ui/                        | # UI controllers                                  |
| │<br>└── util/                      | # Utility scripts (logger, math, etc.)            |
| ├── resources/                      | # Custom resources (.tres) and configs            |
| │<br>├── player_stats.tres          |                                                   |
| │<br>├── world_settings.tres        |                                                   |
| │<br>└──                            |                                                   |
| ├── tests/                          | # Global test suites                              |
| │<br>├── unit/                      |                                                   |
| │<br>├── integration/               |                                                   |
| └── scenarios/<br>│                 |                                                   |
| ├── tools/                          | # Build scripts, level converters, external tools |
| │<br>├── map_importer.py            |                                                   |
| │<br>├── chunk_baker.gd             |                                                   |
| │<br>└──                            |                                                   |
| ├── project.godot                   |                                                   |
| └── README.md                       |                                                   |

**Assets/**: Organized by type (textures, models, audio) for easy reuse and processing. All imported Godot assets reside here. Raw source files (e.g. 3D models .blend , concept art) are kept outside (e.g. in a separate art/ folder) to avoid exporting non-game files . • [7](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html#:~:text=It%20is%20very%20often%20necessary,recognize%20them%20and%20export%20both)

- **Scenes/**: Types of scenes are grouped: level/chunk scenes under levels/ , entity prefabs under entities/ , UI under ui/ , etc. This mirrors many large projects and the GitHub advice ("scenebased assets folder") . For example, scenes/levels/chunk\_001.tscn includes its TileMap and any local resources. Scenes that are reused across the game (like an enemy\_type\_a.tscn used in many levels) live in entities/ . Global root scenes ( server\_root.tscn vs client\_root.tscn ) separate server-only logic. • [16](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=%60balls_fish_fishdata.tres%60%2C%20%60balls_fish.mesh%60%2C%20etc.%20%2A%20Scene,resources%20used%20by%20many%20different)
- **Scripts/**: Pure code is separated by system or feature **type** (not by game feature). For example, all AI scripts go under scripts/ai/ , all navigation/pathfinding code in scripts/navigation/ . This is a common large-project pattern: it aids IDE navigation and reuse. However, it means one may have to open multiple folders to see all parts of a feature's behavior. •
- **Resources/**: Any custom .tres resources (data-only files) such as skill definitions, item stats, or world constants. These are kept in one place, rather than spread in feature folders. For example, world\_settings.tres might define hex spacing, chunk size, tick rate, etc. •
- **Global Network and Simulation**: Here, network and simulation code are explicitly separated: e.g. scripts/networking/client.gd and scripts/networking/server.gd drive the two roles. This makes it clear what runs on each. •
- **Tests/**: All tests are outside the main code (unlike LoB). GUT is configured to scan tests/unit and tests/integration , which reference code from anywhere. This makes running full-suite tests simple, at the cost of jumping around to find code under test. •
- **Naming**: Same conventions: snake\_case for files/folders (PascalCase for C#). Controller scripts are named after the scenes they govern , but here scene files themselves are in separate folders. For example, entities/player/player\_body.tscn with scripts/gameplay/player\_body.gd controlling it. • [5](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=,This%20keeps)
- **Autoloads & Singletons**: May have a top-level scripts or autoloads folder. For instance, scripts/systems/logging.gd as an autoload (Logger), or scripts/systems/ tick\_system.gd managing ticks. These are often in a systems or util folder. •

## **GUT Testing Structure**

Following industry practice, place tests in dedicated tests/ directories: e.g. tests/unit/ test\_hexgrid.gd and tests/integration/test\_world\_load.gd . Configure GUT to include these directories (as per its quickstart guide ). Tests import and instantiate scenes or scripts from the main project structure, rather than being co-located. This makes test execution language-agnostic (all in one place) and easier to run via CI, at the expense of scattering context. [4](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,as%20often%20as%20is%20useful)

### **Asset Pipeline Workflow**

Asset workflow is more formalized:

- **Content Creation**: Artists save raw files (e.g. art/terrain.eps , art/models/\*.blend ) in a source repo outside the Godot project. •
- **Import and Setup**: Use scripts (possibly in tools/ ) to batch-import or convert assets into assets/ (textures, models). For example, a Python or GDScript tool ( tools/map\_importer.gd ) may read Tiled .tmx hex maps and generate .tscn chunk scenes into scenes/levels/ . •
- **Chunk Preparation**: An external or in-editor "chunk baker" tool may preprocess navmeshes and object placement for each chunk. Processed chunks (PackedScenes) live in scenes/levels/ . •

**Runtime Streaming**: The game's world manager (e.g. in scenes/world/world\_root.tscn with scripts/gameplay/world\_manager.gd ) loads chunk scenes around the player. Code for asynchronous loading (using Thread or ResourceLoader ) is found in scripts/gameplay/ or scripts/systems/ . •

In this layout, assets are decoupled from specific features, so the pipeline may use naming conventions (prefix assets with scene names ) to find relevant assets. But since scenes have their own directories, each chunk's local assets can still live in assets/levels/ or inline. [17](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=%2A%20Search,for%20inherited%20scenes%20within%20their)

## **Tick-Based Simulation Organization**

Tick logic is typically implemented in a "system" script (e.g. scripts/systems/simulation.gd ) or as an autoload. For example, a FixedTickSystem autoload drives world ticks. All game systems subscribe to it. Unlike LoB, there isn't a single feature folder; instead, tick handling functions are in scripts under scripts/systems/ or relevant subsystems. For instance, scripts/systems/ai\_manager.gd may be called by the tick system to update NPCs. The fixed timestep is configured in Project Settings or in code. The important part is that all ticked code is organized under scripts/ , not spread next to scenes.

### **Hex Grid and Pathfinding**

The hex grid code lives in scripts/navigation/ (e.g. hex\_grid.gd , pathfinder.gd ). The logic to convert coordinate systems and run A\* is shared by all features that need pathfinding. For example, an NPC's movement code (in scripts/ai/ ) would call HexGrid.get\_neighbor\_coords() or Pathfinder.find\_path(start, goal) . Any pathfinding settings (like movement costs) might be stored in resources/pathfinding\_settings.tres . Multi-layer navigation (bridges, tunnels) is handled by loading multiple NavigationPolygon s into NavigationRegion2D nodes in scene (e.g. in scenes/ world/chunk\_001.tscn ) and using Godot's Navigation layers to select appropriate graphs.

## **Streaming and Memory Management**

Chunk streaming code (e.g. a ChunkLoader script) is placed under scripts/gameplay/ or scripts/ systems/ . It monitors the player's position (via a global autoload or the main scene) and loads/unloads from scenes/levels/ . Memory is freed by calling queue\_free() on old chunk instances. Global pooling systems (also under scripts/systems/ ) might reuse node instances for frequently spawned objects (bullets, enemies). Large static resources (heightmaps, biomes) are stored as Godot Resources ( .tres ) under resources/ , which can be preload ed or load() d on demand; unloading them is automatic when no scene references them.

## **Networking and Entities**

Networked scenes and entities follow Godot's recommended pattern . For example, the scenes/world/client\_root.tscn contains a MultiplayerSpawner node configured to spawn player and world scenes. Each spawned scene has a MultiplayerSynchronizer for its relevant properties. Code controlling networking (e.g. on join, on spawn) resides under scripts/networking/ . Separation is explicit: e.g. scripts/networking/server.gd runs on the headless server and has authority, while client.gd on clients applies updates and sends inputs. Shared code (like the data model for an entity) may be in scripts/util/ or a resources/ file so both sides use the same definitions. [13](https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/#:~:text=,be%20synchronized%20by%20which%20peer)

If using an external (e.g. TypeScript) server, the Godot project's network layer (in scripts/networking/ ) would use WebSocketClient or WebRTCMultiplayer to talk to it. The separation is clearer: Godot is purely client, and server code (not in this project) runs in Node/TS.

## **Comparative Analysis**

- **Organization by Feature vs. by Type**: The LoB layout groups everything (scenes, scripts, assets, tests) for a feature in one place . The industry layout separates by asset type or system. LoB is more self-contained (good for small teams or feature owners) , while the industry layout can be more scalable for large teams specializing in art, code, etc. For example, in LoB you might have features/combat/ with its own scripts and assets, whereas in the industry layout combat scripts live in scripts/gameplay/combat/ and combat assets in assets/ui/ or similar. • [1](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k#:~:text=Here%E2%80%99s%20what%20it%20is%20about%3A) [16](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=%60balls_fish_fishdata.tres%60%2C%20%60balls_fish.mesh%60%2C%20etc.%20%2A%20Scene,resources%20used%20by%20many%20different) [1](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k#:~:text=Here%E2%80%99s%20what%20it%20is%20about%3A)
- **Ease of Navigation**: LoB makes it easy to find all parts of a feature (just look under one folder), reducing "jumping around" to piece behavior . The type-based approach requires knowing where code lives globally (e.g. AI code under scripts/ai/ ). However, type-based can make it easier to reuse code and track usage of assets across features (all sounds in one place, etc.). • [1](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k#:~:text=Here%E2%80%99s%20what%20it%20is%20about%3A)
- **Modularity and Dependencies**: LoB encourages minimal external dependencies: each feature relies mainly on its own resources. This can improve cohesion but sometimes leads to duplication (two features might import the same texture into their own asset folders). The industry layout naturally shares resources: all features draw from the same assets/ pool and the same code libraries in scripts/ . This reduces redundancy but can increase coupling (a change in a global script affects many features). •
- **Testing**: LoB puts tests next to code, making developers more likely to write tests (they see them) and simplifying understanding. Industry approach centralizes tests; running a subset of tests per feature is harder, but global QA is streamlined. GUT supports both styles (tests can call into code anywhere) . • [4](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,as%20often%20as%20is%20useful)
- **Pipeline and Collaboration**: For LoB, artists/designers might need to navigate into feature folders to add assets, which can get cluttered if not managed carefully. Industry layout's separation of assets/ and scenes/ can be clearer for roles (artists put art in assets/ , designers edit scenes/levels/ ). On the other hand, LoB's feature folders can contain feature-specific art pipelines (e.g. a custom map editor for the world feature in features/world/ ). •

Both structures can support an MMO, but differ in emphasis. LoB is often easier for initial development and small teams (everything for "World" is in one place), while the industry-type layout is how many large projects scale (shared systems, clear separation of code vs content, and complex build pipelines).

## **Best Practices and Conventions**

- **Naming**: Use snake\_case for all file and folder names (Godot standard) . For example: hex\_grid.gd , player\_model.glb , world\_settings.tres . Use PascalCase for class names (via class\_name ) and C# scripts. Name scene files after their root node and controller (e.g. player.tscn with root node "Player" and script player.gd ). • [3](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=This%20section%20,instead)
- **File Placement**: Keep GUI scenes in a ui/ folder, levels in scenes/levels/ or feature-level folders, etc. Autoload singletons (e.g. TickManager.gd ) can reside in a top-level scripts/ systems/ or in an autoloads/ folder. Keep .gd scripts close to what they control, or in a •

dedicated scripts/ area if you prefer. Use descriptive folder names ( world/ , player/ , ui/ ) rather than generic ones.

- **Scenes and Scripts**: Each scene has one "controller" script attached to its root, named the same as the scene . Additional scripts (for child nodes) use descriptive names and are kept minimal. Follow the recommended GDScript ordering (signals, enums, consts, vars, \_init, \_ready, etc.). Group related scripts (AI states, utilities) together in their subfolders. • [5](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=,This%20keeps)
- **Modular Design**: Design each scene to be as self-contained as possible . Inject external dependencies via signals or setter methods. Use custom Resource classes to store data (e.g. stats or tile definitions) so scenes load data without hardcoding. Use Godot's composition (SceneTree, instancing) instead of deep inheritance to avoid rigid coupling. • [18](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=,This%20keeps)
- **Version Control**: Follow Godot docs: ignore .import/ folders and .fscache files . Keep project-wide config ( project.godot ) at root. Use consistent case (all lowercase) to avoid casesensitivity issues . • [19](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html#:~:text=Cache%20files%C2%B6)
- **Naming Assets**: For scene-specific assets, some developers prefix asset files with the scene name for searchability (e.g. player\_idle.png for the Player scene) . Keep shared assets (like common shaders or fonts) in global folders. • [17](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=%2A%20Search,for%20inherited%20scenes%20within%20their)
- **Modular Pipelines**: If you have tools (e.g. a map generator), integrate them as either editor plugins ( addons/ ) or external scripts ( tools/ ). Document their usage. For example, you might include a Python script tools/convert\_hex\_map.py and note in README that designers should run it to generate Godot chunks. •
- **Networking**: Follow Godot's high-level multiplayer best practices . All RPC methods should be @rpc annotated. Use authoritative server logic and reject client discrepancies. Avoid calling change\_scene() in multiplayer; instead use MultiplayerSpawner to switch levels so all clients sync . • [13](https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/#:~:text=,be%20synchronized%20by%20which%20peer) [20](https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/#:~:text=control%20which%20peer%20is%20allowed,the%20server%20by%20default)
- **Performance**: Aim to keep tick/update logic fast. Profile using Godot's built-in monitors. Avoid heavy processing on clients for non-visible objects. LOD and culling are essential for large worlds. On the server, limit the number of active entities per tick. Typical targets: sub-0.01s per tick for 1000 active objects on a modern CPU. Use Godot's [Profiling](https://docs.godotengine.org/en/stable/tutorials/performance/profiling.html) and GUT's leak tests to check memory. •
- **File Examples**: Use clear names like hex\_grid.gd , tick\_manager.gd , multiplayer\_manager.gd , chunk\_loader.gd , inventory\_panel.tscn , enemy\_fsm.gd . For data resources: unit\_stats.tres , world\_geometry.csv . •
- **Error Handling**: Place error-checks when loading resources (e.g. verify ResourceLoader.load() does not return null ). In multiplayer, gracefully handle disconnects (use Godot's signals). Log important events (use a custom Logger singleton if needed). •
- **Troubleshooting Tips**: If chunks fail to load, check resource paths in the scene files. Broken links in scenes often break streaming – use "Open in FileSystem" in editor to find missing files. For networking issues, ensure peers use the same networked scenes (same path) and that MultiplayerSynchronizer is set on identical nodes. Use Godot's **Verbose Print** mode to see RPC calls. In GUT tests, if a test hangs, it may be waiting on a signal; consider using await or timeouts. •
- **Performance Benchmarks**: As an order-of-magnitude guide, Godot 4's ENet can handle thousands of connections , but practical player counts per server will be lower depending on message rate. For tick processing, test how many entities you can update per frame – a simple test could be instantiating 10,000 moving sprites and measuring FPS. Optimize until performance is acceptable (e.g. >30 FPS). Use LOD, pooling, and threading to meet goals. • [14](https://www.reddit.com/r/godot/comments/1jobzmg/can_i_start_worrying_about_the_4k_user_limit_on/#:~:text=Godot%27s%20EnetMultiplayer%20Server%20supports%20up,IIRC%29%20clients%20connections)

## **Transition Plan Between Layouts**

If moving from one structure to another, use an incremental refactor:

- **Version Control**: Ensure the project is under git or similar. Create a new branch for restructuring. 1.
- **Move Directories**: For LoB→type layout, create the new top-level folders ( scenes/ , scripts/ , assets/ , etc.). Move files accordingly. Update any hardcoded paths in code ( load("res://...") ). For type→LoB, group related scenes/scripts under a common feature folder. Godot 4 allows moving files in the editor (FileSystem dock) which updates internal references. 2.
- **Fix References**: After moving, open the project in Godot and re-save any scene that lost links. Godot will auto-fix moved script paths if possible, but double-check @export(String) resource paths. Run the game to test. 3.
- **Tests**: Move test files to new locations and update GUT settings. Run all tests to catch missing imports. 4.
- **Stubs/Deprecations**: Maintain old paths as aliases if needed (e.g. a stub script at old path that redirects to new location) during transition. Remove them once everything is stable. 5.
- **Communicate**: Update team on changes (README, docs). If multiple developers, ensure everyone updates their local workspace. 6.

Given that both structures can coexist for a while, one could adopt a hybrid: group by feature, but still have a central assets/ and scripts/ . Eventually, pick one consistent style.

## **Recommendations: Tooling & Server Architecture**

- **Custom Map Tools**: Integrate editor plugins for level design. For example, a *Hex Map Editor* plugin under addons/ can allow painting hex biomes or placing prefabs in-editor, outputting a Godot TileMap or custom resource. Alternatively, support external tools (like Tiled): write import scripts to convert .tmx into Godot scenes. Document the pipeline (e.g. in README: "Run map\_converter.py to import .tmx files into scenes/levels/ "). •
- **Server-Side Separation**: For true MMO scale, offload the game simulation to a backend server architecture. You can still use Godot headless as a server (great for prototyping), but for massive scale use a dedicated solution. One option is a **TypeScript/Node.js** server (e.g. using WebSocket or custom TCP protocol). The Godot client uses WebSocketClient or WebRTCMultiplayer to communicate. We saw an example where a developer built a Godot client and a TS server connected by WebSockets . With TS, you can leverage web tech (load balancers, database integrations). • [15](https://www.reddit.com/r/godot/comments/tpudwy/i_have_been_working_on_a_simple_online/#:~:text=I%27m%20planning%20to%20do%20a,now%20it%27s%20just%20a%20prototype)
- **External Server Patterns**: Implement a lobby/matchmaking system on the TS side, then spawn instances (perhaps still Godot headless servers) for each game session. Or write most logic in TS and have Godot as a lightweight display client. Use message schemas (JSON or binary) and keep them versioned. Use SSL/TLS if needed for security (Godot supports SSL certificates ). • [21](https://forum.godotengine.org/t/is-there-any-viable-backend-for-godot/41218#:~:text=Is%20there%20any%20viable%20backend,class%2C%20SSL%20certificates%2C%20WebSocket%2C%20WebRTC)
- **Authoritative Design**: Regardless of server language, keep server authoritative. Clients send input commands; server computes physics/simulation. For example, clients send move\_unit(direction) and server replies with unit\_position updates. Do not trust client state. •
- **Scaling**: Use multiple server instances behind a gateway. If using ENet, consider the 4096 limit as the max per server. Otherwise, implement sharding or regional servers. • [14](https://www.reddit.com/r/godot/comments/1jobzmg/can_i_start_worrying_about_the_4k_user_limit_on/#:~:text=Godot%27s%20EnetMultiplayer%20Server%20supports%20up,IIRC%29%20clients%20connections)

**Monitoring**: Integrate logging (Moonwards built a custom logger addon ). Collect metrics (tick time, network lag) to guide scaling. • [22](https://godotengine.org/article/guest-post-small-team-big-project-building-moonwards/#:~:text=The%20addon%20I%20think%20will,log%20messages%20by%20log%20type)

In summary, **both layouts can support all requirements**. The LoB design emphasizes ease of understanding and modular development , while the industry-style layout emphasizes clear boundaries and reuse. The final choice depends on team size and preferences; the above guide provides a blueprint for each. [1](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k#:~:text=Here%E2%80%99s%20what%20it%20is%20about%3A)

### Locality of behavior - DEV Community [1](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k#:~:text=Here%E2%80%99s%20what%20it%20is%20about%3A)

<https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k>

### Project organization — Godot Engine latest documentation [2](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html#:~:text=It%E2%80%99s%20generally%20a%20better%20idea,based%20organization%2C%20something%20like%20this) [7](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html#:~:text=It%20is%20very%20often%20necessary,recognize%20them%20and%20export%20both) [19](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html#:~:text=Cache%20files%C2%B6)

[https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project\\_organization.html](https://docs.huihoo.com/godotengine/godot-docs/godot/tutorials/engine/project_organization.html)

### GitHub - abmarnie/godot-architecture-organization-advice: Advice for architecting and organizing Godot projects. [3](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=This%20section%20,instead) [5](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=,This%20keeps) [16](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=%60balls_fish_fishdata.tres%60%2C%20%60balls_fish.mesh%60%2C%20etc.%20%2A%20Scene,resources%20used%20by%20many%20different) [17](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=%2A%20Search,for%20inherited%20scenes%20within%20their) [18](https://github.com/abmarnie/godot-architecture-organization-advice#:~:text=,This%20keeps)

<https://github.com/abmarnie/godot-architecture-organization-advice>

### Quick Start — GUT 9.3.1 documentation [4](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,as%20often%20as%20is%20useful) [6](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=,script%20supplied%20by%20GUT) [12](https://gut.readthedocs.io/en/9.3.1/Quick-Start.html#:~:text=Leak%20Testing%20and%20Memory%20Management%EF%83%81)

<https://gut.readthedocs.io/en/9.3.1/Quick-Start.html>

#### How would you approach an seamless open-world map in Godot 4? : r/godot [8](https://www.reddit.com/r/godot/comments/198tsu8/how_would_you_approach_an_seamless_openworld_map/#:~:text=A%20background%20game%20thread%20could,main%20node%20tree%20when%20appropriate) [9](https://www.reddit.com/r/godot/comments/198tsu8/how_would_you_approach_an_seamless_openworld_map/#:~:text=Dziadzios)

[https://www.reddit.com/r/godot/comments/198tsu8/how\\_would\\_you\\_approach\\_an\\_seamless\\_openworld\\_map/](https://www.reddit.com/r/godot/comments/198tsu8/how_would_you_approach_an_seamless_openworld_map/)

### GitHub - romlok/godot-gdhexgrid: A GDScript hexagonal grid implementation for Godot. [10](https://github.com/romlok/godot-gdhexgrid#:~:text=HexGrid%20pathfinding)

<https://github.com/romlok/godot-gdhexgrid>

### Godot 4 2D. Only first tilemap navigation layers works. : r/godot [11](https://www.reddit.com/r/godot/comments/11z9ntk/godot_4_2d_only_first_tilemap_navigation_layers/#:~:text=In%20general%20navigation%20is%20not,no%20matter%20the%20navigation%20layers)

[https://www.reddit.com/r/godot/comments/11z9ntk/godot\\_4\\_2d\\_only\\_first\\_tilemap\\_navigation\\_layers/](https://www.reddit.com/r/godot/comments/11z9ntk/godot_4_2d_only_first_tilemap_navigation_layers/)

### Multiplayer in Godot 4.0: Scene Replication – Godot Engine [13](https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/#:~:text=,be%20synchronized%20by%20which%20peer) [20](https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/#:~:text=control%20which%20peer%20is%20allowed,the%20server%20by%20default)

<https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/>

### Can I start worrying about the 4K user limit on Godot Multiplayer already? : r/godot [14](https://www.reddit.com/r/godot/comments/1jobzmg/can_i_start_worrying_about_the_4k_user_limit_on/#:~:text=Godot%27s%20EnetMultiplayer%20Server%20supports%20up,IIRC%29%20clients%20connections)

[https://www.reddit.com/r/godot/comments/1jobzmg/can\\_i\\_start\\_worrying\\_about\\_the\\_4k\\_user\\_limit\\_on/](https://www.reddit.com/r/godot/comments/1jobzmg/can_i_start_worrying_about_the_4k_user_limit_on/)

### I have been working on a simple online multiplayer game, with a Godot client and a Typescript server, all connected by websockets : r/godot [15](https://www.reddit.com/r/godot/comments/tpudwy/i_have_been_working_on_a_simple_online/#:~:text=I%27m%20planning%20to%20do%20a,now%20it%27s%20just%20a%20prototype)

[https://www.reddit.com/r/godot/comments/tpudwy/i\\_have\\_been\\_working\\_on\\_a\\_simple\\_online/](https://www.reddit.com/r/godot/comments/tpudwy/i_have_been_working_on_a_simple_online/)

### Is there any viable backend for Godot? - Help [21](https://forum.godotengine.org/t/is-there-any-viable-backend-for-godot/41218#:~:text=Is%20there%20any%20viable%20backend,class%2C%20SSL%20certificates%2C%20WebSocket%2C%20WebRTC)

<https://forum.godotengine.org/t/is-there-any-viable-backend-for-godot/41218>

### Guest post - "Small Team, Big Project": Building Moonwards – Godot Engine [22](https://godotengine.org/article/guest-post-small-team-big-project-building-moonwards/#:~:text=The%20addon%20I%20think%20will,log%20messages%20by%20log%20type)

<https://godotengine.org/article/guest-post-small-team-big-project-building-moonwards/>