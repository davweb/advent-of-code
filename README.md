# Advent of Code

These are my solutions to the annual [Advent of Code][1] puzzles.

These are not by any means exemplary or optimal solutions.  Mostly, I've done enough in each case to solve the problems in a reasonable period of time, tidied up the code a little and stopped there.  Additionally, some problems remain unsolved.

## Details

Everything is in Python 3.  The code has [`doctest`][3] style tests as they are quick and easy to write when working on a problem.

The code is under the `advent` module with each year having its own submodule.  Common code for each year is in the submodule and general utilities are in `advent`.


## CI Pipeline

There is a CI pipeline that runs the tests, lints the code and checks its formatting.

[![Build Status](https://github.com/davweb/advent-of-code/workflows/CI/badge.svg)][2]

[1]: https://adventofcode.com/
[2]: https://github.com/davweb/advent-of-code/actions
[3]: https://docs.python.org/3/library/doctest.html

