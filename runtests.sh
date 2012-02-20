#!/bin/bash

tests=`(cd tests; ls *.py | grep -v __init__)`
for test in $tests; do
    echo "Running test: $test"
    python -m tests.${test%.py}
done
