# Count Schema

[← Back to Root](../../README.md)

The count schema defines the structure for count information in the Abelara MES system. It represents accumulated values such as production counts, runtime hours, or other cumulative measurements.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `timestamp`   | string | When the count was recorded (ISO 8601)     |
| `value`       | number | The count quantity (must be >= 0)          |
| `unit`        | string | Unit of measure (e.g., "units", "kg")      |
| `type`        | object | Count type information                     |
| `metadata`    | object | Standard metadata about the count          |

### Type Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Count type identifier                      |
| `name`        | string | Count type name (e.g., "Infeed", "Waste")  |
| `description` | string | Count type description                     |

### Metadata Fields

| Field            | Type   | Description                                |
|------------------|--------|--------------------------------------------|
| `source`         | string | Source system or service                   |
| `uri`            | string | Data source path/identifier                |
| `asset`          | object | Asset reference                            |
| `production`     | object | Production run information                 |
| `product`        | object | Product information                        |
| `additionalInfo` | object | Additional edge-driven metadata            |

### Asset Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Asset identifier                           |
| `name`        | string | Asset name                                 |
| `description` | string | Asset description                          |

### Production Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Production run identifier                  |
| `name`        | string | Production run name                        |
| `description` | string | Production run description                 |

### Product Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Product identifier                         |
| `name`        | string | Product name                               |
| `description` | string | Product description                        |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "value": 42,
  "unit": "units",
  "type": {
    "id": 1,
    "name": "Outfeed",
    "description": "Finished units or good output"
  },
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBD4",
    "asset": {
      "id": 102,
      "name": "Filler 1",
      "description": "Primary filling machine"
    },
    "production": {
      "id": 1234,
      "name": "Run 1234",
      "description": "Morning shift production run"
    },
    "product": {
      "id": 456,
      "name": "Product A",
      "description": "Standard product variant"
    },
    "additionalInfo": {
      "shift": "A",
      "operator": "John Smith",
      "batch": "B12345"
    }
  }
}
```