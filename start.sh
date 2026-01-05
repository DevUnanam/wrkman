#!/usr/bin/env bash
gunicorn artisan_marketplace.wsgi:application --bind 0.0.0.0:$PORT