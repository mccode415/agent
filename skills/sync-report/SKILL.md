---
name: sync-report
description: Generate diagnostic HTML reports from utility-bill-manager sync logs. Analyzes logs for errors, identifies root causes, and creates a visual report in a temp directory. Use when debugging failed syncs, understanding why 0 bills were downloaded, or reviewing navigator behavior.
tools: Bash, Read, Write, Grep
---

# Sync Report Generator

Generate visual HTML diagnostic reports from utility-bill-manager sync logs. Reports are created in a temp directory (not in the repo) and automatically opened in the browser.

## Usage

Invoke this skill with:
- A log file path: `/sync-report /path/to/sync.log`
- Or paste the log content directly after invoking

## What It Analyzes

### Error Categories

| Category | Patterns | Severity |
|----------|----------|----------|
| VectorDB | `sqlite-vec search failed`, `SqliteError` | High |
| LLM Failures | `LLM failed`, `No high-confidence memory match` | Medium |
| Selector Issues | `not found on page`, `Invalid selector`, `SyntaxError` | High |
| Element Issues | `detached from DOM`, `Element detached` | Medium |
| PDF Download | `Could not extract PDF`, `blob extraction failed` | High |
| Navigation | `FAILED:`, `action_failed` | Medium |
| Timeout | `exceeded timeout`, `timed out` | Medium |

### Metrics Extracted

- Total navigation steps
- Successful vs failed actions
- Bills found (from HTML extraction)
- Bills downloaded (actual PDFs)
- LLM call count and failure rate
- VectorDB query errors
- Popup tracking stats

## Workflow

### Step 1: Locate the Log

If user provides a file path, read it. Otherwise, check recent logs:

```bash
# Find recent utility-bill-manager logs
ls -lt ~/Library/Logs/utility-bill-manager/*.log 2>/dev/null | head -5

# Or check Electron dev logs
ls -lt /tmp/utility-bill-manager*.log 2>/dev/null | head -5
```

### Step 2: Extract Key Events

Parse the log for important events:

```bash
# Count errors by type
grep -c "ERROR\|FAILED\|failed" "$LOG_FILE"

# Find VectorDB issues
grep "VectorDB.*failed\|SqliteError" "$LOG_FILE"

# Find selector failures
grep "not found on page\|SyntaxError" "$LOG_FILE"

# Find LLM status
grep "LLM failed\|LLM.*trying" "$LOG_FILE"

# Find download results
grep "bills downloaded\|PDF.*captured\|PDF.*extracted" "$LOG_FILE"

# Find bill amounts from HTML
grep "HTML-EXTRACT" "$LOG_FILE"
```

### Step 3: Generate the HTML Report

Create the report in the scratchpad directory (session-specific temp):

```bash
# Get the scratchpad directory from environment or use fallback
SCRATCHPAD="${CLAUDE_SCRATCHPAD:-/tmp/claude-sync-reports}"
mkdir -p "$SCRATCHPAD"

# Generate unique filename
REPORT_FILE="$SCRATCHPAD/sync-report-$(date +%Y%m%d-%H%M%S).html"
```

### Step 4: Report Structure

The HTML report should include:

1. **Summary Card**
   - Sync result (success/failure)
   - Bills found vs downloaded
   - Total steps / errors
   - Duration

2. **Failure Cascade Flow**
   - Visual diagram showing how errors propagated
   - Arrow-connected boxes for each stage

3. **Root Causes**
   - Card for each identified issue
   - Status badge (fixed/unfixed/mitigated)
   - Code snippets from log
   - Impact description

4. **Event Timeline**
   - Chronological list of important events
   - Color-coded by severity
   - Timestamps and log excerpts

5. **Recommendations**
   - Actionable next steps
   - Priority levels

### Step 5: Open the Report

```bash
# macOS
open "$REPORT_FILE"

# Linux
xdg-open "$REPORT_FILE" 2>/dev/null || echo "Report saved to: $REPORT_FILE"
```

## HTML Template

Use this template structure for the report:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sync Diagnostic Report</title>
  <style>
    :root {
      --bg: #0f1419;
      --card-bg: #1a1f2e;
      --accent: #3b82f6;
      --success: #10b981;
      --warning: #f59e0b;
      --error: #ef4444;
      --text: #e5e7eb;
      --text-muted: #9ca3af;
      --border: #374151;
    }
    body {
      font-family: 'SF Mono', 'Fira Code', monospace;
      background: var(--bg);
      color: var(--text);
      padding: 2rem;
      line-height: 1.6;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    .card {
      background: var(--card-bg);
      border-radius: 8px;
      padding: 1.5rem;
      margin: 1rem 0;
      border: 1px solid var(--border);
    }
    .status-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .status-error { background: rgba(239, 68, 68, 0.2); color: var(--error); }
    .status-success { background: rgba(16, 185, 129, 0.2); color: var(--success); }
    .status-warning { background: rgba(245, 158, 11, 0.2); color: var(--warning); }
    h1 { color: var(--accent); }
    h2 { border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
    pre {
      background: #0d1117;
      padding: 1rem;
      border-radius: 6px;
      overflow-x: auto;
      font-size: 0.8rem;
    }
    .timeline {
      position: relative;
      padding-left: 2rem;
    }
    .timeline::before {
      content: '';
      position: absolute;
      left: 0.5rem;
      top: 0;
      bottom: 0;
      width: 2px;
      background: var(--border);
    }
    .timeline-item {
      position: relative;
      padding: 0.75rem 0;
    }
    .timeline-item::before {
      content: '';
      position: absolute;
      left: -1.65rem;
      top: 1rem;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--border);
    }
    .timeline-item.error::before { background: var(--error); }
    .timeline-item.success::before { background: var(--success); }
    .flow-diagram {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      align-items: center;
    }
    .flow-step {
      background: var(--card-bg);
      padding: 0.5rem 1rem;
      border-radius: 4px;
      font-size: 0.85rem;
      border: 1px solid var(--border);
    }
    .flow-step.error { border-color: var(--error); color: var(--error); }
    .flow-step.success { border-color: var(--success); color: var(--success); }
    .flow-arrow { color: var(--text-muted); }
  </style>
</head>
<body>
  <div class="container">
    <h1>Sync Diagnostic Report</h1>
    <p style="color: var(--text-muted);">Generated: [TIMESTAMP] | Profile: [PROFILE]</p>

    <!-- Summary -->
    <div class="card">
      <h3>Result: <span class="status-badge status-[STATUS]">[RESULT]</span></h3>
      <p>Steps: [STEPS] | Errors: [ERRORS] | Bills: [DOWNLOADED]/[FOUND]</p>
    </div>

    <!-- Flow Diagram -->
    <h2>Failure Cascade</h2>
    <div class="card">
      <div class="flow-diagram">
        [FLOW_STEPS]
      </div>
    </div>

    <!-- Issues -->
    <h2>Issues Identified</h2>
    [ISSUE_CARDS]

    <!-- Timeline -->
    <h2>Event Timeline</h2>
    <div class="card">
      <div class="timeline">
        [TIMELINE_ITEMS]
      </div>
    </div>

    <!-- Recommendations -->
    <h2>Recommendations</h2>
    <div class="card">
      [RECOMMENDATIONS]
    </div>
  </div>
</body>
</html>
```

## Issue Detection Patterns

### VectorDB Error
```
Pattern: "sqlite-vec search failed" OR "SqliteError"
Root Cause: LIMIT and k=? conflict in query
Impact: Navigation memory disabled, forces LLM fallback
```

### Invalid CSS Selector
```
Pattern: "SyntaxError" + "querySelectorAll" + ":has-text"
Root Cause: Playwright selector used with native DOM API
Impact: Retry logic fails completely
```

### Blob Extraction Failure
```
Pattern: "Could not extract PDF content from blob"
Root Cause: Cross-origin restriction on blob URL
Impact: PDF viewer opens but content not captured
```

### Element Detachment
```
Pattern: "detached from DOM" OR "Element detached"
Root Cause: SPA navigation changes DOM during click
Impact: Click succeeds but follow-up actions fail
```

### LLM Exhaustion
```
Pattern: "LLM failed Xx" followed by "hardcoded fallback"
Root Cause: Vision model couldn't identify correct element
Impact: Falls back to potentially stale selectors
```

## Example Output

After running, report the location:

```
Sync diagnostic report generated:
  /tmp/claude-sync-reports/sync-report-20260204-063126.html

Opening in browser...
```

## Related Files

- `/Users/mcai/src/util/utility-bill-manager/electron/main/services/intelligent-navigator.ts` - Main navigation
- `/Users/mcai/src/util/utility-bill-manager/electron/main/services/vector-db.ts` - Navigation memory
- `/Users/mcai/src/util/utility-bill-manager/electron/main/services/browser-agent.ts` - PDF handling
