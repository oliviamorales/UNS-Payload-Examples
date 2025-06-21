# Product Schema

[← Back to Root](../../README.md)

The product schema defines the structure for product information in the Abelara MES system. It represents product specifications, families, and related metadata.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `timestamp`   | string | When the product was recorded (ISO 8601)   |
| `id`          | number | Product identifier                         |
| `name`        | string | Product name                               |
| `description` | string | Product description                        |
| `family`      | object | Product family information                 |
| `metadata`    | object | Additional context about the product       |

### Manufacturing Fields

| Field            | Type   | Description                                |
|------------------|--------|--------------------------------------------|
| `idealCycleTime` | number | Target cycle time in seconds               |
| `tolerance`      | number | Allowed variance (0-1)                     |
| `unit`           | string | Unit of measure (default: "each")          |

### Family Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Family identifier                          |
| `name`        | string | Family name                                |
| `description` | string | Family description                         |

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
| `description` | string | Asset description                          |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00Z",
  "id": 1,
  "name": "Product A",
  "description": "Main product line",
  "idealCycleTime": 2.5,
  "tolerance": 0.05,
  "unit": "each",
  "family": {
    "id": 1,
    "name": "Beverages",
    "description": "Beverage products"
  },
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1",
      "description": "Primary filling machine"
    },
    "additionalInfo": {
      "customField1": "value1",
      "customField2": 42
    }
  }
}
```
