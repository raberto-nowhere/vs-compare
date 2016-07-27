#!/bin/bash

sed -i 's/^SOURCE.*/SOURCE = '\''source.mkv'\''/g' compare.py
sed -i 's/^ENCODE.*/ENCODE = '\''encode.mkv'\''/g' compare.py
