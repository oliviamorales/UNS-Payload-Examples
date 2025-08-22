#!/usr/bin/env python3
"""
Tank MQTT Publisher - Abelara MES Schema Examples

This script publishes realistic water tank MQTT payloads to demonstrate all schema types.
Configure your broker details in the .env file and run.

Usage:
    python tank_mqtt_publisher.py

Requirements:
    pip install paho-mqtt python-dotenv
"""

import json
import time
import random
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import logging
from jsonschema import validate, ValidationError

# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================

# Load environment variables from .env file
load_dotenv()

# MQTT Broker Configuration
BROKER_ADDRESS = os.getenv("MQTT_BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
USERNAME = os.getenv("MQTT_BROKER_USERNAME", "")
PASSWORD = os.getenv("MQTT_BROKER_PASSWORD", "")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "uns-tank-example")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))
MQTT_QOS = int(os.getenv("MQTT_QOS", "1"))

# MQTT Topic Configuration
MQTT_TOPIC_ENTERPRISE = os.getenv("MQTT_TOPIC_ENTERPRISE", "abelara")
MQTT_TOPIC_SITE = os.getenv("MQTT_TOPIC_SITE", "plant1")
MQTT_TOPIC_AREA = os.getenv("MQTT_TOPIC_AREA", "utilities")
MQTT_TOPIC_LINE = os.getenv("MQTT_TOPIC_LINE", "water-system")
MQTT_TOPIC_CELL = os.getenv("MQTT_TOPIC_CELL", "tank-area")

# Asset Configuration
"""
Asset Configuration for two water tanks
"""
TANKS = [
    {
        "id": 201,
        "name": "Tank-201",
        "description": "Raw water storage tank for process supply",
        "parent_id": 31,
        "parent_name": "Tank Area 1"
    },
    {
        "id": 202,
        "name": "Tank-202",
        "description": "Treated water tank for distribution",
        "parent_id": 31,
        "parent_name": "Tank Area 1"
    }
]

# Publisher Configuration
PUBLISH_INTERVAL = int(os.getenv("PUBLISH_INTERVAL", "5"))
ENABLE_RANDOM_VARIATION = os.getenv("SIMULATION_MODE", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Optional: TLS/SSL Configuration
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "false").lower() == "true"
MQTT_CA_CERT_PATH = os.getenv("MQTT_CA_CERT_PATH", "")
MQTT_CLIENT_CERT_PATH = os.getenv("MQTT_CLIENT_CERT_PATH", "")
MQTT_CLIENT_KEY_PATH = os.getenv("MQTT_CLIENT_KEY_PATH", "")

# Optional: Authentication
MQTT_USE_AUTH = os.getenv("MQTT_USE_AUTH", "false").lower() == "true"

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# =============================================================================
# SCHEMA VALIDATION
# =============================================================================

def load_schemas():
    """Load all JSON schemas for validation"""
    schemas = {}
    schema_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')
    
    schema_files = {
        'asset': 'asset/asset.json',
        'alert': 'alert/alert.json',
        'state': 'state/state.json',
        'measurement': 'measurement/measurement.json',
        'count': 'count/count.json',
        'kpi': 'kpi/kpi.json',
        'product': 'product/product.json',
        'production': 'production/production.json',
        'reading': 'reading/reading.json',
        'value': 'value/value.json'
    }
    
    for schema_name, schema_path in schema_files.items():
        try:
            full_path = os.path.join(schema_dir, schema_path)
            with open(full_path, 'r') as f:
                schemas[schema_name] = json.load(f)
            logger.debug(f"Loaded schema: {schema_name}")
        except Exception as e:
            logger.warning(f"Could not load schema {schema_name}: {e}")
    
    return schemas

def validate_payload(payload, schema_name, schemas):
    """Validate a payload against its schema"""
    if schema_name not in schemas:
        logger.warning(f"No schema found for {schema_name}, skipping validation")
        print(f"⚠️  No schema found for {schema_name}, skipping validation")
        return True
    
    try:
        validate(instance=payload, schema=schemas[schema_name])
        return True
    except ValidationError as e:
        logger.error(f"Schema validation failed for {schema_name}: {e}")
        print(f"❌ Schema validation failed for {schema_name}:")
        print(f"   Error: {e.message}")
        print(f"   Path: {' -> '.join(str(p) for p in e.absolute_path) if e.absolute_path else 'root'}")
        if e.validator_value:
            print(f"   Expected: {e.validator_value}")
        return False

# Load schemas at startup
SCHEMAS = load_schemas()

# =============================================================================
# MQTT CLIENT SETUP
# =============================================================================

def on_connect(client, userdata, flags, rc):
    """Called when connected to MQTT broker"""
    if rc == 0:
        logger.info(f"Connected to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT}")
        print(f"✅ Connected to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT}")
    else:
        logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")
        print(f"❌ Failed to connect to MQTT broker. Return code: {rc}")

def on_publish(client, userdata, mid):
    """Called when message is published"""
    logger.debug(f"Published message ID: {mid}")
    print(f"📤 Published message ID: {mid}")

def on_disconnect(client, userdata, rc):
    """Called when disconnected from MQTT broker"""
    logger.info(f"Disconnected from MQTT broker. Return code: {rc}")
    print(f"🔌 Disconnected from MQTT broker. Return code: {rc}")

# Create MQTT client
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Set authentication if provided
if MQTT_USE_AUTH and USERNAME and PASSWORD:
    client.username_pw_set(USERNAME, PASSWORD)

# Enable TLS/SSL if configured
if MQTT_USE_TLS:
    if MQTT_CA_CERT_PATH and MQTT_CLIENT_CERT_PATH and MQTT_CLIENT_KEY_PATH:
        # Use certificate-based TLS
        client.tls_set(
            ca_certs=MQTT_CA_CERT_PATH,
            certfile=MQTT_CLIENT_CERT_PATH,
            keyfile=MQTT_CLIENT_KEY_PATH
        )
    else:
        # Use basic TLS without certificates
        client.tls_set()
        client.tls_insecure_set(True)  # Allow self-signed certificates

# =============================================================================
# TANK DATA GENERATION
# =============================================================================

def get_timestamp():
    """Get current ISO 8601 timestamp"""
    return datetime.now(timezone.utc).isoformat()

def add_variation(base_value, variation_percent=3):
    """Add realistic variation to values"""
    if not ENABLE_RANDOM_VARIATION:
        return base_value
    variation = base_value * (variation_percent / 100)
    return base_value + random.uniform(-variation, variation)

# =============================================================================
# SCHEMA PAYLOADS
# =============================================================================

def create_asset_payload(tank):
    """Create Asset schema payload for a given tank"""
    return {
        "timestamp": get_timestamp(),
        "id": tank["id"],
        "name": tank["name"],
        "description": tank["description"],
        "assetType": {
            "id": 2,
            "name": "Water Tank",
            "description": "Water storage tank equipment"
        },
        "parentAsset": {
            "id": tank["parent_id"],
            "name": tank["parent_name"],
            "description": "Primary water tank area"
        },
        "metadata": {
            "source": "asset-management",
            "uri": f"asset://{tank['id']}",
            "additionalInfo": {
                "manufacturer": "Pentair",
                "model": "WT-5000",
                "serialNumber": f"PT-2023-00{tank['id']}",
                "installationDate": "2023-04-10",
                "capacity": "5000 m³",
                "material": "Stainless Steel",
                "maxLevel": "5.0 m",
                "diameter": "10 m",
                "height": "6 m"
            }
        }
    }

def create_state_payload(tank):
    """Create State schema payload for a given tank"""
    states = [
        {"id": 1, "name": "Filling", "description": "Tank is being filled", "color": "#00BFFF"},
        {"id": 2, "name": "Full", "description": "Tank is full", "color": "#228B22"},
        {"id": 3, "name": "Emptying", "description": "Tank is being emptied", "color": "#FFD700"},
        {"id": 4, "name": "Low Level", "description": "Tank water level is low", "color": "#FF4500"},
        {"id": 5, "name": "Maintenance", "description": "Tank under maintenance", "color": "#800080"}
    ]
    current_state = random.choice(states)
    previous_state = random.choice([s for s in states if s["id"] != current_state["id"]])
    return {
        "timestamp": get_timestamp(),
        "description": f"Tank is {current_state['name'].lower()}",
        "color": current_state["color"],
        "type": {
            "id": current_state["id"],
            "name": current_state["name"],
            "description": current_state["description"]
        },
        "metadata": {
            "source": "plc-controller",
            "uri": "opc://plc1/DB1.DBW10",
            "asset": {
                "id": tank["id"],
                "name": tank["name"],
                "description": tank["description"]
            },
            "previousState": {
                "id": previous_state["id"],
                "name": previous_state["name"],
                "description": previous_state["description"],
                "color": previous_state["color"],
                "type": {
                    "id": previous_state["id"],
                    "name": previous_state["name"],
                    "description": previous_state["description"]
                }
            },
            "additionalInfo": {
                "runTime": random.randint(500, 3000),
                "lastFillTime": datetime.now(timezone.utc).isoformat(),
                "mode": random.choice(["AUTO", "MANUAL"]),
                "operator": random.choice(["Alice Brown", "Tom Lee", "Eva Green"])
            }
        }
    }

def create_measurement_payloads(tank):
    """Create multiple Measurement schema payloads for water tank maintenance and operator rounds"""
    measurement_types = [
        {"id": 1, "name": "Water Level", "description": "Tank water level measurement", "unit": "m", "base_value": 3.8, "target": 4.5, "topic_suffix": "water-level", "location": "Tank Center"},
        {"id": 2, "name": "Temperature", "description": "Water temperature measurement", "unit": "°C", "base_value": 18.5, "target": 20.0, "topic_suffix": "temperature", "location": "Tank Bottom"},
        {"id": 3, "name": "pH", "description": "Water pH measurement", "unit": "pH", "base_value": 7.2, "target": 7.0, "topic_suffix": "ph", "location": "Tank Outlet"},
        {"id": 4, "name": "Conductivity", "description": "Water conductivity measurement", "unit": "µS/cm", "base_value": 320, "target": 300, "topic_suffix": "conductivity", "location": "Tank Outlet"},
        {"id": 5, "name": "Volume", "description": "Tank water volume measurement", "unit": "m³", "base_value": 4200, "target": 5000, "topic_suffix": "volume", "location": "Tank Center"}
    ]
    
    payloads = []
    for measurement in measurement_types:
        value = add_variation(measurement["base_value"])
        tolerance = measurement["target"] * 0.10  # 10% tolerance for tank measurements
        in_tolerance = abs(value - measurement["target"]) <= tolerance
        
        payload = {
            "timestamp": get_timestamp(),
            "type": {
                "id": measurement["id"],
                "name": measurement["name"],
                "description": measurement["description"]
            },
            "value": round(value, 2),
            "unit": measurement["unit"],
            "target": measurement["target"],
            "tolerance": round(tolerance, 2),
            "inTolerance": in_tolerance,
            "metadata": {
                "source": "tank-maintenance",
                "uri": f"maintenance://{tank['name'].lower()}/{measurement['name'].lower().replace(' ', '-')}",
                "asset": {
                    "id": tank["id"],
                    "name": tank["name"],
                    "description": tank["description"]
                },
                "additionalInfo": {
                    "technician": random.choice(["Alice Brown", "Tom Lee", "Eva Green", "Sam Carter"]),
                    "measurementMethod": random.choice(["Ultrasonic", "Thermocouple", "pH Meter", "Conductivity Probe"]),
                    "equipmentUsed": random.choice(["Endress+Hauser", "Hach HQ40d", "Siemens Probe"]),
                    "measurementDate": datetime.now(timezone.utc).isoformat(),
                    "nextMeasurementDue": "2025-06-15",
                    "trend": random.choice(["Stable", "Rising", "Falling"]),
                    "measurementLocation": measurement["location"]
                }
            },
            "product": {
                "id": 2,
                "name": "Process Water",
                "description": "Water for manufacturing process",
                "family": {
                    "id": 1,
                    "name": "Utilities",
                    "description": "Utility products and services"
                }
            },
            "productionContext": {
                "batchId": f"TANK-2025-{random.randint(1, 999):03d}",
                "processStep": "Tank Maintenance",
                "demand": random.choice(["Scheduled", "Emergency"])
            }
        }
        
        payloads.append((measurement["topic_suffix"], payload, f"{measurement['name']} measurement"))
    
    return payloads

def create_edge_payloads(tank):
    """Create multiple Edge schema payloads for tank process readings"""
    edge_types = [
        {"id": 1, "name": "Inflow Rate", "description": "Water inflow rate", "unit": "m³/h", "base_value": 38.5, "topic_suffix": "inflow-rate", "location": "Inlet Pipe"},
        {"id": 2, "name": "Outflow Rate", "description": "Water outflow rate", "unit": "m³/h", "base_value": 36.2, "topic_suffix": "outflow-rate", "location": "Outlet Pipe"},
        {"id": 3, "name": "Temperature", "description": "Water temperature", "unit": "°C", "base_value": 18.5, "topic_suffix": "temperature", "location": "Tank Bottom"},
        {"id": 4, "name": "Pressure", "description": "Tank pressure", "unit": "bar", "base_value": 1.2, "topic_suffix": "pressure", "location": "Tank Top"},
        {"id": 5, "name": "Valve Position", "description": "Outlet valve position", "unit": "%", "base_value": 85, "topic_suffix": "valve-position", "location": "Outlet Valve"}
    ]
    
    payloads = []
    for edge_type in edge_types:
        value = add_variation(edge_type["base_value"])
        
        payload = {
            "timestamp": get_timestamp(),
            "type": {
                "id": edge_type["id"],
                "name": edge_type["name"],
                "description": edge_type["description"]
            },
            "value": round(value, 2),
            "unit": edge_type["unit"],
            "metadata": {
                "source": f"{edge_type['name'].lower()}-sensor",
                "uri": f"opc://plc1/DB1.DBD{random.randint(40, 60)}",
                "asset": {
                    "id": tank["id"],
                    "name": tank["name"],
                    "description": tank["description"]
                },
                "additionalInfo": {
                    "sensorId": f"{edge_type['name'].upper().replace(' ', '')}-{tank['id']:03d}",
                    "location": edge_type["location"],
                    "alarmThreshold": edge_type["base_value"] * 1.2,
                    "warningThreshold": edge_type["base_value"] * 1.1,
                    "calibrationDate": "2025-01-15",
                    "nextCalibration": "2025-07-15"
                }
            }
        }
        
        payloads.append((edge_type["topic_suffix"], payload, f"{edge_type['name']} reading"))
    
    return payloads

def create_count_payloads(tank):
    """Create multiple Count schema payloads for tank accumulated values"""
    count_types = [
        {"id": 1, "name": "Total Inflow", "description": "Total water inflow to tank", "unit": "m³", "base_value": 12000, "topic_suffix": "total-inflow", "increment": lambda: random.uniform(10, 20)},
        {"id": 2, "name": "Total Outflow", "description": "Total water outflow from tank", "unit": "m³", "base_value": 11800, "topic_suffix": "total-outflow", "increment": lambda: random.uniform(10, 20)},
        {"id": 3, "name": "Fill Cycles", "description": "Number of fill cycles", "unit": "count", "base_value": 45, "topic_suffix": "fill-cycles", "increment": lambda: random.randint(0, 1)},
        {"id": 4, "name": "Drain Cycles", "description": "Number of drain cycles", "unit": "count", "base_value": 44, "topic_suffix": "drain-cycles", "increment": lambda: random.randint(0, 1)}
    ]
    
    payloads = []
    for count_type in count_types:
        increment = count_type["increment"]()
        value = count_type["base_value"] + increment
        
        payload = {
            "timestamp": get_timestamp(),
            "value": round(value, 1) if count_type["unit"] == "m³" else int(value),
            "unit": count_type["unit"],
            "type": {
                "id": count_type["id"],
                "name": count_type["name"],
                "description": count_type["description"]
            },
            "metadata": {
                "source": "tank-counter",
                "uri": "opc://plc1/DB1.DBD50",
                "asset": {
                    "id": tank["id"],
                    "name": tank["name"],
                    "description": tank["description"]
                },
                "production": {
                    "id": random.randint(2000, 2999),
                    "name": f"Tank Operation {random.randint(1, 100)}",
                    "description": "Water tank operation cycle"
                },
                "product": {
                    "id": 2,
                    "name": "Process Water",
                    "description": "Water for manufacturing process"
                },
                "additionalInfo": {
                    "lastMaintenance": "2025-01-15",
                    "nextMaintenance": "2025-06-15",
                    "lastReset": "2025-01-01T00:00:00Z",
                    "nextReset": "2026-01-01T00:00:00Z"
                }
            }
        }
        
        payloads.append((count_type["topic_suffix"], payload, f"{count_type['name']} count"))
    
    return payloads

def create_kpi_payloads(tank):
    """Create multiple KPI schema payloads for tank performance metrics"""
    kpi_types = [
        {"id": 1, "name": "Fill Efficiency", "description": "Tank fill efficiency", "unit": "%", "base_value": 97.5, "topic_suffix": "fill-efficiency"},
        {"id": 2, "name": "Drain Efficiency", "description": "Tank drain efficiency", "unit": "%", "base_value": 96.2, "topic_suffix": "drain-efficiency"},
        {"id": 3, "name": "Water Quality Index", "description": "Water quality index", "unit": "index", "base_value": 98.8, "topic_suffix": "quality-index"}
    ]
    
    payloads = []
    for kpi_type in kpi_types:
        value = add_variation(kpi_type["base_value"])
        
        payload = {
            "timestamp": get_timestamp(),
            "value": round(value, 2),
            "unit": kpi_type["unit"],
            "type": {
                "id": kpi_type["id"],
                "name": kpi_type["name"],
                "description": kpi_type["description"]
            },
            "product": {
                "id": 2,
                "name": "Process Water",
                "description": "Water for manufacturing process",
                "family": {
                    "id": 1,
                    "name": "Utilities",
                    "description": "Utility products and services"
                }
            },
            "metadata": {
                "source": "kpi-calculator",
                "uri": f"kpi://{tank['name'].lower()}/{kpi_type['name'].lower().replace(' ', '-')}",
                "asset": {
                    "id": tank["id"],
                    "name": tank["name"]
                },
                "additionalInfo": {
                    "calculationPeriod": "1 hour",
                    "trend": random.choice(["Improving", "Stable", "Declining"]),
                    "lastCalculation": datetime.now(timezone.utc).isoformat(),
                    "baselineValue": kpi_type["base_value"],
                    "improvement": round((value - kpi_type["base_value"]) / kpi_type["base_value"] * 100, 2)
                }
            }
        }
        
        payloads.append((kpi_type["topic_suffix"], payload, f"{kpi_type['name']} KPI"))
    
    return payloads

def create_alert_payload(tank):
    """Create Alert schema payload for tank"""
    alert_types = [
        {"severity": 2, "code": "LEVEL_LOW", "message": "Tank water level below minimum threshold"},
        {"severity": 3, "code": "LEVEL_HIGH", "message": "Tank water level exceeds maximum threshold"},
        {"severity": 1, "code": "MAINT_DUE", "message": "Tank maintenance due within 50 hours"},
        {"severity": 2, "code": "QUALITY_WARN", "message": "Water quality approaching warning threshold"},
        {"severity": 3, "code": "QUALITY_ALARM", "message": "Water quality exceeds alarm threshold"}
    ]
    
    alert = random.choice(alert_types)
    is_acknowledged = random.choice([True, False])
    
    acknowledgment = {
        "acknowledged": is_acknowledged,
        "acknowledgedBy": random.choice(["Alice Brown", "Tom Lee", "Eva Green"]) if is_acknowledged else None,
        "acknowledgedAt": get_timestamp() if is_acknowledged else None
    }
    
    return {
        "timestamp": get_timestamp(),
        "severity": alert["severity"],
        "code": alert["code"],
        "message": alert["message"],
        "metadata": {
            "source": "monitoring-system",
            "uri": "opc://plc1/DB1.DBD44",
            "asset": {
                "id": tank["id"],
                "name": tank["name"],
                "description": tank["description"]
            },
            "acknowledgment": acknowledgment,
            "additionalInfo": {
                "waterLevel": round(add_variation(3.8), 2),
                "minThreshold": 1.0,
                "maxThreshold": 5.0,
                "sensorLocation": "Tank Center",
                "trend": random.choice(["Rising", "Stable", "Falling"]),
                "timeInAlarm": random.randint(2, 20),
                "recommendedAction": random.choice(["Monitor", "Check sensors", "Schedule maintenance", "Adjust inflow"]),
                "priority": random.choice(["Low", "Medium", "High", "Critical"])
            }
        }
    }

def create_product_payload(tank):
    """Create Product schema payload for tank"""
    return {
        "timestamp": get_timestamp(),
        "id": 2,
        "name": "Process Water",
        "description": "Water for manufacturing process and utilities",
        "idealCycleTime": 3600,
        "tolerance": 0.05,
        "unit": "m³/h",
        "family": {
            "id": 1,
            "name": "Utilities",
            "description": "Utility products and services"
        },
        "metadata": {
            "source": "product-management",
            "uri": "product://process-water",
            "asset": {
                "id": tank["id"],
                "name": tank["name"],
                "description": tank["description"]
            },
            "additionalInfo": {
                "specifications": {
                    "temperature": "10-25°C",
                    "pressure": "1-2 bar",
                    "quality": "Process Grade",
                    "chlorinated": False
                },
                "regulatoryCompliance": ["ISO 14001", "Water Quality Standards"]
            }
        }
    }

def create_production_payload(tank):
    """Create Production schema payload for tank"""
    water_inflow = random.randint(350, 400)
    water_outflow = random.randint(340, 390)
    runtime_hours = random.uniform(5.5, 7.0)
    
    return {
        "timestamp": get_timestamp(),
        "start_ts": datetime.now(timezone.utc).isoformat(),
        "end_ts": None,
        "counts": [
            {
                "type": {
                    "id": 1,
                    "name": "Water Inflow",
                    "description": "Total water inflow to tank",
                    "unit": "m³"
                },
                "quantity": water_inflow,
                "timestamp": get_timestamp()
            },
            {
                "type": {
                    "id": 2,
                    "name": "Water Outflow",
                    "description": "Total water outflow from tank",
                    "unit": "m³"
                },
                "quantity": water_outflow,
                "timestamp": get_timestamp()
            },
            {
                "type": {
                    "id": 3,
                    "name": "Runtime Hours",
                    "description": "Total tank operation hours",
                    "unit": "hours"
                },
                "quantity": round(runtime_hours, 1),
                "timestamp": get_timestamp()
            }
        ],
        "metadata": {
            "source": "production-tracker",
            "uri": f"production://tank-system-2025-{random.randint(1, 999):03d}",
            "asset": {
                "id": tank["id"],
                "name": tank["name"],
                "description": tank["description"]
            },
            "product": {
                "id": 2,
                "name": "Process Water",
                "description": "Water for manufacturing process and utilities",
                "idealCycleTime": 3600,
                "tolerance": 0.05,
                "unit": "m³/h",
                "family": {
                    "id": 1,
                    "name": "Utilities",
                    "description": "Utility products and services"
                }
            },
            "additionalInfo": {
                "shift": random.choice(["Day", "Night", "Weekend"]),
                "operator": random.choice(["Alice Brown", "Tom Lee", "Eva Green", "Sam Carter"]),
                "demandLevel": random.choice(["Low", "Medium", "High"]),
                "systemEfficiency": round(add_variation(97.5), 1),
                "energyConsumption": round(add_variation(28.8), 1),
                "qualityScore": round(add_variation(98.8), 1),
                "plannedProduction": 400,
                "actualProduction": water_outflow,
                "efficiency": round((water_outflow / 400) * 100, 1)
            }
        }
    }

# =============================================================================
# PAYLOAD DEFINITIONS
# =============================================================================

SCHEMA_PAYLOADS = {
    "asset": ("Asset configuration", create_asset_payload),
    "state": ("Tank state", create_state_payload),
    "alert": ("System alert", create_alert_payload),
    "product": ("Product information", create_product_payload),
    "production": ("Production data", create_production_payload),
    "value": ("Value data", None)
}

VALUE_PAYLOADS = {
    "measurement": ("Tank maintenance", create_measurement_payloads),
    "count": ("Counter data", create_count_payloads),
    "kpi": ("Performance KPI", create_kpi_payloads),
    "edge": ("Edge sensor reading", create_edge_payloads)
}

# =============================================================================
# MAIN PUBLISHING LOOP
# =============================================================================

def publish_tank_data():
    """Main function to publish tank data using all schema types"""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)
    if MQTT_USE_TLS:
        client.tls_set()
    try:
        client.connect(BROKER_ADDRESS, BROKER_PORT, MQTT_KEEPALIVE)
        client.loop_start()
        time.sleep(2)
        cycle = 0
        while True:
            cycle += 1
            print(f"\n🔄 Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
            for tank in TANKS:
                print(f"\n🛢️ Publishing for {tank['name']} (ID: {tank['id']})")
                base_topic = f"{MQTT_TOPIC_ENTERPRISE}/{MQTT_TOPIC_SITE}/{MQTT_TOPIC_AREA}/{MQTT_TOPIC_LINE}/{MQTT_TOPIC_CELL}/{tank['name'].lower()}"
                for schema_type, (description, payload_func) in SCHEMA_PAYLOADS.items():
                    print(f"📤 Publishing {schema_type.upper()} payload...")
                    try:
                        if schema_type == "value":
                            for value_type, (value_description, value_payload_func) in VALUE_PAYLOADS.items():
                                print(f"  📊 {value_description}...")
                                value_payloads = value_payload_func(tank)
                                for topic_suffix, value_payload, value_desc in value_payloads:
                                    topic = f"{base_topic}/{value_type}/{topic_suffix}"
                                    if publish_payload(client, topic, value_payload):
                                        print(f"    ✅ {value_desc:20} → {topic}")
                                    else:
                                        print(f"    ❌ {value_desc:20} → Validation failed")
                        else:
                            payload = payload_func(tank)
                            topic = f"{base_topic}/{schema_type}"
                            if publish_payload(client, topic, payload):
                                print(f"  ✅ {description:20} → {topic}")
                            else:
                                print(f"  ❌ {description:20} → Validation failed")
                    except Exception as e:
                        logger.error(f"Error publishing {schema_type}: {e}")
                        print(f"  ❌ {description:20} → Error: {e}")
            print(f"⏳ Waiting {PUBLISH_INTERVAL} seconds until next cycle...")
            time.sleep(PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping tank MQTT publisher...")
    except Exception as e:
        logger.error(f"Connection error: {e}")
        print(f"❌ Connection failed: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("👋 Disconnected from MQTT broker")

def publish_payload(client, topic, payload):
    """Publish a payload to MQTT with schema validation"""
    schema_name = None
    if '/edge/' in topic:
        schema_name = 'reading'
    elif '/reading/' in topic:
        schema_name = 'reading'
    elif '/measurement/' in topic:
        schema_name = 'measurement'
    elif '/count/' in topic:
        schema_name = 'count'
    elif '/kpi/' in topic:
        schema_name = 'kpi'
    elif '/asset' in topic:
        schema_name = 'asset'
    elif '/alert' in topic:
        schema_name = 'alert'
    elif '/state' in topic:
        schema_name = 'state'
    elif '/product' in topic and '/production' not in topic:
        schema_name = 'product'
    elif '/production' in topic:
        schema_name = 'production'
    elif '/value' in topic:
        schema_name = 'value'
    if not schema_name:
        if 'assetId' in payload:
            schema_name = 'asset'
        elif 'alertId' in payload:
            schema_name = 'alert'
        elif 'stateId' in payload:
            schema_name = 'state'
        elif 'measurementId' in payload:
            schema_name = 'measurement'
        elif 'countId' in payload:
            schema_name = 'count'
        elif 'kpiId' in payload:
            schema_name = 'kpi'
        elif 'productId' in payload:
            schema_name = 'product'
        elif 'productionId' in payload:
            schema_name = 'production'
        elif 'valueId' in payload:
            schema_name = 'value'
        elif 'type' in payload and 'value' in payload and 'unit' in payload:
            schema_name = 'reading'
    if schema_name and not validate_payload(payload, schema_name, SCHEMAS):
        logger.error(f"Payload validation failed, not publishing to {topic}")
        return False
    elif not schema_name:
        print(f"⚠️  Could not determine schema type for topic: {topic}")
        logger.warning(f"Could not determine schema type for topic: {topic}")
    payload_json = json.dumps(payload, indent=2)
    result = client.publish(topic, payload_json, qos=MQTT_QOS)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        logger.info(f"Published to {topic}")
        logger.debug(f"Payload: {payload_json}")
        return True
    else:
        logger.error(f"Failed to publish to {topic}: {result.rc}")
        return False

# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("🚀 Starting UNS Tank MQTT Payload Publisher")
    print("=" * 50)
    print(f"📋 Loaded {len(SCHEMAS)} schemas for validation")
    for schema_name in SCHEMAS.keys():
        print(f"   ✅ {schema_name}")
    print(f"\n⚙️  Configuration:")
    print(f"   📡 Broker: {BROKER_ADDRESS}:{BROKER_PORT}")
    print(f"   🛢️ Tanks:")
    for tank in TANKS:
        print(f"      - {tank['name']} (ID: {tank['id']})")
    print(f"   ⏱️  Interval: {PUBLISH_INTERVAL} seconds")
    print(f"   🔄 Random variation: {'Enabled' if ENABLE_RANDOM_VARIATION else 'Disabled'}")
    print(f"   🔐 Authentication: {'Enabled' if MQTT_USE_AUTH else 'Disabled'}")
    print(f"   🔒 TLS: {'Enabled' if MQTT_USE_TLS else 'Disabled'}")
    print(f"   📝 Log Level: {LOG_LEVEL}")
    print("\n🔗 Connecting to MQTT broker...")
    publish_tank_data()
