# Matrix Rain Effect (Terminal)

A continuous **Matrix-style digital rain effect** rendered directly in the terminal using **Python**.  
Works on **Linux, macOS**, and **Windows** (with a small dependency).

---

## Features

- Continuous Matrix rain (no empty gaps)
- Bright head with fading trails
- Dynamic terminal resize support
- Unicode + ASCII character mix
- Smooth animation
- Quit anytime using `q` or `Ctrl+C`

---

## Demo

> Run in a full-size terminal for the best visual effect.

---

## Requirements

- Python **3.7+**
- Terminal that supports colors

### Platform Support

| OS       | Supported | Notes                     |
|----------|-----------|---------------------------|
| Linux    | ✅ Yes    | Works out of the box      |
| macOS    | ✅ Yes    | Works out of the box      |
| Windows  | ✅ Yes    | Requires `windows-curses` |

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/your-username/matrix-rain-terminal.git
cd matrix-rain-terminal
```

## Controls

- **q** → Quit the animation
- **Ctrl + C** → Force exit

## Configuration

You can tweak these values at the top of the script:
| Animation | Discription |
|------------------------|----------------------------------------|
| TICK = `0.06 `           | Animation speed (lower = faster)       |
| SPAWN_MIN_INTERVAL = `1` | Minimum delay between drops per column |
| SPAWN_MAX_INTERVAL = `6` | Maximum delay between drops per column |
| MAX_TRAIL = `8`          | Length of each rain trail              |
| INTENSITY_DECAY = `1`    | Trail fade speed                       |

## License

MIT License — free to use, modify, and distribute.