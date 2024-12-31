### Code Structure Report for Coral Reef Survival Simulator

#### Directory Structure

```plaintext
coral_reef_simulator/
│
├── main.py                      # Entry point of the game
├── config.py                    # Stores game configurations and constants
├── assets/                      # Stores all game assets
│   ├── images/                  # Images and sprites
│   ├── sounds/                  # Sound effects and background music
│   └── facts.json               # Educational facts displayed between rounds
├── core/                        # Core game mechanics and logic
│   ├── game_manager.py          # Handles the game loop and main logic
│   ├── events.py                # Defines random event mechanics
│   ├── health_system.py         # Manages reef health calculations
│   ├── player_actions.py        # Processes player inputs and actions
│   └── thresholds.py            # Threshold logic for environmental factors
├── ui/                          # User interface components
│   ├── main_menu.py             # Main menu screen
│   ├── game_screen.py           # Game screen with sliders and visuals
│   ├── game_over_screen.py      # Game over screen
│   └── helpers.py               # UI utility functions (e.g., button rendering)
├── visuals/                     # Visual and animation handling
│   ├── background_manager.py    # Dynamically updates reef visuals
│   ├── animations.py            # Handles fish and coral animations
│   └── visual_feedback.py       # Provides feedback on health changes
├── audio/                       # Audio handling
│   ├── sound_manager.py         # Manages background music and sound effects
│   └── audio_feedback.py        # Plays sounds for events or actions
├── tests/                       # Testing modules
│   ├── test_events.py           # Tests for event mechanics
│   ├── test_health_system.py    # Tests for health calculations
│   └── test_player_actions.py   # Tests for player actions
└── README.md                    # Instructions for setting up and playing the game
```

---

#### Functional Overview

##### **Core Modules**

1. **game_manager.py**:
   - Manages the game loop, state transitions, and overall flow.
   - Coordinates interactions between health systems, events, and player actions.
   - Provides an interface to manage the progression of rounds, ensuring proper initialization and closure of each game phase.
   - Implements timer-based mechanisms to manage event durations and intervals between rounds.
   - Includes debugging tools to log the state of the game during each phase for easier troubleshooting.

2. **events.py**:
   - Defines random events with their triggers, impacts, and durations.
   - Supports both positive and negative events, providing variety to gameplay.
   - Includes functionality to calculate the probability of event occurrences based on game difficulty and progression.
   - Categorizes events by type (e.g., natural, human-induced) to enhance storytelling and player education.
   - Manages visual and auditory cues for events to enhance player immersion and clarity.

3. **health_system.py**:
   - Calculates health changes dynamically based on player actions, environmental adjustments, and event effects.
   - Tracks a real-time health metric, ensuring immediate feedback to players.
   - Integrates thresholds logic from `thresholds.py` to enforce the impact of exceeding critical environmental levels.
   - Maintains a history of health changes for debugging and balancing gameplay.
   - Provides a predictive model to warn players of potential negative outcomes based on current trends.

4. **player_actions.py**:
   - Handles adjustments from sliders for factors like temperature, salinity, and pH.
   - Validates player inputs to ensure changes are within permissible ranges.
   - Applies corresponding effects to the reef health based on input validity and alignment with optimal values.
   - Provides error handling for invalid inputs and feedback mechanisms to guide players.
   - Records player actions to generate a performance summary at the end of the game.

5. **thresholds.py**:
   - Encapsulates logic for thresholds defined in the design document.
   - Provides methods to evaluate current environmental factors against predefined thresholds.
   - Offers utility functions to calculate the severity of penalties or bonuses when thresholds are breached.
   - Integrates with other modules to trigger appropriate visual and audio feedback when critical conditions are met.
   - Supports dynamic adjustment of thresholds to increase difficulty as the game progresses.

##### **UI Modules**

1. **main_menu.py**:
   - Displays start, instructions, and quit options.
   - Provides a seamless transition to the game screen.
   - Includes an options menu to adjust game settings, such as difficulty and audio preferences.

2. **game_screen.py**:
   - Renders health stats, sliders, and event descriptions.
   - Updates visuals dynamically based on the game state.
   - Includes tooltips to explain the purpose of each slider and its impact on the reef.

3. **game_over_screen.py**:
   - Shows win/lose messages and final statistics.
   - Provides the option to replay the game or return to the main menu.
   - Highlights educational elements to reinforce learning outcomes.

4. **helpers.py**:
   - Provides reusable UI functions (e.g., button rendering, text alignment).
   - Includes utilities for scaling UI elements dynamically based on screen resolution.

##### **Visuals**

1. **background_manager.py**:
   - Updates reef visuals based on health levels.
   - Supports transitions between different states (e.g., thriving reef to bleached reef).
   - Integrates animations from `animations.py` for enhanced player immersion.

2. **animations.py**:
   - Handles animations for fish, coral growth, and events.
   - Uses frame-based animation techniques to ensure smooth transitions.
   - Includes customizable animation sequences for future expansions.

3. **visual_feedback.py**:
   - Provides visual cues for health gains/losses.
   - Includes color-coded indicators to show critical conditions (e.g., red for danger, green for improvement).

##### **Audio**

1. **sound_manager.py**:
   - Plays background music and manages sound effects.
   - Ensures audio synchronization with game events.
   - Includes a library of oceanic and environmental sounds for atmospheric immersion.

2. **audio_feedback.py**:
   - Adds sound effects for specific actions or random events.
   - Provides auditory feedback for player success or failure, enhancing engagement.

---

#### Next Steps

1. **Phase 1**:
   - Set up the directory structure and `pygame` framework.
2. **Phase 2**:
   - Implement `main.py` with the basic game loop and integrate initial modules (`game_manager.py`, `health_system.py`, `events.py`).
3. **Phase 3**:
   - Add sliders, visuals, and event handling.
4. **Phase 4**:
   - Enhance audio and animations.

This structure ensures modularity, making the game maintainable and scalable. Each component is clearly defined for a focused development approach.

