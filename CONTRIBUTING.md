# Contributing
## Reporting Issues
Report issues [here](https://github.com/wieden-kennedy/boxel/issues/new)
## Submitting Changes
Branch and submit a pull request. Try to keep it **PEP8**.
## Running the Tests
Unit tests are in the ```tests/``` directory and can be run by ```nosetests -v```
## Running benchmark tests
To run analysis use the benchmark flag with a command:
```bash
python -m boxel.boxel --benchmark COMMAND
```
This will ouput benchmark file in ```benchmarks/``` named as profileN.txt with N being
the largest number in the directory.
To view results:
```bash
cprofile -f benchmarks/<FILE>.txt
```
Then visit localhost:4000 in a browser.
