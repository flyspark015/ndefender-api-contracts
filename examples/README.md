# Examples ✅

## curl examples

Set environment variables:
```bash
export BASE_URL=http://127.0.0.1:8001/api/v1
```

Run:
```bash
./curl_health.sh
./curl_status.sh
./curl_contacts.sh
```

Command example:
```bash
export VRX_ID=1
export FREQ_HZ=5740000000
./curl_command_vrx_tune.sh
```

Dangerous command:
```bash
./curl_command_reboot.sh
```

## WebSocket example client

Requires:
```bash
pip install websockets
```

Run:
```bash
python3 ws_client.py --url ws://127.0.0.1:8001/api/v1/ws
```
