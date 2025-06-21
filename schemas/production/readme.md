# Production Schema

[← Back to Root](../../README.md)

The production schema defines the structure for production information in the Abelara MES system. It represents production runs, batches, or work orders with associated counts and metadata.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `timestamp`   | string | When the production was recorded (ISO 8601) |
| `start_ts`    | string | Start of production run (ISO 8601)         |
| `end_ts`      | string | End of production run (ISO 8601), null if active |
| `metadata`    | object | Additional context about the production    |
| `counts`      | array  | Array of count entries                     |

### Count Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `type`        | object | Count type reference                       |
| `quantity`    | number | Count amount                               |
| `timestamp`   | string | When count was recorded (ISO 8601)         |

### Count Type Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Count type identifier                      |
| `name`        | string | Count type name                            |
| `description` | string | Count type description                     |
| `unit`        | string | Unit of measure for the count              |

### Metadata Fields

| Field            | Type   | Description                                |
|------------------|--------|--------------------------------------------|
| `source`         | string | Source system                              |
| `uri`            | string | Data source path                           |
| `asset`          | object | Asset reference                            |
| `product`        | object | Product information                        |
| `additionalInfo` | object | Additional edge-driven metadata            |

### Asset Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Asset identifier                           |
| `name`        | string | Asset name                                 |
| `description` | string | Asset description                          |

### Product Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Product identifier                         |
| `name`        | string | Product name                               |
| `description` | string | Product description                        |
| `family`      | object | Product family information                 |
| `idealCycleTime` | number | Target ideal cycle time in seconds      |
| `tolerance`   | number | Allowed variance (0-1)                     |
| `unit`        | string | Unit of measure (default: "each")          |

### Product Family Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Family identifier                          |
| `name`        | string | Family name                                |
| `description` | string | Family description                         |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00Z",
  "start_ts": "2024-03-20T14:00:00Z",
  "end_ts": null,
  "counts": [
    {
      "type": {
        "id": 1,
        "name": "Good",
        "description": "Acceptable finished goods",
        "unit": "each"
      },
      "quantity": 1250,
      "timestamp": "2024-03-20T14:30:00Z"
    },
    {
      "type": {
        "id": 2,
        "name": "Scrap",
        "description": "Rejected products",
        "unit": "each"
      },
      "quantity": 25,
      "timestamp": "2024-03-20T14:30:00Z"
    }
  ],
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1",
      "description": "Primary filling machine"
    },
    "product": {
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
      }
    },
    "additionalInfo": {
      "batchId": "B12345",
      "orderId": "PO-789",
      "sequence": 1,
      "stage": "Filling"
    }
  }
}
```
