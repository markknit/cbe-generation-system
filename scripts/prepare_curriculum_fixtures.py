#!/usr/bin/env python3
"""Copy frozen reviewed pilot records into an explicitly isolated workspace."""
import argparse
from pathlib import Path
from curriculum.fixtures import prepare

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--workspace',type=Path,default=Path('/tmp/cbe-preparation-fixture'))
args=parser.parse_args()
prepare(args.workspace.resolve())
print('Prepared reviewed reference copies in',args.workspace.resolve())
