# CONTRACTS

> Frozen APIs, schemas, interfaces, file formats, commands, and ownership rules.
> Contracts are frozen before implementation. Do not edit mid-slice without
> explicit human approval.

## Freeze status

| Field | Value |
| --- | --- |
| Current slice | `<slice id>` |
| Freeze timestamp | `<YYYY-MM-DD HH:MM TZ>` |
| Frozen by | `Fable` |
| Can change this slice? | `No; Fable must review and re-freeze before workers resume` |

## Public interfaces

| Name | Type | Location | Contract |
| --- | --- | --- | --- |
| `<name>` | `API/schema/component/CLI/file` | `<path>` | `<required behavior>` |

## Data schemas

| Schema | Location | Required fields | Notes |
| --- | --- | --- | --- |
| `<schema>` | `<path>` | `<fields>` | `<notes>` |

## Commands

| Command | Purpose | Expected result |
| --- | --- | --- |
| `<command>` | `<why it matters>` | `<exit/output>` |

## File ownership rules

| Area | Owner lane | Allowed files | Forbidden files |
| --- | --- | --- | --- |
| `<area>` | `<lane>` | `<paths>` | `<paths>` |

## Out-of-scope for current slice

- `<explicit non-goal>`
- `<explicit non-goal>`

## Contract change log

| Date | Change | Approved by | Reason |
| --- | --- | --- | --- |
| `<date>` | `<change>` | `Fable` | `<why>` |
