#!/usr/bin/env python3
"""
Pump MQTT Publisher - Abelara MES Schema Examples

This script publishes realistic pump MQTT payloads to demonstrate all schema types.
Configure your broker details in the .env file and run.

Usage:
    python pump_mqtt_publisher.py

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
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "uns-payload-example")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))
MQTT_QOS = int(os.getenv("MQTT_QOS", "1"))

# MQTT Topic Configuration
MQTT_TOPIC_ENTERPRISE = os.getenv("MQTT_TOPIC_ENTERPRISE", "abelara")
MQTT_TOPIC_SITE = os.getenv("MQTT_TOPIC_SITE", "plant1")
MQTT_TOPIC_AREA = os.getenv("MQTT_TOPIC_AREA", "utilities")
MQTT_TOPIC_LINE = os.getenv("MQTT_TOPIC_LINE", "water-system")
MQTT_TOPIC_CELL = os.getenv("MQTT_TOPIC_CELL", "pump-station")

# Asset Configuration
"""
Asset Configuration for multiple pumps
"""
PUMPS = [
    {
        "id": 101,
        "name": "Pump-101",
        "description": "Centrifugal water pump for cooling system",
        "parent_id": 22,
        "parent_name": "Pump Station 1"
    },
    {
        "id": 102,
        "name": "Pump-102",
        "description": "Centrifugal water pump for cooling system",
        "parent_id": 22,
        "parent_name": "Pump Station 1"
    },
    {
        "id": 103,
        "name": "Pump-103",
        "description": "Centrifugal water pump for cooling system",
        "parent_id": 22,
        "parent_name": "Pump Station 1"
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
# PUMP DATA GENERATION
# =============================================================================

def get_timestamp():
    """Get current ISO 8601 timestamp"""
    return datetime.now(timezone.utc).isoformat()

def add_variation(base_value, variation_percent=3):
    """Add realistic variation to values - reduced from 5% to 3% for more stable readings"""
    if not ENABLE_RANDOM_VARIATION:
        return base_value
    variation = base_value * (variation_percent / 100)
    return base_value + random.uniform(-variation, variation)

# =============================================================================
# SCHEMA PAYLOADS
# =============================================================================

def create_asset_payload(pump):
    """Create Asset schema payload for a given pump"""
    return {
        "timestamp": get_timestamp(),
        "id": pump["id"],
        "name": pump["name"],
        "description": pump["description"],
        "assetType": {
            "id": 1,
            "name": "Centrifugal Pump",
            "description": "Centrifugal pump equipment"
        },
        "parentAsset": {
            "id": pump["parent_id"],
            "name": pump["parent_name"],
            "description": "Primary water pump station"
        },
        "metadata": {
            "source": "asset-management",
            "uri": f"asset://{pump['id']}",
            "additionalInfo": {
                "manufacturer": "Grundfos",
                "model": "CR45-4",
                "serialNumber": f"GF-2023-00{pump['id']}",
                "installationDate": "2023-03-15",
                "powerRating": "5.5 kW",
                "maxFlow": "45 m³/h",
                "maxPressure": "10 bar",
                "impellerDiameter": "165 mm"
            }
        }
    }

def create_state_payload(pump):
    """Create State schema payload for a given pump"""
    states = [
        {"id": 1, "name": "Running", "description": "Equipment is operating normally", "color": "#00FF00"},
        {"id": 2, "name": "Starting", "description": "Equipment startup sequence", "color": "#FFFF00"},
        {"id": 3, "name": "Stopping", "description": "Equipment shutdown sequence", "color": "#FFA500"},
        {"id": 4, "name": "Fault", "description": "Equipment fault condition", "color": "#FF0000"},
        {"id": 5, "name": "Maintenance", "description": "Equipment under maintenance", "color": "#800080"}
    ]
    current_state = random.choice(states)
    previous_state = random.choice([s for s in states if s["id"] != current_state["id"]])
    return {
        "timestamp": get_timestamp(),
        "description": f"Pump is {current_state['name'].lower()}",
        "color": current_state["color"],
        "type": {
            "id": current_state["id"],
            "name": current_state["name"],
            "description": current_state["description"]
        },
        "metadata": {
            "source": "plc-controller",
            "uri": "opc://plc1/DB1.DBW0",
            "asset": {
                "id": pump["id"],
                "name": pump["name"],
                "description": pump["description"]
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
                "runTime": random.randint(1000, 5000),
                "startupTime": datetime.now(timezone.utc).isoformat(),
                "mode": random.choice(["AUTO", "MANUAL"]),
                "operator": random.choice(["John Smith", "Jane Doe", "Bob Wilson"])
            }
        }
    }

def create_measurement_payloads(pump):
    """Create multiple Measurement schema payloads for precision maintenance and operator rounds"""
    measurement_types = [
        {"id": 1, "name": "Bearing Temperature", "description": "Precision bearing temperature measurement", "unit": "°C", "base_value": 72.5, "target": 70.0, "topic_suffix": "bearing-temperature", "location": "Drive End Bearing"},
        {"id": 2, "name": "Vibration Analysis", "description": "Precision vibration measurement", "unit": "mm/s", "base_value": 1.8, "target": 1.2, "topic_suffix": "vibration-analysis", "location": "Drive End"},
        {"id": 3, "name": "Oil Analysis", "description": "Oil quality measurement", "unit": "mg/kg", "base_value": 12.5, "target": 8.0, "topic_suffix": "oil-analysis", "location": "Oil Reservoir"},
        {"id": 4, "name": "Alignment Check", "description": "Shaft alignment measurement", "unit": "mm", "base_value": 0.08, "target": 0.03, "topic_suffix": "alignment-check", "location": "Coupling"},
        {"id": 5, "name": "Insulation Resistance", "description": "Motor insulation resistance", "unit": "MΩ", "base_value": 850, "target": 1000, "topic_suffix": "insulation-resistance", "location": "Motor"}
    ]
    
    payloads = []
    for measurement in measurement_types:
        value = add_variation(measurement["base_value"])
        tolerance = measurement["target"] * 0.15  # 15% tolerance for precision measurements
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
                "source": "precision-maintenance",
                "uri": f"maintenance://{pump['name'].lower()}/{measurement['name'].lower().replace(' ', '-')}",
                "asset": {
                    "id": pump["id"],
                    "name": pump["name"],
                    "description": pump["description"]
                },
                "additionalInfo": {
                    "technician": random.choice(["John Smith", "Jane Doe", "Bob Wilson", "Mike Johnson", "Sarah Davis"]),
                    "measurementMethod": random.choice(["Infrared Thermography", "Vibration Analysis", "Oil Sampling", "Laser Alignment", "Megger Test"]),
                    "equipmentUsed": random.choice(["Fluke Ti480", "SKF Microlog", "Spectro Scientific", "Easy-Laser", "Fluke 1507"]),
                    "measurementDate": datetime.now(timezone.utc).isoformat(),
                    "nextMeasurementDue": "2024-06-15",
                    "trend": random.choice(["Improving", "Stable", "Deteriorating"]),
                    "measurementLocation": measurement["location"]
                }
            },
            "product": {
                "id": 1,
                "name": "Cooling Water",
                "description": "Process cooling water",
                "family": {
                    "id": 1,
                    "name": "Utilities",
                    "description": "Utility products and services"
                }
            },
            "productionContext": {
                "batchId": f"MAINT-2024-{random.randint(1, 999):03d}",
                "processStep": "Precision Maintenance",
                "demand": random.choice(["Scheduled", "Condition Based", "Emergency"])
            }
        }
        
        payloads.append((measurement["topic_suffix"], payload, f"{measurement['name']} measurement"))
    
    return payloads

def create_edge_payloads(pump):
    """Create multiple Edge schema payloads for different process readings"""
    edge_types = [
        {"id": 1, "name": "Temperature", "description": "Temperature readings from process equipment", "unit": "°C", "base_value": 72.5, "topic_suffix": "temperature", "location": "Drive End Bearing"},
        {"id": 2, "name": "Pressure", "description": "Pressure readings from process equipment", "unit": "bar", "base_value": 7.2, "topic_suffix": "pressure", "location": "Discharge"},
        {"id": 3, "name": "Flow", "description": "Flow rate readings from process equipment", "unit": "m³/h", "base_value": 42.8, "topic_suffix": "flow", "location": "Discharge"},
        {"id": 4, "name": "Vibration", "description": "Vibration readings from process equipment", "unit": "mm/s", "base_value": 1.8, "topic_suffix": "vibration", "location": "Drive End"},
        {"id": 5, "name": "Current", "description": "Electrical current readings from process equipment", "unit": "A", "base_value": 9.2, "topic_suffix": "current", "location": "Motor"},
        {"id": 6, "name": "Voltage", "description": "Electrical voltage readings from process equipment", "unit": "V", "base_value": 418, "topic_suffix": "voltage", "location": "Motor"},
        {"id": 7, "name": "Power", "description": "Power consumption readings from process equipment", "unit": "kW", "base_value": 4.8, "topic_suffix": "power", "location": "Motor"}
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
            "value": round(value, 1),
            "unit": edge_type["unit"],
            "metadata": {
                "source": f"{edge_type['name'].lower()}-sensor",
                "uri": f"opc://plc1/DB1.DBD{random.randint(12, 30)}",
                "asset": {
                    "id": pump["id"],
                    "name": pump["name"],
                    "description": pump["description"]
                },
                "additionalInfo": {
                    "sensorId": f"{edge_type['name'].upper().replace(' ', '')}-{pump['id']:03d}",
                    "location": edge_type["location"],
                    "alarmThreshold": edge_type["base_value"] * 1.2,
                    "warningThreshold": edge_type["base_value"] * 1.1,
                    "calibrationDate": "2024-01-15",
                    "nextCalibration": "2024-07-15"
                }
            }
        }
        
        payloads.append((edge_type["topic_suffix"], payload, f"{edge_type['name']} reading"))
    
    return payloads

def create_count_payloads(pump):
    """Create multiple Count schema payloads for different accumulated values"""
    count_types = [
        {"id": 1, "name": "Gallons Delivered", "description": "Total gallons delivered to cooling system", "unit": "gallons", "base_value": 125000, "topic_suffix": "gallons-delivered", "increment": lambda: random.randint(80, 120)},
        {"id": 2, "name": "Water Delivered", "description": "Total water delivered to cooling system", "unit": "m³", "base_value": 473, "topic_suffix": "water-delivered", "increment": lambda: random.uniform(0.3, 0.45)},
        {"id": 3, "name": "Runtime Hours", "description": "Total pump runtime hours", "unit": "hours", "base_value": 1250, "topic_suffix": "runtime-hours", "increment": lambda: random.uniform(0.1, 0.2)},
        {"id": 4, "name": "Starts", "description": "Total pump starts", "unit": "count", "base_value": 150, "topic_suffix": "starts", "increment": lambda: random.randint(0, 1)},
        {"id": 5, "name": "Energy Consumed", "description": "Total energy consumed", "unit": "kWh", "base_value": 12500, "topic_suffix": "energy-consumed", "increment": lambda: random.uniform(4.5, 5.5)}
    ]
    
    payloads = []
    for count_type in count_types:
        increment = count_type["increment"]()
        value = count_type["base_value"] + increment
        
        payload = {
            "timestamp": get_timestamp(),
            "value": round(value, 1) if count_type["unit"] in ["m³", "hours", "kWh"] else int(value),
            "unit": count_type["unit"],
            "type": {
                "id": count_type["id"],
                "name": count_type["name"],
                "description": count_type["description"]
            },
            "metadata": {
                "source": "flow-counter",
                "uri": "opc://plc1/DB1.DBD16",
                "asset": {
                    "id": pump["id"],
                    "name": pump["name"],
                    "description": pump["description"]
                },
                "production": {
                    "id": random.randint(1000, 9999),
                    "name": f"Cooling System Operation {random.randint(1, 100)}",
                    "description": "Continuous cooling system operation"
                },
                "product": {
                    "id": 1,
                    "name": "Cooling Water",
                    "description": "Process cooling water"
                },
                "additionalInfo": {
                    "maintenanceDue": 2500,
                    "lastMaintenance": "2024-01-15",
                    "nextMaintenance": "2024-06-15",
                    "flowRate": round(add_variation(42.8), 1),
                    "efficiency": round(add_variation(96.5), 1),
                    "totalEnergy": round(add_variation(12500), 1),
                    "increment": round(increment, 2) if count_type["unit"] in ["m³", "hours", "kWh"] else int(increment),
                    "lastReset": "2024-01-01T00:00:00Z",
                    "nextReset": "2025-01-01T00:00:00Z"
                }
            }
        }
        
        payloads.append((count_type["topic_suffix"], payload, f"{count_type['name']} count"))
    
    return payloads

def create_kpi_payloads(pump):
    """Create multiple KPI schema payloads for different performance metrics"""
    kpi_types = [
        {"id": 1, "name": "Pump Efficiency", "description": "Overall pump efficiency", "unit": "%", "base_value": 96.5, "topic_suffix": "efficiency"},
        {"id": 2, "name": "Energy Efficiency", "description": "Energy efficiency ratio", "unit": "kWh/m³", "base_value": 0.115, "topic_suffix": "energy-efficiency"},
        {"id": 3, "name": "MTBF", "description": "Mean Time Between Failures", "unit": "hours", "base_value": 8760, "topic_suffix": "mtbf"}
    ]
    
    # OEE components
    oee_components = [
        {"id": 4, "name": "Availability", "description": "Equipment availability percentage", "unit": "%", "base_value": 98.2, "topic_suffix": "availability"},
        {"id": 5, "name": "Performance", "description": "Equipment performance percentage", "unit": "%", "base_value": 95.5, "topic_suffix": "performance"},
        {"id": 6, "name": "Quality", "description": "Equipment quality percentage", "unit": "%", "base_value": 99.8, "topic_suffix": "quality"},
        {"id": 7, "name": "OEE", "description": "Overall Equipment Effectiveness", "unit": "%", "base_value": 94.5, "topic_suffix": "oee"}
    ]
    
    payloads = []
    
    # Add regular KPIs
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
                "id": 1,
                "name": "Cooling Water",
                "description": "Process cooling water",
                "family": {
                    "id": 1,
                    "name": "Utilities",
                    "description": "Utility products and services"
                }
            },
            "metadata": {
                "source": "kpi-calculator",
                "uri": f"kpi://{pump['name'].lower()}/{kpi_type['name'].lower().replace(' ', '-')}",
                "asset": {
                    "id": pump["id"],
                    "name": pump["name"]
                },
                "additionalInfo": {
                    "calculationPeriod": "1 hour",
                    "inputPower": round(add_variation(4.8), 1),
                    "outputPower": round(add_variation(4.63), 1),
                    "targetEfficiency": 95.0,
                    "trend": random.choice(["Improving", "Stable", "Declining"]),
                    "lastCalculation": datetime.now(timezone.utc).isoformat(),
                    "baselineValue": kpi_type["base_value"],
                    "improvement": round((value - kpi_type["base_value"]) / kpi_type["base_value"] * 100, 2)
                }
            }
        }
        
        payloads.append((kpi_type["topic_suffix"], payload, f"{kpi_type['name']} KPI"))
    
    # Add OEE components under oee topic path
    for oee_component in oee_components:
        value = add_variation(oee_component["base_value"])
        
        payload = {
            "timestamp": get_timestamp(),
            "value": round(value, 1),
            "unit": oee_component["unit"],
            "type": {
                "id": oee_component["id"],
                "name": oee_component["name"],
                "description": oee_component["description"]
            },
            "product": {
                "id": 1,
                "name": "Cooling Water",
                "description": "Process cooling water",
                "family": {
                    "id": 1,
                    "name": "Utilities",
                    "description": "Utility products and services"
                }
            },
            "metadata": {
                "source": "oee-calculator",
                "uri": f"oee://{pump['name'].lower()}/{oee_component['name'].lower().replace(' ', '-')}",
                "asset": {
                    "id": pump["id"],
                    "name": pump["name"]
                },
                "additionalInfo": {
                    "calculationPeriod": "1 hour",
                    "plannedProductionTime": 480,
                    "actualProductionTime": round(add_variation(470), 1),
                    "idealCycleTime": 3600,
                    "actualCycleTime": round(add_variation(3780), 1),
                    "goodUnits": round(add_variation(125), 1),
                    "totalUnits": round(add_variation(126), 1),
                    "trend": random.choice(["Improving", "Stable", "Declining"]),
                    "lastCalculation": datetime.now(timezone.utc).isoformat(),
                    "targetOEE": 95.0,
                    "worldClassOEE": 85.0
                }
            }
        }
        
        payloads.append((f"oee/{oee_component['topic_suffix']}", payload, f"{oee_component['name']} OEE"))
    
    return payloads

def create_alert_payload(pump):
    """Create Alert schema payload"""
    alert_types = [
        {"severity": 2, "code": "TEMP_WARN", "message": "Pump bearing temperature approaching warning threshold"},
        {"severity": 3, "code": "TEMP_HIGH", "message": "Pump bearing temperature exceeds warning threshold"},
        {"severity": 1, "code": "MAINT_DUE", "message": "Pump maintenance due within 100 hours"},
        {"severity": 2, "code": "FLOW_LOW", "message": "Pump flow rate below target range"},
        {"severity": 2, "code": "VIBRATION_HIGH", "message": "Pump vibration levels above normal range"},
        {"severity": 3, "code": "PRESSURE_HIGH", "message": "Pump discharge pressure exceeds safety limit"}
    ]
    
    alert = random.choice(alert_types)
    is_acknowledged = random.choice([True, False])
    
    # Build acknowledgment object
    acknowledgment = {
        "acknowledged": is_acknowledged,
        "acknowledgedBy": random.choice(["John Smith", "Jane Doe", "Bob Wilson", "Mike Johnson"]) if is_acknowledged else None,
        "acknowledgedAt": get_timestamp() if is_acknowledged else None
    }
    
    return {
        "timestamp": get_timestamp(),
        "severity": alert["severity"],
        "code": alert["code"],
        "message": alert["message"],
        "metadata": {
            "source": "monitoring-system",
            "uri": "opc://plc1/DB1.DBD4",
            "asset": {
                "id": pump["id"],
                "name": pump["name"],
                "description": pump["description"]
            },
            "acknowledgment": acknowledgment,
            "additionalInfo": {
                "temperature": round(add_variation(76.5), 1),
                "warningThreshold": 75.0,
                "alarmThreshold": 85.0,
                "sensorLocation": "Drive End Bearing",
                "trend": random.choice(["Rising", "Stable", "Falling"]),
                "timeInAlarm": random.randint(5, 30),
                "recommendedAction": random.choice(["Monitor", "Check bearings", "Schedule maintenance", "Reduce load", "Check alignment"]),
                "priority": random.choice(["Low", "Medium", "High", "Critical"])
            }
        }
    }

def create_product_payload(pump):
    """Create Product schema payload"""
    return {
        "timestamp": get_timestamp(),
        "id": 1,
        "name": "Cooling Water",
        "description": "Process cooling water for heat exchange systems",
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
            "uri": "product://cooling-water",
            "asset": {
                "id": pump["id"],
                "name": pump["name"],
                "description": pump["description"]
            },
            "additionalInfo": {
                "specifications": {
                    "temperature": "15-25°C",
                    "pressure": "3-8 bar",
                    "quality": "Process Grade",
                    "chlorinated": True
                },
                "regulatoryCompliance": ["ISO 14001", "Water Quality Standards"]
            }
        }
    }

def create_production_payload(pump):
    """Create Production schema payload"""
    water_delivered = random.randint(320, 380)  # More realistic range
    runtime_hours = random.uniform(6.5, 7.5)    # More realistic runtime
    
    return {
        "timestamp": get_timestamp(),
        "start_ts": datetime.now(timezone.utc).isoformat(),
        "end_ts": None,
        "counts": [
            {
                "type": {
                    "id": 1,
                    "name": "Water Delivered",
                    "description": "Total water delivered to cooling system",
                    "unit": "m³"
                },
                "quantity": water_delivered,
                "timestamp": get_timestamp()
            },
            {
                "type": {
                    "id": 2,
                    "name": "Runtime Hours",
                    "description": "Total pump runtime hours",
                    "unit": "hours"
                },
                "quantity": round(runtime_hours, 1),
                "timestamp": get_timestamp()
            }
        ],
        "metadata": {
            "source": "production-tracker",
            "uri": f"production://cooling-system-2024-{random.randint(1, 999):03d}",
            "asset": {
                "id": pump["id"],
                "name": pump["name"],
                "description": pump["description"]
            },
            "product": {
                "id": 1,
                "name": "Cooling Water",
                "description": "Process cooling water for heat exchange systems",
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
                "operator": random.choice(["John Smith", "Jane Doe", "Bob Wilson", "Mike Johnson", "Sarah Davis"]),
                "demandLevel": random.choice(["Low", "Medium", "High"]),
                "systemEfficiency": round(add_variation(96.5), 1),
                "energyConsumption": round(add_variation(32.8), 1),
                "qualityScore": round(add_variation(98.5), 1),
                "plannedProduction": 350,
                "actualProduction": water_delivered,
                "efficiency": round((water_delivered / 350) * 100, 1)
            }
        }
    }

# =============================================================================
# PAYLOAD DEFINITIONS
# =============================================================================

# Define all schema payloads (functions to call when needed)
SCHEMA_PAYLOADS = {
    "asset": ("Asset configuration", create_asset_payload),
    "state": ("Pump state", create_state_payload),
    "alert": ("System alert", create_alert_payload),
    "product": ("Product information", create_product_payload),
    "production": ("Production data", create_production_payload),
    "value": ("Value data", None)  # Handled separately with multiple payloads
}

# Define value payloads (functions to call when needed)
VALUE_PAYLOADS = {
    "measurement": ("Precision maintenance", create_measurement_payloads),
    "count": ("Counter data", create_count_payloads),
    "kpi": ("Performance KPI", create_kpi_payloads),
    "edge": ("Edge sensor reading", create_edge_payloads)
}

# =============================================================================
# MAIN PUBLISHING LOOP
# =============================================================================

def publish_pump_data():
    """Main function to publish pump data using all schema types"""
    # Create MQTT client
    client = mqtt.Client()
    
    # Set up callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    
    # Set up authentication if provided
    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)
    
    # Set up TLS if enabled
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
            for pump in PUMPS:
                print(f"\n🚰 Publishing for {pump['name']} (ID: {pump['id']})")
                # Build base topic dynamically using UNS structure language
                base_topic = f"{MQTT_TOPIC_ENTERPRISE}/{MQTT_TOPIC_SITE}/{MQTT_TOPIC_AREA}/{MQTT_TOPIC_LINE}/{MQTT_TOPIC_CELL}/{pump['name'].lower()}"
                for schema_type, (description, payload_func) in SCHEMA_PAYLOADS.items():
                    print(f"📤 Publishing {schema_type.upper()} payload...")
                    try:
                        if schema_type == "value":
                            for value_type, (value_description, value_payload_func) in VALUE_PAYLOADS.items():
                                print(f"  📊 {value_description}...")
                                value_payloads = value_payload_func(pump)
                                for topic_suffix, value_payload, value_desc in value_payloads:
                                    topic = f"{base_topic}/{value_type}/{topic_suffix}"
                                    if publish_payload(client, topic, value_payload):
                                        print(f"    ✅ {value_desc:20} → {topic}")
                                    else:
                                        print(f"    ❌ {value_desc:20} → Validation failed")
                        else:
                            payload = payload_func(pump)
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
        print(f"\n🛑 Stopping pump MQTT publisher...")
    except Exception as e:
        logger.error(f"Connection error: {e}")
        print(f"❌ Connection failed: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("👋 Disconnected from MQTT broker")

def publish_payload(client, topic, payload):
    """Publish a payload to MQTT with schema validation"""
    # Determine schema type from topic path first, then payload structure
    schema_name = None
    
    # Topic-based detection (more reliable)
    if '/edge/' in topic:
        schema_name = 'reading'  # Edge payloads use reading schema
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
    
    # Fallback to payload structure detection if topic-based fails
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
            # Reading schema has type, value, unit structure
            schema_name = 'reading'
    
    # Validate payload against schema
    if schema_name and not validate_payload(payload, schema_name, SCHEMAS):
        logger.error(f"Payload validation failed, not publishing to {topic}")
        return False
    elif not schema_name:
        print(f"⚠️  Could not determine schema type for topic: {topic}")
        logger.warning(f"Could not determine schema type for topic: {topic}")
    
    # Convert payload to JSON
    payload_json = json.dumps(payload, indent=2)
    
    # Publish to MQTT
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
    print("🚀 Starting UNS MQTT Payload Publisher")
    print("=" * 50)
    
    # Show schema loading status
    print(f"📋 Loaded {len(SCHEMAS)} schemas for validation")
    for schema_name in SCHEMAS.keys():
        print(f"   ✅ {schema_name}")
    
    # Show configuration
    print(f"\n⚙️  Configuration:")
    print(f"   📡 Broker: {BROKER_ADDRESS}:{BROKER_PORT}")
    print(f"   🏭 Pumps:")
    for pump in PUMPS:
        print(f"      - {pump['name']} (ID: {pump['id']})")
    print(f"   ⏱️  Interval: {PUBLISH_INTERVAL} seconds")
    print(f"   🔄 Random variation: {'Enabled' if ENABLE_RANDOM_VARIATION else 'Disabled'}")
    print(f"   🔐 Authentication: {'Enabled' if MQTT_USE_AUTH else 'Disabled'}")
    print(f"   🔒 TLS: {'Enabled' if MQTT_USE_TLS else 'Disabled'}")
    print(f"   📝 Log Level: {LOG_LEVEL}")
    print("\n🔗 Connecting to MQTT broker...")
    publish_pump_data()