# Alert Schema

[← Back to Root](../../README.md)

The alert schema defines the structure for alert information in the Abelara MES system. It represents a system alert or notification that may require operator acknowledgment.

## Overview

> **Note**: For general schema guidelines and best practices, see the [Style Guide](../../style-guide.md).

## Required Fields

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| `timestamp`   | string | When the alert occurred (ISO 8601)         |
| `severity`    | number | Alert severity (1-5)                       |
| `code`        | string | Alert code for categorization              |
| `message`     | string | Human-readable alert message               |
| `metadata`    | object | Additional context about the alert         |

### Severity Levels

| Level | Name      | Description                                     |
|-------|-----------|------------------------------------------------|
| 1     | Info      | Informational message, no action needed         |
| 2     | Warning   | Potential issue, monitor situation              |
| 3     | Error     | Issue requires attention                        |
| 4     | Critical  | Serious problem needs immediate attention       |
| 5     | Fatal     | System/safety critical, immediate action needed |

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

### Acknowledgment Fields

| Field            | Type    | Description                                |
|------------------|---------|---------------------------------------------|
| `acknowledged`   | boolean | Whether alert has been acknowledged         |
| `acknowledgedBy` | string  | User who acknowledged the alert            |
| `acknowledgedAt` | string  | When acknowledged (ISO 8601)               |

## Example

```json
{
  "timestamp": "2024-03-20T14:30:00Z",
  "severity": 4,
  "code": "TEMP_HIGH",
  "message": "Process temperature exceeds critical threshold",
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1",
      "description": "Primary filling machine"
    },
    "acknowledgment": {
      "acknowledged": false,
      "acknowledgedBy": null,
      "acknowledgedAt": null
    },
    "additionalInfo": {
      "temperature": 95.5,
      "threshold": 90.0,
      "unit": "°C"
    }
  }
}
```