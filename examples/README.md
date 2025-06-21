# MQTT Payload Examples

This directory contains practical examples of MQTT payloads for the Unified Namespace (UNS) architecture.

## Python Example: Pump MQTT Publisher

The `pump_mqtt_publisher.py` script demonstrates how to publish realistic MQTT payloads for an industrial pump using all schema types.

### Features

- **Complete Schema Coverage**: Demonstrates all 10 payload types
- **Realistic Data**: Generates realistic pump data with configurable variations
- **Environment Configuration**: Uses `.env` files for secure configuration
- **Comprehensive Logging**: Detailed console output for monitoring

### Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   ```bash
   cp ../example.env .env
   # Edit .env with your MQTT broker settings
   ```

3. **Run the Example:**
   ```bash
   python pump_mqtt_publisher.py
   ```

### Configuration

All environment variables used by the script are defined in the `../example.env` file. To configure your environment:

1. **Duplicate the example file:**
   ```bash
   cp ../example.env .env
   ```
2. **Edit `.env`** with your MQTT broker settings, credentials, and any other options you wish to change.

**Environment variables include:**
- `MQTT_BROKER_HOST`: MQTT broker address
- `MQTT_BROKER_PORT`: MQTT broker port
- `MQTT_USE_TLS`: Enable TLS/SSL (true/false)
- `MQTT_USE_AUTH`: Enable authentication (true/false)
- `MQTT_BROKER_USERNAME`: Authentication username
- `MQTT_BROKER_PASSWORD`: Authentication password
- `MQTT_CLIENT_ID`: MQTT client ID
- `MQTT_KEEPALIVE`: Keepalive interval
- `MQTT_QOS`: Quality of Service level
- `ASSET_ID`, `ASSET_NAME`, `ASSET_DESCRIPTION`: Pump asset configuration
- `PUBLISH_INTERVAL`: Seconds between publish cycles
- `SIMULATION_MODE`: Enable random data variation (true/false)
- `LOG_LEVEL`: Logging level (e.g., INFO, DEBUG)

For a full list and descriptions, see the comments in `../example.env`.

### Output

The script publishes to topics following the UNS structure:
```
abelara/plant1/utilities/water-system/pump-station/pump-101/{schemaType}
```

Example topics:
- `.../definition` - Asset configuration
- `.../state` - Pump operational state
- `.../edge/temperature` - Real-time temperature readings
- `.../measurement/bearing-temperature` - Precision maintenance data
- `.../count/runtime-hours` - Accumulated runtime
- `.../kpi/oee` - Performance metrics
- `.../alert` - System alerts
- `.../production` - Production tracking

### Schema Types Demonstrated

1. **Asset Definition** - Pump configuration and metadata
2. **State** - Operational states (Running, Stopped, Fault, etc.)
3. **Edge** - Real-time sensor data (temperature, pressure, flow)
4. **Measurement** - Precision maintenance measurements
5. **Count** - Accumulated values (runtime, production, energy)
6. **KPI** - Performance indicators (OEE, efficiency)
7. **Alert** - System notifications and alarms
8. **Product** - Product specifications
9. **Production** - Production run tracking

### Customization

To adapt this example for your own equipment:

1. Modify the asset configuration variables
2. Adjust the data generation functions for your specific sensors
3. Update the topic structure to match your UNS hierarchy
4. Customize the payload content for your use case

### Troubleshooting

- **Connection Issues**: Check your MQTT broker settings in `.env`
- **Authentication Errors**: Verify username/password in `.env`
- **TLS Issues**: Set `MQTT_USE_TLS=true` for secure connections
- **Topic Errors**: Ensure your broker supports the topic structure

For more information, see the main [README](../README.md). 