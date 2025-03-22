#!/bin/bash

while true; do
	mv logs "pre_$(date +'%s')_logs" 2> /dev/null
	PYTHONUNBUFFERED=1 python3 src/main.py &> logs < /dev/null
done & disown
