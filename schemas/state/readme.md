# State Schema

[← Back to Root](../../README.md)

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

The state schema defines the structure for asset state information in the Abelara MES system.

## Required Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `timestamp`   | string | When the state was recorded (ISO 8601)     |
| `description` | string | Detailed state description                 |
| `color`       | string | Visual color code                          |
| `type`        | object | State type information                     |
| `metadata`    | object | Additional context about the state         |

### Type Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Type identifier                            |
| `name`        | string | Type name                                  |
| `description` | string | Type description                           |

### Metadata Fields

| Field            | Type   | Description                                |
|------------------|--------|--------------------------------------------|
| `source`         | string | Source system or service                   |
| `uri`            | string | Data source path/identifier                |
| `asset`          | object | Asset reference                            |
| `previousState`  | object | Previous state information                 |
| `additionalInfo` | object | Additional edge-driven metadata            |

### Asset Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Asset identifier                           |
| `name`        | string | Asset name                                 |
| `description` | string | Asset description                          |

### Previous State Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Previous state identifier                  |
| `name`        | string | Previous state name                        |
| `description` | string | Previous state description                 |
| `color`       | string | Previous state color                       |
| `type`        | object | Previous state type information            |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "description": "Asset is in normal operation",
  "color": "#00FF00",
  "type": {
    "id": 1,
    "name": "Production",
    "description": "Normal production state"
  },
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1",
      "description": "Primary filling machine"
    },
    "previousState": {
      "id": 2,
      "name": "Setup",
      "description": "Asset is being configured",
      "color": "#FFFF00",
      "type": {
        "id": 2,
        "name": "Setup",
        "description": "Setup and configuration state"
      }
    },
    "additionalInfo": {
      "mode": "AUTO",
      "operator": "John Smith"
    }
  }
}