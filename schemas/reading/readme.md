# Reading Schema

[← Back to Root](../../README.md)

The reading schema defines the structure for reading information in the Abelara MES system. It represents raw sensor readings or process values with minimal processing.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

The schema defines the minimum required fields while allowing additional properties to be included based on specific reading requirements.

## Required Fields

| Field         | Type   | Description                                  |
|---------------|--------|----------------------------------------------|
| `timestamp`   | string | When the reading was taken (ISO 8601)        |
| `type`        | object | Measurement type information                 |
| `value`       | number | The actual reading value                     |
| `unit`        | string | Unit of measure for the reading             |
| `metadata`    | object | Standard metadata about the reading         |

### Type Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Measurement type identifier                |
| `name`        | string | Measurement type name                      |
| `description` | string | Measurement type description               |

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

## Additional Properties

The schema allows for additional properties to be included in the reading data. This flexibility enables different types of readings to include context-specific information. However, core reading attributes like quality, sampling rates, or timing characteristics should be handled at the Measurement level rather than in the raw reading.

The `additionalInfo` object in the metadata section is the preferred location for any edge-specific or contextual information that needs to be preserved with the reading.

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
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1",
      "description": "Primary filling machine"
    },
    "additionalInfo": {
      "batch": "B12345",
      "processStep": "Heating",
      "recipeId": "RECIPE-001"
    }
  }
}
```
