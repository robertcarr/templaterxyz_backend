#!/usr/bin/env bash

./manage.py dumpdata \
--indent 4 \
--natural-foreign \
-e contenttypes \
-e admin \
-e auth.Permission \
> fixtures/default.json