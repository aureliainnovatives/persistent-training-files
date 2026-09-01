# Customer Transformation Requirements

## Goal
Migrate customer records from a legacy CRM into the canonical Customer Platform format.

## Requirements
- REQ-01: Preserve the legacy customer number as the target customer ID.
- REQ-02: Build full name from first name and last name.
- REQ-03: Normalize email addresses to lowercase. Email is optional, but if supplied it must be valid.
- REQ-04: Normalize valid Indian 10-digit mobile numbers to `+91-XXXXXXXXXX`.
- REQ-05: Convert known state codes to full state names: `MH` → `Maharashtra`, `KA` → `Karnataka`, `DL` → `Delhi`.
- REQ-06: Trim leading/trailing whitespace from textual source values.
- REQ-07: Never invent missing or malformed phone numbers, email addresses, names, IDs, or states.
- REQ-08: Unknown state codes must be flagged for review rather than guessed.
- REQ-09: Duplicate customer IDs must be detected.
- REQ-10: Records that cannot be safely repaired must be quarantined.
