# Value Schema

[← Back to Root](../../README.md)

The value schema defines the structure for generic value information in the Abelara MES system. It represents simple key-value pairs with metadata.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field       | Type   | Description                                |
|-------------|--------|--------------------------------------------|
| `timestamp` | string | When the value was taken (ISO 8601)        |
| `value`     | number | The actual value                           |
| `unit`      | string | Unit of measure                            |
| `metadata`  | object | Standard metadata about the value          |

### Metadata Fields

| Field            | Type   | Description                                |
|------------------|--------|--------------------------------------------|
| `source`         | string | Source system or service                   |
| `uri`            | string | Data source path/identifier                |
| `asset`          | object | Asset reference                            |
| `additionalInfo` | object | Additional edge-driven metadata            |

### Asset Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Asset identifier                           |
| `name`        | string | Asset name                                 |
| `description` | string | Asset description                          |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "value": 42.5,
  "unit": "°C",
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1",
      "description": "Primary filling machine"
    },
    "additionalInfo": {
      "sensorId": "TEMP-001",
      "location": "Tank 1"
    }
  }
}
```
