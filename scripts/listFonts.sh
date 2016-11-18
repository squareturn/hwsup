#!/bin/bash

convert -list font | awk '$1 == "Font:" { print $2 }'
