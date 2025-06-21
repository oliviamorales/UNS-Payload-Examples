# Measurement Schema

[← Back to Root](../../README.md)

The measurement schema defines the structure for measurement information in the Abelara MES system. It represents precision measurements taken manually or automatically for quality control, maintenance, or process monitoring.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field         | Type   | Description                                  |
|---------------|--------|----------------------------------------------|
| `timestamp`   | string | When the measurement was taken (ISO 8601)    |
| `type`        | object | Measurement type information                 |
| `value`       | number | The actual measurement value                 |
| `unit`        | string | Unit of measure                             |
| `metadata`    | object | Standard metadata about the measurement     |

### Type Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Measurement type identifier                |
| `name`        | string | Measurement type name                      |
| `description` | string | Measurement type description               |

### Quality Control Fields

| Field         | Type    | Description                                |
|---------------|---------|---------------------------------------------|
| `target`      | number  | Target value for the measurement           |
| `tolerance`   | number  | Tolerance value for the measurement        |
| `inTolerance` | boolean | Whether the measurement is within tolerance|

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

### Production Context

The schema allows for production context information through the `productionContext` object. This can include any additional production-related data that provides context for the measurement.

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "type": {
    "id": 1,
    "name": "Temperature",
    "description": "Temperature readings from process equipment"
  },
  "value": 42.5,
  "unit": "°C",
  "target": 40.0,
  "tolerance": 5.0,
  "inTolerance": true,
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
      "calibrationDate": "2024-01-15"
    }
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
  "productionContext": {
    "batchId": "B12345",
    "orderId": "PO-789",
    "sequence": 1,
    "stage": "Filling"
  }
}
```
