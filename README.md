# Fort Lauderdale Roleplay Discord Bot

A Discord bot that monitors voice channels for callsign compliance and runs as a web service.

## Features

- Monitors specific voice channels for users joining without proper callsign format
- Automatically sends reminder messages to users with invalid nicknames
- Runs as a web service with health check endpoints
- Supports LEO, Fire, and EMS callsign formats

## Deployment

### Requirements
- Python 3.8+
- Discord bot token
- Channel and role IDs configured in `app.py`

### Local Development
```bash
pip install -r requirements.txt
python app.py
```

### Production Deployment (Heroku/Render/etc.)
1. Ensure all files are in your repository
2. Set environment variables if needed
3. Deploy using the platform's standard deployment process

## API Endpoints

- `GET /` - Service status and information
- `GET /health` - Health check endpoint
- `GET /status` - Bot connection status and configuration

## Configuration

Update the following variables in `app.py`:
- `TOKEN` - Your Discord bot token
- `PING_CHANNEL_ID` - Channel where violation messages are sent
- `ALLOWED_ROLES` - Role IDs that bypass checks
- `MONITORED_VC_CHANNELS` - Voice channel IDs to monitor

## Supported Callsign Formats

- LEO: `7D-###`, `8D-###`, `9D-###`
- Fire: `PUMP-#`, `AER-#`, `TANK-#`
- EMS: `EMS-#`, `AMB-#`, `E-#`
- Other: `TOW-#`, `PLOW-#`
