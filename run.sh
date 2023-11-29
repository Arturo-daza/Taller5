#!/bin/bash
# uvicorn main:app --host 137.184.45.65 --port 3001
$env:TF_ENABLE_ONEDNN_OPTS=0

uvicorn main:app --reload