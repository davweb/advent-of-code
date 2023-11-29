# Advent of Code

These are my solutions to the annual [Advent of Code][1] puzzles.

These are not by any means exemplary or optimal solutions.  Mostly, I've done enough in each case to solve the problems in a reasonable period of time, tidied up the code a little and stopped there.  Additionally, some problems remain unsolved.

## Details

Everything is in Python 3.  The code has [`doctest`][3] style tests as they are quick and easy to write when working on a problem.

The code is under the `advent` module with each year having its own submodule.  Common code for each year is in the submodule and general utilities are in `advent`.

Each day is a separate submodule called `day<n>` under each year.  When executed they will output the answers to the standard output.  The day modules will usually contain the following functions:
* `main` - the entry point
* `part1` - solves the first part of the problem
* `part2` - solves the second part of the problem
* `read_input` - reads and parses the puzzle input

The `input` directory contains copies of the input for most days (which will be specific to me).

The `template.py` file is a template for quickly creating a script for each day.

## CI Pipeline

There is a CI pipeline that runs the tests, lints the code and checks its formatting.

[![Build Status](https://github.com/davweb/advent-of-code/workflows/CI/badge.svg)][2]

[1]: https://adventofcode.com/
[2]: https://github.com/davweb/advent-of-code/actions
[3]: https://docs.python.org/3/library/doctest.html

