# KPI Schema

[← Back to Root](../../README.md)

The KPI schema defines the structure for Key Performance Indicator information in the Abelara MES system. It represents calculated performance metrics such as OEE, efficiency, or other business indicators.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `timestamp`   | string | When the KPI was recorded (ISO 8601)       |
| `value`       | number | KPI value (must be >= 0)                   |
| `unit`        | string | Unit of measure                            |
| `type`        | object | KPI type information                       |
| `metadata`    | object | Additional context about the KPI           |

### Type Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Type identifier                            |
| `name`        | string | Type name                                  |
| `description` | string | Type description                           |

### Metadata Fields

| Field            | Type   | Description                                |
|------------------|--------|--------------------------------------------|
| `source`         | string | Source system                              |
| `uri`            | string | Data source path                           |
| `asset`          | object | Asset reference                            |
| `additionalInfo` | object | Additional custom fields                   |

### Asset Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Asset identifier                           |
| `name`        | string | Asset name                                 |

### Product Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Product identifier                         |
| `name`        | string | Product name                               |
| `description` | string | Product description                        |
| `family`      | object | Product family information                 |

### Product Family Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Family identifier                          |
| `name`        | string | Family name                                |
| `description` | string | Family description                         |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "value": 85.5,
  "unit": "%",
  "type": {
    "id": 1,
    "name": "OEE",
    "description": "Overall Equipment Effectiveness"
  },
  "product": {
    "id": 1,
    "name": "Product A",
    "description": "Main product line",
    "family": {
      "id": 1,
      "name": "Beverages",
      "description": "Beverage products"
    }
  },
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1"
    },
    "additionalInfo": {
      "availability": 90.0,
      "performance": 95.0,
      "quality": 98.0
    }
  }
}
```
