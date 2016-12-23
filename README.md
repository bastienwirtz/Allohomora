# Allohomora
Raspberry pi based connected doorbell

![schema](/schema/path/to/allohomora.png?raw=true)

## Run

```gunicorn --bind 0.0.0.0:5000 --worker-class eventlet -w 1 run:app```
