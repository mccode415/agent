---
name: discord-logs
description: Query Discord channel logs from cb-auto-buy service. Use this skill when debugging production issues, checking recent errors, finding purchase history, or investigating service behavior. Retrieves logs without needing SSH access.
tools: Bash, Read
---

# Discord Logs Query

Query application logs posted to Discord by the cb-auto-buy service. Use this when:
- Debugging production issues
- Checking for recent errors
- Finding purchase/trade history
- Investigating dip buyer or ETF strategy behavior
- Verifying service is running correctly

## Prerequisites

The `logquery` tool must be built in the cb-auto-buy repository:
```bash
cd /Users/mcai/src/cb-auto-buy
go build -o logquery ./cmd/logquery
```

Credentials are auto-retrieved from OCI Vault.

## Common Commands

### Check Recent Logs
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 20
```

### Search for Errors
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "error"
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "fail"
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "ERROR"
```

### View Purchase Notifications Only
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 50 -embeds
```

### View Application Logs Only (No Notifications)
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 50 -logs
```

### Search for Specific Topics
```bash
# ETF strategy
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "ETF"

# Dip buyer
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "DipBuyer"

# Price feed
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "PRICE"

# Specific coin
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "BTC"
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "XRP"
```

### Raw JSON Output (for parsing)
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 50 -raw | jq .
```

## CLI Flags Reference

| Flag | Default | Description |
|------|---------|-------------|
| `-n` | 20 | Number of messages (max 100) |
| `-before` | "" | Pagination: fetch before message ID |
| `-grep` | "" | Filter by text (case-insensitive) |
| `-raw` | false | Output raw JSON |
| `-embeds` | false | Only show notifications (purchases, errors) |
| `-logs` | false | Only show log code blocks |
| `-no-color` | false | Disable colored output |
| `-v` | false | Verbose mode |

## Workflow for Debugging

### Step 1: Check for Recent Errors
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "error" 2>&1
```

### Step 2: If No Errors, Check Recent Activity
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 50 2>&1
```

### Step 3: Check Specific Strategy
```bash
# For ETF issues
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "ETF" 2>&1

# For Dip Buyer issues
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 100 -grep "DipBuyer" 2>&1
```

### Step 4: Check Recent Purchases
```bash
cd /Users/mcai/src/cb-auto-buy && go run ./cmd/logquery/ -n 20 -embeds 2>&1
```

## Troubleshooting the Tool Itself

If logquery fails:
1. **"bot token not found"** - OCI CLI not configured, run: `oci setup config`
2. **"forbidden"** - Bot needs MESSAGE_CONTENT intent in Discord Developer Portal
3. **"not found"** - Wrong channel ID or bot not in server

## Message Types

### Log Messages (code blocks)
Application log output wrapped in markdown code blocks:
```
[2026-01-25 10:00:00] LOG
  2026/01/25 10:00:00 [ETF] Starting weekly buy...
  2026/01/25 10:00:01 [ETF] Found 10 tradable coins
```

### Embed Messages (notifications)
Rich notifications for important events:
```
[2026-01-25 10:30:00] [SUCCESS] BTC Purchase Complete
  Strategy: ETF
  Amount: $10.00 = 0.00010234 BTC
  Price: $97,650.00
```

## Related Documentation

- `/Users/mcai/src/cb-auto-buy/LOG_QUERY_SETUP.md` - Discord bot setup
- `/Users/mcai/src/cb-auto-buy/CLAUDE.md` - Project documentation
