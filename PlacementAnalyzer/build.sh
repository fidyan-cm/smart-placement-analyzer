#!/bin/bash
python generate_dataset.py
python train_model.py
python manage.py collectstatic --no-input
python manage.py migrate