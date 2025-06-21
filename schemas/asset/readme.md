# Asset Schema

[← Back to Root](../../README.md)

The asset schema defines the structure for asset information and configuration in the Abelara MES system. This schema is used to publish asset details, updates, and configuration changes.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field         | Type   | Description                                  |
|---------------|--------|----------------------------------------------|
| `timestamp`   | string | When the asset information was recorded (ISO 8601) |
| `id`          | number | Asset identifier                             |
| `name`        | string | Asset name                                   |
| `description` | string | Detailed asset description                   |
| `assetType`   | object | Asset type information                       |
| `metadata`    | object | Standard metadata about the asset           |

### Asset Type Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Asset type identifier                       |
| `name`        | string | Asset type name                             |
| `description` | string | Asset type description                      |

### Parent Asset Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `id`          | number | Parent asset identifier                     |
| `name`        | string | Parent asset name                           |
| `description` | string | Parent asset description                    |

### Metadata Fields

| Field            | Type   | Description                                |
|------------------|--------|--------------------------------------------|
| `source`         | string | Source system or service                   |
| `uri`            | string | Data source path/identifier                |
| `additionalInfo` | object | Additional edge-driven metadata            |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00.123Z",
  "id": 101,
  "name": "CNC Machine-03",
  "description": "5-axis CNC Mill for high-precision parts",
  "assetType": {
    "id": 1,
    "name": "Machining Center",
    "description": "CNC machining equipment"
  },
  "parentAsset": {
    "id": 22,
    "name": "Production Line 1",
    "description": "Main production line"
  },
  "metadata": {
    "source": "asset-management",
    "uri": "asset://101",
    "additionalInfo": {
      "manufacturer": "Haas",
      "model": "VF-2",
      "serialNumber": "H123456",
      "installationDate": "2023-06-15"
    }
  }
}
``` 