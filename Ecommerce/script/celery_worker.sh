#!/usr/bin/env bash

# echo "entrou"
#cd ../../venv_Ecommerce/bin
#.activate
celery -A Ecommerce worker -l info