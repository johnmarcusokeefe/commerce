#!/bin/bash
echo "running batch git"
git add .
if [$0 == ""]; then
    git commit -m "batch commit"
else
    git commit -m $0
fi
git push
echo "finish batch git"
