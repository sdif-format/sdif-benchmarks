#!/usr/bin/env python3
import sys
from sdif_benchmarks.generators.generate_semantic_golden import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
