# Sokoban Solver

> Project to solve sokoban puzzle using search algorithm, with CLI and GUI mode.

Some sokoban will never be solved, therefore this project is born.
## Installation

### Local setup

#### Pip/venv

```bash
# First, you need to have Python(>=3.5) installed on your system
$ python --version
Python 3.10.6

# Clone this repo
$ git clone https://github.com/DepressingWeeb/Sokopan-Search.git

# Create venv
$ python -m venv venv

# Activate venv
$ source venv/bin/activate
# For windows, use venv/Scripts/activate

# Install the dependencies
$ pip install -r requirements.txt
```

## Usage

### GUI mode (default)

```bash
$ python main.py --mode gui
# or python main.py
```

### CLI mode
#### For solving all input in levels folder
```bash
$ python main.py --mode cli
```
#### For solving a specific input
```bash
$ python main.py --mode cli --path levels/input-01.txt
```

### Options

```text
-h, --help                                   show this help message and exit
-m, --mode {gui,cli}
                                             Run the script in 'cli' mode or 'gui' mode
-p, --path PATH [PATH ...]                   Path to a level(txt) file if using cli mode

```
### Contributors/Collaborators
<a href="https://github.com/DepressingWeeb/Sokopan-Search/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DepressingWeeb/Sokopan-Search" />
</a>
