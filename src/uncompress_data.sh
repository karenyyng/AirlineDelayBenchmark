#!/bin/bash

ls ../data/*.csv.bz2 | xargs bzip -d 
