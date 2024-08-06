# PiddiPlatsch

[![image](https://img.shields.io/pypi/v/piddiplatsch.svg)](https://pypi.python.org/pypi/piddiplatsch)


Demo project for a PID consumer.

-   Free software: Apache Software License 2.0

## Features

-   TODO

## Testing

Start "vanilla" rabbitmq with docker:

```
./run_rabbit.sh
```

Check management web page:
http://localhost:15672/

Login with guest/guest.

Install piddiplatsch consumer:

```
mamba env create
conda activate piddiplatsch
pip install -e .
```

Check available commands:
```
piddiplatsch --help
```

Start consumer:
```
piddiplatsch consume --help
piddiplatsch consume --dry-run
```

Send a message to the rabbit queue:
```
piddiplatsch send --help
piddiplatsch send -e wdcc.test examples/wdcc.json
piddiplatsch send -e wdcc.test examples/wdcc_invalid.json
piddiplatsch send -e cmip6.test examples/cmip6.json
```

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
