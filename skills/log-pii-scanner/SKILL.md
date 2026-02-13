---
name: log-pii-scanner
description: Scan log files in ~/Library/Logs for PII leaks (emails, phone numbers, account numbers, names, addresses, SSNs, etc.). Use when verifying PII protection, auditing security, or checking for data leaks in application logs.
tools: Bash, Grep, Read
---

# Log PII Scanner

Scan application log files for potential PII (Personally Identifiable Information) leaks. This skill searches logs for patterns that indicate sensitive data may have been logged improperly.

## Target Directories

- `~/Library/Logs` - macOS application logs
- `~/Library/Application Support/*/logs` - App-specific logs
- `~/.local/share/*/logs` - Linux application logs (if applicable)

## PII Patterns to Detect

### High Severity (Always a Problem)
| Pattern | Description | Regex |
|---------|-------------|-------|
| SSN | Social Security Numbers | `\d{3}-\d{2}-\d{4}` |
| Credit Card | Card numbers (13-19 digits) | `\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{1,7}` |
| Full Email | Email addresses in content | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` |

### Medium Severity (Context Dependent)
| Pattern | Description | Regex |
|---------|-------------|-------|
| Phone | US phone numbers | `\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}` |
| Account Number | Long numeric IDs (8-16 digits) | `(?<![0-9-])\d{10,16}(?![0-9])` |
| IP Address | IPv4 addresses | `(?:\d{1,3}\.){3}\d{1,3}` |
| Street Address | Address patterns | `\d+\s+[A-Za-z]+\s+(Street|St|Avenue|Ave|Blvd|Drive|Dr|Road|Rd|Lane|Ln)` |

### Low Severity (Check Context)
| Pattern | Description | Regex |
|---------|-------------|-------|
| Named Person | Names after context words | `(Welcome|Hello|Hi|Dear|Customer:)\s+[A-Z][a-z]+` |
| ZIP Code | 5 or 9 digit ZIP | `\b\d{5}(-\d{4})?\b` |

## Workflow

### Step 1: Identify Log Files

```bash
# Find all log files in Library/Logs
find ~/Library/Logs -name "*.log" -type f -mtime -30 2>/dev/null | head -50

# Check specific app logs (e.g., utility-bill-manager)
ls -la ~/Library/Logs/utility-bill-manager/ 2>/dev/null
```

### Step 2: Scan for High-Severity PII

**SSN Pattern:**
```bash
grep -rEn '\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b' ~/Library/Logs/ 2>/dev/null | head -20
```

**Credit Card Pattern:**
```bash
grep -rEn '\b[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{1,7}\b' ~/Library/Logs/ 2>/dev/null | head -20
```

**Email Pattern (excluding common placeholders):**
```bash
grep -rEn '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' ~/Library/Logs/ 2>/dev/null | grep -v 'example\.com\|@test\.\|noreply@\|no-reply@' | head -30
```

### Step 3: Scan for Account Numbers

**Long numeric sequences (potential account numbers):**
```bash
grep -rEn '([^0-9-]|^)[0-9]{10,16}([^0-9]|$)' ~/Library/Logs/ 2>/dev/null | grep -v 'timestamp\|bytes\|ms$\|Z$' | head -30
```

**Account numbers after redaction markers (indicates incomplete sanitization):**
```bash
grep -rEn '\[.*REDACTED.*\]-[0-9]{6,}' ~/Library/Logs/ 2>/dev/null | head -20
```

### Step 4: Scan for Personal Information

**Phone numbers:**
```bash
grep -rEn '\(?\b[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b' ~/Library/Logs/ 2>/dev/null | head -20
```

**Street addresses:**
```bash
grep -rEin '\b[0-9]+\s+[a-z]+\s+(street|st|avenue|ave|boulevard|blvd|drive|dr|road|rd|lane|ln|way|court|ct)\b' ~/Library/Logs/ 2>/dev/null | head -20
```

**Named greetings (may contain customer names):**
```bash
grep -rEin '(welcome|hello|hi|dear),?\s+[A-Z][a-z]+' ~/Library/Logs/ 2>/dev/null | grep -v 'REDACTED' | head -20
```

### Step 5: Check for Partially Redacted Data

Look for patterns where redaction was applied but data leaked:

```bash
# Account numbers following redaction markers
grep -rEn '\[ACCOUNT-REDACTED\].*[0-9]{8,}' ~/Library/Logs/ 2>/dev/null

# Names following redaction
grep -rEn '\[NAME-REDACTED\].*[A-Z][a-z]+\s+[A-Z][a-z]+' ~/Library/Logs/ 2>/dev/null

# Any long numbers after any redaction marker
grep -rEn '\[[A-Z-]+REDACTED\][^0-9]*[0-9]{8,}' ~/Library/Logs/ 2>/dev/null
```

## Output Format

Report findings in this format:

```markdown
## PII Scan Results

### Summary
- **Files Scanned**: X
- **High Severity Findings**: X
- **Medium Severity Findings**: X
- **Low Severity Findings**: X

### High Severity Findings

#### SSN Detected
- **File**: `/path/to/file.log`
- **Line**: 123
- **Sample**: `...context [SSN-PATTERN] context...`

#### Credit Card Detected
...

### Medium Severity Findings

#### Account Number Leaked
- **File**: `/path/to/file.log`
- **Line**: 456
- **Pattern**: Long numeric ID after redaction marker
- **Sample**: `[ACCOUNT-REDACTED]-12345678901`

### Recommendations

1. Update PII sanitizer patterns to catch [specific pattern]
2. Add pre-logging sanitization for [component]
3. Review and rotate any exposed credentials
```

## Integration with Security Audits

This skill should be invoked by security audit agents (like `security-fortress`) as part of comprehensive security reviews. The scan results help identify:

1. **Sanitization gaps** - Where PII patterns slip through
2. **New PII types** - Patterns not covered by current rules
3. **Compliance risks** - Data that shouldn't be logged at all
4. **Incident response** - What data may have been exposed

## Best Practices

1. **Run regularly** - Include in CI/CD or scheduled audits
2. **Check after changes** - Scan logs after modifying logging code
3. **Verify fixes** - After updating sanitization, run scan to confirm
4. **Retention awareness** - Old logs may contain PII from before protections were added
