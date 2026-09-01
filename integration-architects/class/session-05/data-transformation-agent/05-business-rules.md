# Customer Transformation Business Rules

## Scope

These rules define the approved business behavior for migrating legacy CRM
customer records into the canonical Customer Platform format. They are based
only on `01-source-schema.yaml`, `02-target-schema.yaml`, and
`03-business-requirements.md`.

## Rules

### BR-01: Preserve the legacy customer number

- **Rule ID:** BR-01
- **Requirement ID:** REQ-01
- **Business description:** Preserve the legacy customer number as the target customer ID.
- **Source field(s):** `customer.cust_no`
- **Target field:** `customer.customerId`
- **Transformation/normalization:** Trim leading and trailing whitespace. Do not change the remaining value or generate a replacement.
- **Validation:** The resulting value must be present and must satisfy the target pattern `^C[0-9]{4}$`.
- **Error handling:** Preserve the supplied value for diagnostics, mark the record invalid, and quarantine it when the target ID is missing or does not satisfy the target pattern. Do not pad, truncate, or otherwise rewrite it.
- **Determinism / human review:** Trimming and pattern validation are deterministic. A pattern violation requires human review.

### BR-02: Build the customer full name

- **Rule ID:** BR-02
- **Requirement ID:** REQ-02
- **Business description:** Build the canonical full name from the customer's first and last names.
- **Source field(s):** `customer.first_name`, `customer.last_name`
- **Target field:** `customer.fullName`
- **Transformation/normalization:** Trim both source values and join the non-empty values with one space. If the optional last name is absent, use the trimmed first name only.
- **Validation:** `customer.first_name` must be present and non-empty after trimming. The resulting `fullName` must be present and non-empty.
- **Error handling:** Do not invent or substitute a name. Preserve the source values for diagnostics and quarantine the record if the required first name is missing, empty, or malformed.
- **Determinism / human review:** Joining and whitespace normalization are deterministic. A missing or malformed required name requires human review.

### BR-03: Normalize and validate email

- **Rule ID:** BR-03
- **Requirement ID:** REQ-03
- **Business description:** Normalize a supplied email address to lowercase while retaining the optional nature of the field.
- **Source field(s):** `customer.mail`
- **Target field:** `customer.email`
- **Transformation/normalization:** Trim leading and trailing whitespace, then lowercase the supplied text. Do not create an email when the source value is absent.
- **Validation:** An absent value is valid because the target field is optional. A supplied value must pass the project's approved email validity check after trimming and before or after lowercasing as applicable.
- **Error handling:** Preserve the lowercased supplied text without inventing or correcting it. Mark the field invalid and quarantine the record when a supplied email is malformed, unless a downstream process explicitly supports non-quarantined invalid records.
- **Determinism / human review:** Trimming, lowercasing, and validity checking are deterministic. Deciding how to repair a malformed email requires human review; no repair is authorized by this requirement.

### BR-04: Normalize valid Indian mobile numbers

- **Rule ID:** BR-04
- **Requirement ID:** REQ-04
- **Business description:** Format valid Indian 10-digit mobile numbers in the canonical international form.
- **Source field(s):** `customer.mobile`
- **Target field:** `customer.phone`
- **Transformation/normalization:** Trim the source value. If the result contains exactly 10 numeric digits, prefix it with `+91-`. Do not add the prefix to values with any other length or non-numeric content.
- **Validation:** An absent value is valid because the target field is optional. A supplied value is transformable only when it is exactly 10 numeric digits after trimming. Other supplied values remain identifiable as invalid.
- **Error handling:** Preserve an invalid supplied value for downstream validation and do not invent, truncate, pad, or otherwise repair it. Quarantine the record when the phone value cannot be safely accepted.
- **Determinism / human review:** Trimming, digit/length checking, and formatting are deterministic. Any repair of an invalid phone number requires human review.

### BR-05: Convert known state codes

- **Rule ID:** BR-05
- **Requirement ID:** REQ-05
- **Business description:** Convert approved legacy state codes to their canonical full state names.
- **Source field(s):** `customer.state`
- **Target field:** `customer.state`
- **Transformation/normalization:** Trim the source value and apply only this approved mapping: `MH` -> `Maharashtra`, `KA` -> `Karnataka`, `DL` -> `Delhi`.
- **Validation:** The source state is required. A trimmed value must be present. Only the three approved codes may be converted; no other code or state name may be guessed or mapped by this rule.
- **Error handling:** Preserve an unknown or malformed value for downstream validation, flag the record for review, and quarantine it when it cannot be safely accepted. Do not substitute a state name.
- **Determinism / human review:** Trimming and the three listed mappings are deterministic. Unknown or malformed state values require human review, as required by REQ-08.

### BR-06: Trim textual source values

- **Rule ID:** BR-06
- **Requirement ID:** REQ-06
- **Business description:** Remove leading and trailing whitespace from textual source values before validation and mapping.
- **Source field(s):** `customer.cust_no`, `customer.first_name`, `customer.last_name`, `customer.mail`, `customer.mobile`, `customer.state`
- **Target field:** The corresponding target field populated from each source field: `customerId`, `fullName`, `email`, `phone`, or `state`
- **Transformation/normalization:** Apply one leading/trailing whitespace trim to each supplied textual value. Internal whitespace is not changed by this rule.
- **Validation:** Values are validated after trimming against the requiredness, target pattern, email, phone, and state rules defined in BR-01 through BR-05.
- **Error handling:** Do not treat a whitespace-only required value as valid. Preserve the original value for diagnostics and apply the field-specific error handling from the related rule.
- **Determinism / human review:** Trimming and whitespace-only detection are deterministic. Any subsequent repair of an invalid value requires human review.

### BR-07: Do not invent or repair source values

- **Rule ID:** BR-07
- **Requirement ID:** REQ-07
- **Business description:** Transformation must not create, infer, or silently correct missing or malformed customer values.
- **Source field(s):** `customer.cust_no`, `customer.first_name`, `customer.last_name`, `customer.mail`, `customer.mobile`, `customer.state`
- **Target field:** `customerId`, `fullName`, `email`, `phone`, `state`
- **Transformation/normalization:** Permit only the explicit normalization and mappings in BR-01 through BR-06. Missing optional values remain absent; missing required values and malformed supplied values remain invalid.
- **Validation:** Each target value must satisfy its target schema and the applicable rule-specific validation. No source value may be replaced with a guessed value.
- **Error handling:** Retain the original supplied value where possible for diagnostics, record the validation failure, and route unsafe records to quarantine under BR-10.
- **Determinism / human review:** Enforcement is deterministic. Choosing a replacement or repair requires human review and is outside the approved transformation scope.

### BR-08: Flag unknown state codes

- **Rule ID:** BR-08
- **Requirement ID:** REQ-08
- **Business description:** Unknown state codes must be explicitly identified for review rather than interpreted.
- **Source field(s):** `customer.state`
- **Target field:** `customer.state`
- **Transformation/normalization:** Trim the value. Apply only the BR-05 mapping table; leave an unknown code unchanged.
- **Validation:** The value must be one of `MH`, `KA`, or `DL` to be transformed by this mapping. Any other non-empty value is unknown for this rule.
- **Error handling:** Preserve the unknown value, attach a review flag or validation error, and do not guess a full state name. Quarantine the record when required by BR-10.
- **Determinism / human review:** Identifying and flagging an unknown code is deterministic. Selecting the correct replacement requires human review.

### BR-09: Detect duplicate customer IDs

- **Rule ID:** BR-09
- **Requirement ID:** REQ-09
- **Business description:** Detect multiple records that resolve to the same target customer ID.
- **Source field(s):** `customer.cust_no`
- **Target field:** `customer.customerId`
- **Transformation/normalization:** Compare IDs after the BR-01 and BR-06 trimming normalization. No deduplication, merge, or ID generation is authorized.
- **Validation:** Each normalized target customer ID must be unique within the migration input set.
- **Error handling:** Flag all records participating in a duplicate group, retain their source data, and quarantine them until an approved record-selection or merge decision is made.
- **Determinism / human review:** Duplicate detection is deterministic. Resolving which record to retain or whether records should be merged requires human review.

### BR-10: Quarantine records that are unsafe to transform

- **Rule ID:** BR-10
- **Requirement ID:** REQ-10
- **Business description:** Prevent records with unresolved validation, identity, or mapping problems from entering the canonical target dataset.
- **Source field(s):** All source fields in the `customer` object
- **Target field:** The complete target customer record
- **Transformation/normalization:** Apply BR-01 through BR-09 before deciding whether the record is safe to publish.
- **Validation:** A record is publishable only when required target fields are valid, the target ID is valid and unique, supplied optional values are valid, and no unresolved unknown state or other unsafe value remains.
- **Error handling:** Route unsafe records to quarantine with the original record, applicable rule IDs, validation failures, and review status. Do not publish a partial or guessed target record as a successful transformation.
- **Determinism / human review:** The quarantine decision based on validation results is deterministic. Release, repair, merge, or otherwise resolve a quarantined record requires human review.

## Assumptions and Explicit Gaps

- **A-01:** `cust_no` is expected to satisfy the target schema pattern `^C[0-9]{4}$` because REQ-01 requires preservation and the target schema makes the pattern mandatory. The requirements do not authorize changing a non-conforming legacy ID, so such an ID is flagged rather than rewritten.
- **A-02:** “Valid email” means the validity check defined by the consuming platform or approved validation standard. The requirements do not specify an exact syntax, domain policy, or deliverability check; no stricter rule is invented here.
- **A-03:** “Valid Indian 10-digit mobile” is operationalized only as exactly 10 numeric digits after trimming, because no additional numbering-range or leading-digit rule is provided. The `+91-` prefix is added only after that check.
- **A-04:** A missing optional last name produces a full name containing the first name only. The requirements do not specify whether a missing last name should instead invalidate the record.
- **A-05:** The source schema marks `last_name`, `mail`, and `mobile` optional, while `cust_no`, `first_name`, and `state` are required. This requiredness is honored; no additional required fields are introduced.
- **A-06:** The target schema does not define a target-side error, review, or quarantine field. Review flags, validation errors, and quarantined records are therefore treated as migration-control metadata or an operational quarantine output, not as invented target customer fields.
- **A-07:** Duplicate detection is performed across the complete migration input set after ID trimming. The requirements do not define survivorship, merge precedence, or an allowed duplicate exception, so duplicates require human review.