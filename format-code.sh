#!/bin/bash


autopep8 --in-place --aggressive --aggressive --max-line-length 120 -r ${1:-advent}
