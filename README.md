# PMT Profiler

A Python package for analyzing analog PMT devices used for TCSPC
using Micro-Manager controlled Becker-Hickl Detecter Control Card DCC-100
and Swabian Time-Tagger Ultra.

## Features

- PMT control functionality
- Mock mode for testing without hardware

## Installation

```bash
# Install from source
pip install -e .
```

## Usage

### Basic Usage

```bash
python -m pmt_profiler.cli --pmt start --gain 65 --channel C3
```

### Available Commands

- `--pmt`: Control PMT operations (`start` or `stop`)
- `--gain`: Set PMT gain (default: 65)
- `--channel`: Specify PMT channel (default: C3)
- `--mock`: Use mock Micro-Manager for testing

### Examples

Start PMT with gain 65 on channel C3:
```bash
python -m pmt_profiler.cli --pmt start --gain 65 --channel C3
```

Stop PMT on channel C3:
```bash
python -m pmt_profiler.cli --pmt stop --channel C3
```

Run in mock mode (no hardware required):
```bash
python -m pmt_profiler.cli --mock --pmt start --gain 65
```

## Project Structure

- `pmt_profiler/`: Main package directory
  - `cli.py`: Command-line interface
  - `core.py`: Core functionality and Micro-Manager interface
  - `pmt.py`: PMT control functions


## Mock Mode

The tool includes a mock mode for development and testing without hardware:

```python
from pmt_profiler.core import MockMicroManager

# Use mock Micro-Manager
mmc = MockMicroManager()
```

## Hardware Mode

For real hardware operation:

```python
from pmt_profiler.core import MicroManager

# Use real Micro-Manager
mmc = MicroManager()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 