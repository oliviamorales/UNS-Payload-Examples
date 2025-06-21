# MQTT Payload Schemas

[← Back to Root](../README.md)

## Table of Contents
- [Overview](#overview)
- [Design Principles](#design-principles)
- [Schema Types](#schema-types)
- [Standard Patterns](#standard-patterns)
- [Validation Rules](#validation-rules)
- [Common Properties](#common-properties)
- [Schema Keys](#schema-keys)
- [Usage Guidelines](#usage-guidelines)
- [Best Practices](#best-practices)

> **Note**: For detailed implementation guidelines, best practices, and standards, see the [Style Guide](../style-guide.md).

## Overview

This directory contains sample JSON Schema definitions for MQTT payloads demonstrating UNS concepts. These are educational examples showing one possible approach to industrial data modeling - not definitive standards or comprehensive specifications.

## Design Principles

1. **Clear and Descriptive**
   - Use full, descriptive property names
   - Maintain reasonable payload size
   - Focus on readability and maintainability

2. **Consistency**
   - Common metadata structure
   - Standard timestamp format
   - Uniform type handling
   - Consistent property naming

3. **Extensibility**
   - Choice of extensibility approaches:
     - Strict: Use additionalProperties: false with metadata.additionalInfo
     - Open: Use additionalProperties: true
     - Flexible: Leave additionalProperties unspecified
   - Versioning strategy
   - Backward compatibility

4. **Validation**
   - Strong typing and required fields
   - Clear validation rules
   - Consistent patterns

## Schema Types

- [Alert Schema](alert/readme.md) - System alerts and notifications
- [Asset Schema](asset/readme.md) - Asset information and configuration
- [Count Schema](count/readme.md) - Production counts
- [KPI Schema](kpi/readme.md) - Key Performance Indicators
- [Measurement Schema](measurement/readme.md) - Measurement data
- [Product Schema](product/readme.md) - Product information
- [Production Schema](production/readme.md) - Production records
- [Reading Schema](reading/readme.md) - Raw reading data
- [State Schema](state/readme.md) - Equipment operational states
- [Value Schema](value/readme.md) - Generic value measurements

**Note**: "Edge" is a namespace concept in topic paths (e.g., `.../edge/temperature`) for real-time sensor data, not a separate schema type. Edge payloads use the same schema structures as other payloads.

Each schema type has its own detailed documentation and JSON schema definition.

## Standard Patterns

### Type Objects
```json
{
  "type": {
    "id": 1,
    "name": "Running",
    "description": "Machine is running normally"
  }
}
```

### Asset Objects
```json
{
  "asset": {
    "id": 102,
    "name": "Filler 1",
    "description": "Primary filling machine"
  }
}
```

### Product Objects
```json
{
  "product": {
    "id": 19,
    "name": "Widget A",
    "description": "Standard widget",
    "family": {
      "id": 1,
      "name": "Widget Family",
      "description": "Standard widgets product family"
    }
  }
}
```

### Metadata Structure
```json
{
  "metadata": {
    "source": "node-red",
    "uri": "opc://plc1/DB1.DBW0",
    "asset": {
      "id": 102,
      "name": "Filler 1"
    }
  }
}
```

Note: The metadata structure can be extended based on your chosen extensibility approach. See the Style Guide for details.

## Validation Rules

### Time and Dates
- All timestamps must be ISO 8601 format with timezone
- Production records must include both `start_ts` and `end_ts`
- Format: `YYYY-MM-DDThh:mm:ss.sssZ` or `YYYY-MM-DDThh:mm:ss.sss±HH:MM`

### Numbers
- All IDs must be numbers
- Count values must be >= 0
- Tolerance values must be between 0 and 1

### Visual Elements
- Color codes must follow #RRGGBB format (e.g., #00FF00)

### Required Fields
Every message must include:
- `timestamp`: When the event/data was recorded
- `metadata`: Contextual information about the message

Metadata must always include:
- `source`: System or service that generated the message
- `uri`: Data source path/identifier
- `asset`: Reference to the associated asset

Note: Additional fields may be included based on your chosen extensibility approach.

## Common Properties

All schemas share these base properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `timestamp` | string | Yes | ISO 8601 timestamp with timezone |
| `metadata` | object | Yes | Common metadata structure |
| `metadata.source` | string | Yes | Source system or service |
| `metadata.uri` | string | Yes | Data source path |
| `metadata.asset` | object | Yes | Asset reference |

Note: Schema extensibility options determine how additional properties are handled. See the Style Guide for details.

## Schema Keys

| Key | Type | Description | Example | Validation |
|-----|------|-------------|---------|------------|
| `id` | number | Identifier | `102` | Required |
| `name` | string | Human-readable name | `"Filler 1"` | Required |
| `description` | string | Detailed description | `"Primary filling machine"` | Optional |
| `timestamp` | string | ISO 8601 timestamp | `"2024-03-20T14:30:00Z"` | Required, ISO 8601 |
| `start_ts` | string | Start timestamp | `"2024-03-20T14:30:00Z"` | ISO 8601 |
| `end_ts` | string | End timestamp | `"2024-03-20T15:30:00Z"` | ISO 8601 |
| `value` | number/string | Primary value | `42` or `"RUNNING"` | Type-specific |
| `unit` | string | Unit of measure | `"kg"`, `"pcs"` | Required for measurements |
| `target` | number | Target value | `100` | Optional |
| `tolerance` | number | Tolerance | `0.5` | 0-1 range |
| `inTolerance` | boolean | Within tolerance | `true` | Optional |
| `color` | string | Visual indicator | `"#00FF00"` | #RRGGBB format |
| `severity` | number | Alert severity | `1` | 1-5 range |
| `code` | string | Status/error code | `"E001"` | Type-specific |

## Usage Guidelines

1. Schema Selection:
   - Choose the most specific schema type
   - Use base schemas for simple cases
   - Choose appropriate extensibility approach

2. Required Fields:
   - Include all required base fields
   - Add schema-specific required fields
   - Validate against schema definition

3. Metadata Usage:
   - Always include required metadata
   - Follow chosen extensibility approach
   - Maintain consistent structure

4. Validation:
   - Validate against JSON Schema
   - Check required fields
   - Verify data types
   - Test edge cases

## Best Practices

1. Message Structure:
   - Keep payloads focused
   - Use clear field names
   - Follow standard patterns
   - Include proper context

2. Data Types:
   - Use correct formats
   - Follow validation rules
   - Handle edge cases
   - Document constraints

3. Metadata:
   - Include full context
   - Use standard fields
   - Document extensions
   - Keep it relevant

4. Documentation:
   - Document all fields
   - Include examples
   - Explain validation
   - Keep docs updated 