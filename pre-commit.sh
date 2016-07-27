#!/bin/bash

sed -i 's/^SOURCE\s.*/SOURCE = '\''source.mkv'\''/g' compare.py
sed -i 's/^ENCODE\s.*/ENCODE = '\''encode.mkv'\''/g' compare.py
