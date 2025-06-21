# Abelara Payload Style Guide

[← Back to Root](README.md)

## Table of Contents
- [Overview](#overview)
- [Core Principles](#core-principles)
  - [Clear and Descriptive](#1-clear-and-descriptive)
  - [Consistency](#2-consistency)
  - [Extensibility](#3-extensibility)
  - [Validation](#4-validation)
- [Schema Structure](#schema-structure)
  - [Topic Structure](#1-topic-structure)
  - [Standard Object Patterns](#2-standard-object-patterns)
  - [Required Fields](#3-required-fields)
  - [Validation Rules](#4-validation-rules)
  - [Property Naming](#5-property-naming)
  - [Common Properties](#6-common-properties)
  - [Data Types](#7-data-types)
  - [Timestamps](#8-timestamps)
  - [Type Definitions](#9-type-definitions)
  - [Metadata Structure](#10-metadata-structure)
- [Best Practices](#best-practices)
- [Example: Building the Reading Schema](#example-building-the-reading-schema)

For a quick reference of all detailed schemas and their examples, see the `/schemas` directory and the README in each schema folder.

## Overview

This style guide defines the standards and best practices for MQTT message schemas in the Abelara MES system. The schemas follow Web of Things (WoT) principles and are designed to be efficient, consistent, and extensible.

At Abelara, we believe that **clarity is a gift to the next developer.** Consistency isn't about rules for rules' sake - it's about honoring the craft, building trust, and making teamwork effortless.

For detailed schema examples and implementation details, see the individual schema documentation:
   - [Alert Schema](../schemas/alert/readme.md) - System alerts and notifications
   - [Asset Schema](../schemas/asset/readme.md) - Asset information and configuration
   - [Count Schema](../schemas/count/readme.md) - Production counts
   - [KPI Schema](../schemas/kpi/readme.md) - Key Performance Indicators
   - [Measurement Schema](../schemas/measurement/readme.md) - Measurement data
   - [Product Schema](../schemas/product/readme.md) - Product information
   - [Production Schema](../schemas/production/readme.md) - Production records
   - [Reading Schema](../schemas/reading/readme.md) - Reading data
   - [State Schema](../schemas/state/readme.md) - Equipment operational states
   - [Value Schema](../schemas/value/readme.md) - Generic value measurements

## Core Principles

### 1. Clear and Descriptive
- Use full, descriptive property names
- Maintain reasonable payload size
- Focus on readability and maintainability
- Enable flexible implementations

### 2. Consistency
- Common metadata structure
- Standard timestamp format
- Uniform type handling
- Consistent property naming

### 3. Extensibility

Schema extensibility can be handled in three ways:

#### Strict Mode (`additionalProperties: false`)
```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "timestamp": { "type": "string" },
    "metadata": {
      "additionalInfo": {
        "type": "object",
        "additionalProperties": true
      }
    }
  }
}
```
- ✓ Strict validation of field names
- ✓ Prevents typos in field names
- ✓ Clear separation of standard vs custom fields
- Use when field names must be controlled

#### Open Mode (`additionalProperties: true`)
```json
{
  "type": "object",
  "additionalProperties": true,
  "properties": {
    "timestamp": { "type": "string" }
  }
}
```
- ✓ Allows any additional fields
- ✓ More flexible
- ✓ Simpler schema
- Use when explicitly allowing extensions

#### Unspecified (Default)
```json
{
  "type": "object",
  "properties": {
    "timestamp": { "type": "string" }
  }
}
```
- ✓ Most flexible approach
- ✓ Simplest schema
- ✓ Future-proof
- Use when flexibility is preferred

Choose the approach that best fits your schema's needs. Required field validation is maintained regardless of which approach you choose.

### 4. Validation
- Strong typing and required fields
- Clear validation rules
- Consistent patterns

## Schema Structure

### 1. Topic Structure

MQTT topics follow the Unified Namespace (UNS) structure:
```
{enterprise}/{site}/{area}/{line}/{cell}/{equipment}/{messageType}
```

Where each level represents:
- `enterprise`: Company or organization identifier
- `site`: Physical location or plant
- `area`: Functional area within the site
- `line`: Production line or process line
- `cell`: Work cell or sub-line
- `equipment`: Individual device or machine
- `message`: Message being published

Messages can be published at any level of the hierarchy, following the path structure from left to right. Each level must maintain the defined order, but levels can be skipped when not applicable.

Examples:
```
# Enterprise level message
abelara/status

# Site level message
abelara/plant1/status

# Area level message
abelara/plant1/production/status

# Line level message
abelara/plant1/production/line1/status

# Cell level message
abelara/plant1/production/line1/cell1/status

# Equipment level message (attached to cell)
abelara/plant1/production/line1/cell1/device123/status

# Equipment level message (attached to line, skipping cell)
abelara/plant1/production/line1/device123/status

# Equipment level message (attached to area, skipping line and cell)
abelara/plant1/production/device123/status

# Equipment level message (attached to site, skipping area, line, and cell)
abelara/plant1/device123/status
```

Message types include:
- `alert`: System alerts and notifications
- `asset`: Asset information and configuration
- `count`: Production counts
- `measurement`: Measurement data
- `production`: Production records
- `reading`: Reading data
- `state`: Equipment operational states

### 2. Standard Object Patterns

All common objects must follow these structures:

```json
Type Object: {
  "id": "number",
  "name": "string",
  "description": "string"  // optional in some contexts
}

Asset Object: {
  "id": "number",
  "name": "string",
  "description": "string"  // optional
}

Product Object: {
  "id": "number",
  "name": "string",
  "description": "string",
  "family": {
    "id": "number",
    "name": "string",
    "description": "string"  // optional
  }
}
```

### 3. Required Fields

Every message must include:
- `timestamp`: When the event/data was recorded
- `metadata`: Contextual information about the message

Metadata must always include:
- `source`: System or service that generated the message
- `uri`: Data source path/identifier
- `asset`: Reference to the associated asset
- `additionalInfo`: Optional object for edge-specific data

### 4. Validation Rules

Time and Dates:
- All timestamps must be ISO 8601 format with timezone
- Production records must include both `start_ts` and `end_ts`

Visual Elements:
- Color codes must follow #RRGGBB format (e.g., #00FF00)

### 5. Property Naming

- Use camelCase for all property names
- Use full, descriptive names
- Avoid abbreviations except for common terms
- Maintain consistency across schemas

Examples:
```json
// Good
{
  "timestamp": "2024-07-28T14:30:03Z",
  "value": 42,
  "source": "sensor1"
}

// Bad
{
  "ts": "2024-07-28T14:30:03Z",
  "val": 42,
  "src": "sensor1" 
}
```

### 6. Common Properties

Every message payload must include:
```json
{
  "timestamp": "string",
  "metadata": {
    "source": "string",
    "uri": "string",
    "asset": {
      "id": "number",
      "value": "string"
    },
    "additionalInfo": {
      "type": "object",
      "additionalProperties": true
    }
  }
}
```

### 7. Data Types

Standard type requirements:
- `string`: Text and identifiers
  - Example: `"device123"`
  - Example: `"RUNNING"`
- `number`: Numeric values
  - Example: `42`
  - Example: `3.14159`
- `boolean`: True/false values
  - Example: `true`
  - Example: `false`
- `object`: Complex structures
  - Example: `{"key": "value"}`
- `array`: Lists
  - Example: `[1, 2, 3]`

### 8. Timestamps

- Use ISO 8601 date-time string format
- Always include timezone information (Z for UTC or +/-HH:MM offset)
- Format: `YYYY-MM-DDThh:mm:ss.sssZ` or `YYYY-MM-DDThh:mm:ss.sss±HH:MM`
- Examples:
  - `2024-07-28T14:30:03.123Z` (UTC with milliseconds)
  - `2024-07-28T12:30:03.123+02:00` (UTC+2 with milliseconds)

### 9. Type Definitions

Type definitions must follow this structure:
```json
{
  "type": {
    "id": "number",
    "name": "string",
    "description": "string"
  }
}
```

Examples:
```json
{
  "type": {
    "id": 1,
    "name": "Running",
    "description": "Machine is running normally"
  }
}
```

### 10. Metadata Structure

Structure:
- Use `additionalInfo` object for extensible metadata
- All metadata must follow the standard metadata pattern

Field Naming:
- Use camelCase for all field names
- Use descriptive names that indicate purpose
- Avoid abbreviations unless widely understood

Common Patterns:
- State Changes:
  - Include previous state information in metadata when relevant
  - Track state transitions with type and reason codes

- Measurements:
  - Include unit of measure
  - Include target and tolerance when applicable
  - Use `inTolerance` boolean for quick status checks

- Production Context:
  - Link to relevant production runs
  - Include product information when applicable
  - Use standardized unit measurements

## Best Practices

1. **Schema Design**
   - Keep schemas focused and single-purpose
   - Use clear, descriptive property names
   - Include proper validation rules
   - Document all fields and their purposes

2. **Metadata Usage**
   - Always include required metadata fields
   - Use additionalInfo for edge-driven data
   - Keep metadata consistent across schemas
   - Document any custom metadata fields

3. **Type Handling**
   - Use proper type definitions
   - Include type descriptions
   - Maintain type consistency
   - Document type enumerations

4. **Extensibility**
   - Use additionalInfo for custom fields
   - Maintain backward compatibility
   - Document extensions
   - Follow versioning guidelines

5. **Documentation**
   - Include clear descriptions
   - Provide usage examples
   - Document all fields
   - Keep documentation up to date

## Example: Building the Reading Schema

Let's walk through how we built the Reading schema following our style guide principles.

### Step 1: Core Structure

First, we establish the basic schema structure with required metadata:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://abelara.com/schemas/base/reading.json",
  "title": "Reading Schema",
  "description": "Schema for raw reading data from equipment or processes",
  "type": "object",
  "additionalProperties": false
}
```

### Step 2: Required Base Fields

We add the common required fields that all schemas must have:

```json
{
  // ... schema header ...
  "properties": {
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the reading was taken (ISO 8601 with timezone)"
    }
  },
  "required": ["timestamp"]
}
```

### Step 3: Type Definition

We add the type object following our standard pattern:

```json
{
  // ... previous properties ...
  "type": {
    "type": "object",
    "required": ["id", "name", "description"],
    "properties": {
      "id": {
        "type": "number",
        "description": "Measurement type identifier"
      },
      "name": {
        "type": "string",
        "description": "Measurement type name"
      },
      "description": {
        "type": "string",
        "description": "Measurement type description"
      }
    }
  }
}
```

### Step 4: Core Reading Properties

Add the essential properties for a reading:

```json
{
  // ... previous properties ...
  "value": {
    "type": "number",
    "description": "The actual reading value"
  },
  "unit": {
    "type": "string",
    "description": "Unit of measure for the reading"
  }
}
```

### Step 5: Metadata Structure

Add the standard metadata structure:

```json
{
  // ... previous properties ...
  "metadata": {
    "type": "object",
    "required": ["source", "uri", "asset"],
    "properties": {
      "source": {
        "type": "string",
        "description": "Source system or service that generated the reading"
      },
      "uri": {
        "type": "string",
        "description": "Data source path/identifier"
      },
      "asset": {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
          "id": {
            "type": "number",
            "description": "Asset identifier"
          },
          "name": {
            "type": "string",
            "description": "Asset name"
          },
          "description": {
            "type": "string",
            "description": "Asset description"
          }
        }
      }
    }
  }
}
```

### Step 6: Extension Point

Add the additionalInfo object for extensibility:

```json
{
  // ... previous properties ...
  "metadata": {
    // ... metadata properties ...
    "additionalInfo": {
      "type": "object",
      "description": "Additional edge-driven metadata",
      "additionalProperties": true
    }
  }
}
```

### Step 7: Required Fields

Define all required fields:

```json
{
  // ... schema content ...
  "required": [
    "timestamp",
    "type",
    "value",
    "unit",
    "metadata"
  ]
}
```

### Final Result

The complete Reading schema demonstrates:
1. Clear, focused purpose (raw reading data)
2. Standard patterns (Type, Asset objects)
3. Required base fields (timestamp, metadata)
4. Proper validation (types, formats)
5. Extension points (additionalInfo)
6. Complete documentation

This schema serves as a template for other schemas while maintaining its specific purpose of handling raw reading data. Each decision in its construction follows our style guide principles and patterns.
