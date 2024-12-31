# Coral Reef Survival Simulator

An educational game where players manage and protect a coral reef ecosystem by maintaining optimal environmental conditions.

## Description

The Coral Reef Survival Simulator is an interactive educational game that teaches players about coral reef ecosystems and the environmental factors that affect their health. Players must balance temperature, pH levels, and salinity to keep the coral reef healthy while dealing with various environmental events.

## Features

- Real-time environmental management system
- Dynamic coral reef visualization
- Realistic fish animations with multiple species
- Random environmental events
- Educational facts about coral reefs
- Achievement system
- Power-up system
- Particle effects for visual feedback
- Ambient ocean sounds and effects

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/coral-reef-simulator.git
cd coral-reef-simulator
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python main.py
```

## Game Controls

- Use sliders to adjust environmental parameters:
  - Temperature (23-29°C)
  - pH levels (8.0-8.4)
  - Salinity (32-36 ppt)
- Click through tutorial messages
- Monitor health bar and event notifications
- Watch for achievements and power-ups

## Project Structure

```
coral-reef-simulator/
├── assets/
│   ├── images/
│   │   └── fish/
│   ├── sounds/
│   └── facts.json
├── core/
│   ├── health_system.py
│   ├── events.py
│   ├── player_actions.py
│   ├── achievements.py
│   ├── power_ups.py
│   ├── facts_manager.py
│   └── __init__.py
├── ui/
│   ├── game_screen.py
│   ├── main_menu.py
│   ├── game_over_screen.py
│   ├── tutorial_overlay.py
│   └── __init__.py
├── visuals/
│   ├── animations.py
│   ├── background_manager.py
│   ├── particle_system.py
│   ├── visual_feedback.py
│   └── __init__.py
├── audio/
│   ├── sound_manager.py
│   └── __init__.py
├── config.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Dependencies

- Python 3.8+
- Pygame 2.5.2
- NumPy 1.24.3
- Pillow 10.0.0

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Educational content sourced from marine biology research
- Fish images should be credited to their respective owners
- Sound effects from [source]

## Future Improvements

- Additional coral species
- More environmental factors
- Multiplayer mode
- Advanced weather systems
- Detailed statistics tracking
- Mobile support