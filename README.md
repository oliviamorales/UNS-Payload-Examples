# UNS Payload Examples
## Industrial MQTT Schema Definitions & Examples

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JSON Schema](https://img.shields.io/badge/JSON%20Schema-2020--12-blue.svg)](https://json-schema.org/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Sample UNS payload examples - educational reference, not a standard or comprehensive specification**

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/UNS-Payload-Examples.git
cd UNS-Payload-Examples

# Set up the Python example
cd examples
pip install -r requirements.txt
cp example.env .env
# Edit .env with your MQTT broker settings

# Run the example
python pump_mqtt_publisher.py
```

## 📋 Table of Contents
- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [📊 Schema Types](#-schema-types)
- [🏗️ Architecture](#️-architecture)
- [📖 Payload Examples](#-payload-examples)
  - [Asset Definition](#asset-definition-payload)
  - [State Management](#state-payload)
  - [Edge Data](#edge-payload)
  - [Measurements](#measurement-payload)
  - [Counters](#count-payload)
  - [KPIs](#kpi-payload)
  - [Alerts](#alert-payload)
  - [Production](#production-payload)
- [🛠️ Implementation](#️-implementation)
- [📚 Documentation](#-documentation)
- [⚖️ License](#️-license)

## 🎯 Overview

**UNS Payload Examples** provides sample schemas and examples for industrial MQTT payloads following Unified Namespace (UNS) principles. This is an educational project demonstrating one possible approach to UNS implementation - not a definitive standard or comprehensive specification.

### The Problem

Industrial data is often trapped in silos, lacking context and standardization:
- Raw sensor values without meaning (`72.5` - but what is it?)
- Custom integrations for every system connection
- No standard format for industrial data exchange
- Difficult to implement analytics and AI initiatives

### The Solution

A **Unified Namespace (UNS)** approach with sample schema-validated MQTT payloads:
- **Self-describing data** with context and metadata
- **Example integration patterns** using structured schemas
- **Sample validation** demonstrating data quality concepts
- **Educational examples** for learning UNS principles

## ✨ Features

- **🔧 Sample Schema Suite**: 10 example industrial payload types with JSON Schema validation
- **📡 MQTT Example**: Working MQTT publisher demonstrating concepts
- **🎯 Schema Validation**: Example payload validation implementation
- **📊 Sample Data**: Example industrial data for learning purposes
- **🔒 Security Examples**: TLS and authentication implementation samples
- **📈 Monitoring Examples**: Logging and status reporting patterns
- **⚙️ Configurable Examples**: Environment-based configuration patterns

## 📊 Schema Types

| Schema | Purpose | Example Topic |
|--------|---------|---------------|
| **Asset** | Equipment configuration | `.../pump-101/asset` |
| **State** | Operational states | `.../pump-101/state` |
| **Alert** | System notifications | `.../pump-101/alert` |
| **Measurement** | Precision measurements | `.../pump-101/measurement/vibration` |
| **Count** | Accumulated values | `.../pump-101/count/runtime-hours` |
| **KPI** | Performance indicators | `.../pump-101/kpi/oee` |
| **Product** | Product specifications | `.../pump-101/product` |
| **Production** | Production tracking | `.../pump-101/production` |
| **Reading** | Real-time sensor data | `.../pump-101/edge/temperature` |
| **Value** | Generic measurements | `.../pump-101/value/pressure` |

## 🏗️ Architecture

The UNS follows a hierarchical topic structure that mirrors your physical plant:

```
{enterprise}/{site}/{area}/{line}/{cell}/{equipment}/{messageType}
```

**Example**: `abelara/plant1/utilities/water-system/pump-station/pump-101/state`

### Example Principles Demonstrated

1. **Edge Modeling**: Sample data contextualized at the source
2. **Schema Validation**: Example payload validation against JSON Schema
3. **Metadata Rich**: Sample context included with messages
4. **Decoupled Architecture**: Example publisher/subscriber patterns
5. **Schema Based**: JSON Schema Draft 2020-12 examples

## 📖 Payload Examples

All examples below show sample payloads demonstrating possible UNS structures. These are educational examples, not definitive standards.

### Asset Definition Payload

**Purpose**: To describe the static, physical, and hierarchical properties of a piece of equipment. This is the foundational "birth certificate" for any asset. It is published infrequently, typically only when the asset is created or its core configuration is updated.

**Topic**: `.../pump-101/definition`

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "id": 101,
  "name": "Pump-101",
  "description": "Centrifugal water pump for cooling system",
  "assetType": {
    "id": 1,
    "name": "Centrifugal Pump",
    "description": "Centrifugal pump equipment"
  },
  "parentAsset": {
    "id": 22,
    "name": "Pump Station 1",
    "description": "Primary water pump station"
  },
  "metadata": {
    "source": "asset-management",
    "uri": "asset://101",
    "additionalInfo": {
      "manufacturer": "Grundfos",
      "model": "CR45-4",
      "serialNumber": "GF-2023-001234",
      "installationDate": "2023-03-15",
      "powerRating": "5.5 kW",
      "maxFlow": "45 m³/h",
      "maxPressure": "10 bar",
      "impellerDiameter": "165 mm"
    }
  }
}
```

### State Payload

**Purpose**: To communicate the operational state of an asset at a specific point in time. This is the single most important payload for tracking uptime, downtime, and OEE Availability. It is published immediately whenever the asset's state changes.

**Topic**: `.../pump-101/state`

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "description": "Pump is running normally",
  "color": "#00FF00",
  "type": {
    "id": 1,
    "name": "Running",
    "description": "Equipment is operating normally"
  },
  "metadata": {
    "source": "plc-controller",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 101,
      "name": "Pump-101",
      "description": "Centrifugal water pump for cooling system"
    },
    "previousState": {
      "id": 2,
      "name": "Starting",
      "description": "Equipment startup sequence",
      "color": "#FFFF00",
      "type": {
        "id": 2,
        "name": "Starting",
        "description": "Equipment startup sequence"
      }
    },
    "additionalInfo": {
      "runTime": 1250,
      "startupTime": "2024-03-20T06:00:00.000Z",
      "mode": "AUTO",
      "operator": "John Smith"
    }
  }
}
```

### Edge Payload

**Purpose**: To transmit raw, high-frequency process values directly from sensors at the "edge" of the network. This represents the core real-time telemetry from the asset.

**Note**: "Edge" refers to the namespace concept in topic paths (e.g., `.../edge/temperature`), not a separate schema type. Edge payloads use the same structure as other payloads but are published to edge-specific topics for real-time sensor data.

**Topic**: `.../pump-101/edge/{type}` (e.g., `.../edge/temperature`)

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "type": {
    "id": 1,
    "name": "Temperature",
    "description": "Temperature readings from process equipment"
  },
  "value": 72.5,
  "unit": "°C",
  "metadata": {
    "source": "temperature-sensor",
    "uri": "opc://plc1/DB1.DBD12",
    "asset": {
      "id": 101,
      "name": "Pump-101",
      "description": "Centrifugal water pump for cooling system"
    },
    "additionalInfo": {
      "sensorId": "TEMPERATURE-101",
      "location": "Drive End Bearing",
      "alarmThreshold": 87.0,
      "warningThreshold": 79.8,
      "calibrationDate": "2024-01-15",
      "nextCalibration": "2024-07-15"
    }
  }
}
```

### Measurement Payload

**Purpose**: To record a precision measurement, often taken manually as part of a quality check or condition-based maintenance task.

**Topic**: `.../pump-101/measurement/{type}` (e.g., `.../measurement/vibration-analysis`)

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "type": {
    "id": 2,
    "name": "Vibration Analysis",
    "description": "Precision vibration measurement"
  },
  "value": 1.8,
  "unit": "mm/s",
  "target": 1.2,
  "tolerance": 0.18,
  "inTolerance": false,
  "metadata": {
    "source": "precision-maintenance",
    "uri": "maintenance://pump-101/vibration-analysis",
    "asset": {
      "id": 101,
      "name": "Pump-101",
      "description": "Centrifugal water pump for cooling system"
    },
    "additionalInfo": {
      "technician": "Jane Doe",
      "measurementMethod": "Vibration Analysis",
      "equipmentUsed": "SKF Microlog",
      "measurementDate": "2024-03-20T14:30:00.123Z",
      "nextMeasurementDue": "2024-06-15",
      "trend": "Deteriorating",
      "measurementLocation": "Drive End"
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
    "batchId": "MAINT-2024-002",
    "processStep": "Precision Maintenance",
    "demand": "Condition Based"
  }
}
```

### Count Payload

**Purpose**: To report the accumulation of a discrete value over time, such as total production, cycles, or runtime hours.

**Topic**: `.../pump-101/count/{type}` (e.g., `.../count/runtime-hours`)

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "value": 1250.2,
  "unit": "hours",
  "type": {
    "id": 3,
    "name": "Runtime Hours",
    "description": "Total pump runtime hours"
  },
  "metadata": {
    "source": "runtime-counter",
    "uri": "opc://plc1/DB1.DBD20",
    "asset": {
      "id": 101,
      "name": "Pump-101",
      "description": "Centrifugal water pump for cooling system"
    },
    "production": {
      "id": 2024,
      "name": "Cooling System Operation 45",
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
      "flowRate": 42.8,
      "efficiency": 96.5,
      "totalEnergy": 12500,
      "increment": 0.15,
      "lastReset": "2024-01-01T00:00:00Z",
      "nextReset": "2025-01-01T00:00:00Z"
    }
  }
}
```

### KPI Payload

**Purpose**: To publish the result of a performance calculation. This is information, not raw data, providing standardized metrics for dashboards and reports.

**Topic**: `.../pump-101/kpi/{type}` (e.g., `.../kpi/oee/oee`)

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "value": 72.0,
  "unit": "%",
  "type": {
    "id": 7,
    "name": "OEE",
    "description": "Overall Equipment Effectiveness"
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
    "uri": "oee://pump-101/oee",
    "asset": {
      "id": 101,
      "name": "Pump-101"
    },
    "additionalInfo": {
      "calculationPeriod": "1 hour",
      "plannedProductionTime": 480,
      "actualProductionTime": 470.0,
      "idealCycleTime": 3.6,
      "goodUnits": 125.0,
      "totalUnits": 126.0,
      "trend": "Decreasing",
      "lastCalculation": "2024-03-20T14:30:00.123Z",
      "targetOEE": 85.0,
      "components": {
        "availability": 95.0,
        "performance": 76.5,
        "quality": 99.2
      }
    }
  }
}
```

### Alert Payload

**Purpose**: To notify systems and personnel of a significant event that requires awareness or action. It drives all alarm and notification systems.

**Topic**: `.../pump-101/alert`

```json
{
  "timestamp": "2024-03-20T14:35:00.123Z",
  "severity": 2,
  "code": "TEMP_WARN",
  "message": "Pump bearing temperature approaching warning threshold",
  "metadata": {
    "source": "monitoring-system",
    "uri": "opc://plc1/DB1.DBD4",
    "asset": {
      "id": 101,
      "name": "Pump-101",
      "description": "Centrifugal water pump for cooling system"
    },
    "acknowledgment": {
      "acknowledged": false,
      "acknowledgedBy": null,
      "acknowledgedAt": null
    },
    "additionalInfo": {
      "temperature": 76.5,
      "warningThreshold": 75.0,
      "alarmThreshold": 85.0,
      "sensorLocation": "Drive End Bearing",
      "trend": "Rising",
      "timeInAlarm": 15,
      "recommendedAction": "Monitor",
      "priority": "Medium"
    }
  }
}
```

### Production Payload

**Purpose**: To define the context of a specific production run, linking the asset, the product being made, and the resulting counts over a period of time. It acts as a "wrapper" or "session" for a work order or batch.

**Topic**: `.../pump-101/production`

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "start_ts": "2024-03-20T07:00:00.000Z",
  "end_ts": null,
  "counts": [
    {
      "type": {
        "id": 1,
        "name": "Water Delivered",
        "description": "Total water delivered to cooling system",
        "unit": "m³"
      },
      "quantity": 350,
      "timestamp": "2024-03-20T14:30:00.123Z"
    },
    {
      "type": {
        "id": 2,
        "name": "Runtime Hours",
        "description": "Total pump runtime hours",
        "unit": "hours"
      },
      "quantity": 7.5,
      "timestamp": "2024-03-20T14:30:00.123Z"
    }
  ],
  "metadata": {
    "source": "production-tracker",
    "uri": "production://cooling-system-2024-001",
    "asset": {
      "id": 101,
      "name": "Pump-101",
      "description": "Centrifugal water pump for cooling system"
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
      "shift": "Day",
      "operator": "John Smith",
      "demandLevel": "High",
      "systemEfficiency": 96.5,
      "energyConsumption": 32.8,
      "qualityScore": 98.5,
      "plannedProduction": 350,
      "actualProduction": 350,
      "efficiency": 100.0
    }
  }
}
```

## 🛠️ Implementation

### Working Example Output

The Python example publishes validated payloads continuously. Here's what you'll see:

```
🚀 Starting UNS MQTT Payload Publisher
==================================================
📋 Loaded 10 schemas for validation
   ✅ asset      ✅ alert       ✅ state       ✅ measurement ✅ count
   ✅ kpi        ✅ product     ✅ production  ✅ reading     ✅ value

⚙️  Configuration:
   📡 Broker: your-broker.hivemq.cloud:8883
   🏭 Pump: Pump-101 (ID: 101)
   ⏱️  Interval: 5 seconds
   🔐 Authentication: Enabled
   🔒 TLS: Enabled

🔄 Cycle 1 - 12:51:47
📤 Publishing ASSET payload...
  ✅ Asset configuration  → .../pump-101/asset
📤 Publishing STATE payload...
  ✅ Pump state           → .../pump-101/state
📤 Publishing ALERT payload...
  ✅ System alert         → .../pump-101/alert
📤 Publishing PRODUCTION payload...
  ✅ Production data      → .../pump-101/production
📤 Publishing VALUE payload...
  📊 Precision maintenance...
    ✅ Bearing Temperature  → .../measurement/bearing-temperature
    ✅ Vibration Analysis   → .../measurement/vibration-analysis
  📊 Counter data...
    ✅ Runtime Hours       → .../count/runtime-hours
    ✅ Energy Consumed     → .../count/energy-consumed
  📊 Performance KPI...
    ✅ Pump Efficiency     → .../kpi/efficiency
    ✅ OEE Availability    → .../kpi/oee/availability
  📊 Edge sensor reading...
    ✅ Temperature reading → .../edge/temperature
    ✅ Pressure reading    → .../edge/pressure
```

### Schema Validation in Action

Every payload is validated before publishing:

```python
# Automatic schema detection and validation
def publish_payload(topic, payload, description):
    schema_type = detect_schema_type(topic, payload)
    if validate_payload(payload, schema_type):
        client.publish(topic, json.dumps(payload))
        print(f"  ✅ {description} → {topic}")
    else:
        print(f"  ❌ {description} → Validation failed")
```

**Validation Failures Show Details:**
```
❌ Schema validation failed for production:
   Error: None is not of type 'string'
   Path: end_ts
   Expected: string
```

### Integration Examples

**Subscribe to All Pump Data:**
```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    print(f"Received {topic}: {payload}")

client = mqtt.Client()
client.on_message = on_message
client.connect("your-broker.com", 8883, 60)
client.subscribe("abelara/plant1/utilities/water-system/pump-station/pump-101/+")
client.loop_forever()
```

**Filter by Schema Type:**
```python
# Subscribe to only alerts
client.subscribe("abelara/+/+/+/+/+/alert")

# Subscribe to all edge data
client.subscribe("abelara/+/+/+/+/+/edge/+")

# Subscribe to specific measurements
client.subscribe("abelara/+/+/+/+/+/measurement/vibration-analysis")
```

### Customization Guide

**1. Adapt for Your Equipment:**
```python
# Update asset configuration
PUMP_ID = 102
PUMP_NAME = "Compressor-A1"
PUMP_DESCRIPTION = "Primary air compressor"

# Modify data generation functions
def create_asset_payload():
    return {
        "id": PUMP_ID,
        "name": PUMP_NAME,
        "assetType": {
            "id": 3,
            "name": "Rotary Compressor",
            "description": "Industrial air compressor"
        }
        # ... rest of payload
    }
```

**2. Add New Sensors:**
```python
def create_edge_payloads():
    sensors = [
        ("temperature", "Temperature", "°C", 85.0),
        ("pressure", "Pressure", "bar", 7.2),
        ("vibration", "Vibration", "mm/s", 2.1),
        ("flow", "Flow Rate", "m³/h", 42.5),
        # Add your sensors here
        ("humidity", "Humidity", "%", 65.0),
        ("power", "Power Consumption", "kW", 5.2)
    ]
    # ... payload generation logic
```

**3. Custom Topic Structure:**
```python
# Update base topic for your organization
BASE_TOPIC = "your-company/site1/production/line2/station5"

def get_topic(message_type, sub_type=None):
    topic = f"{BASE_TOPIC}/{ASSET_NAME.lower()}/{message_type}"
    if sub_type:
        topic += f"/{sub_type}"
    return topic
```

## 📚 Documentation

### Repository Structure
```
UNS-Payload-Examples/
├── schemas/                 # JSON Schema definitions
│   ├── asset/              # Asset schema + documentation
│   ├── alert/              # Alert schema + documentation
│   ├── state/              # State schema + documentation
│   └── ...                 # All 10 schema types
├── examples/               # Working code examples
│   ├── pump_mqtt_publisher.py  # Sample Python example
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Example documentation
├── README.md              # This comprehensive guide
├── style-guide.md         # Schema development standards
└── LICENSE               # MIT License
```

### Key Documents

- **[Main README](README.md)**: sample payload examples and architecture guide
- **[Schema Documentation](schemas/README.md)**: Detailed schema specifications
- **[Style Guide](style-guide.md)**: Development standards and best practices
- **[Python Example](examples/README.md)**: Implementation guide and usage
- **Individual Schema Docs**: Each schema has detailed documentation with examples

### Schema Validation Tools

**Python (recommended):**
```python
from jsonschema import validate
import json

# Load schema and validate payload
with open('schemas/asset/asset.json') as f:
    schema = json.load(f)

validate(payload, schema)  # Raises exception if invalid
```

**Command Line:**
```bash
# Using ajv-cli (npm install -g ajv-cli)
ajv validate -s schemas/asset/asset.json -d payload.json

# Using jsonschema (pip install jsonschema)
jsonschema -i payload.json schemas/asset/asset.json
```

## ⚖️ License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ **Commercial use allowed**
- ✅ **Modification allowed**  
- ✅ **Distribution allowed**
- ✅ **Private use allowed**
- ⚠️ **No warranty provided**
- ⚠️ **License and copyright notice required**

---

## ⚠️ Important Disclaimer

**This project provides sample schemas and examples for educational purposes only.**

- ❌ **Not a standard** - These are example patterns, not official specifications
- ❌ **Not comprehensive** - Limited scope covering basic industrial scenarios
- ❌ **Not authoritative** - One possible approach among many valid alternatives
- ❌ **Not production-ready without customization** - Adapt for your specific needs

**✅ What this IS:**
- Educational examples of UNS concepts
- Sample JSON Schema patterns
- Working code demonstrating validation
- Starting point for your own implementation

**Use this project to learn and experiment, then design your own schemas that fit your specific industrial requirements.**

## 🚀 Get Started Learning

1. **Clone this repository** to explore the examples
2. **Run the Python example** to see concepts in action
3. **Study the schema patterns** for learning purposes
4. **Design your own schemas** based on your specific needs
5. **Build your own UNS implementation!**

*Learn UNS concepts through practical examples - then build your own solution.* 