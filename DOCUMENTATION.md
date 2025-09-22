# 📚 OpenCode Monitor - Complete Documentation

Welcome to the complete documentation for OpenCode Monitor, a powerful CLI tool for monitoring and analyzing your OpenCode AI coding sessions.

> **📸 Screenshots**: Throughout this documentation, you'll find clickable screenshot references that show actual command outputs. These screenshots are located in the `screenshots/` directory. To add your own screenshots, replace the placeholder PNG files with actual screenshots of your terminal output.

## 📖 Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Command Reference](#command-reference)
4. [Configuration](#configuration)
5. [Adding New Models](#adding-new-models)
6. [Setting Usage Quotas](#setting-usage-quotas)
7. [Exporting Reports](#exporting-reports)
8. [Configuration Commands](#configuration-commands)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Tips](#advanced-tips)

---

## 🚀 Installation

### Prerequisites

Before installing OpenCode Monitor, ensure you have:
- **Python 3.7+** installed on your system
- **pip** package manager
- **OpenCode AI** installed and configured

### Method 1: Automated Installation (Recommended)

The easiest way to install OpenCode Monitor:

```bash
# Clone the repository
git clone https://github.com/yourusername/ocmonitor.git
cd ocmonitor

# Run the automated installer
./install.sh
```

The installer will:
- ✅ Check Python version compatibility
- ✅ Install all required dependencies
- ✅ Configure PATH settings automatically
- ✅ Verify the installation

### Method 2: Manual Installation

For more control over the installation process:

```bash
# Clone the repository
git clone https://github.com/yourusername/ocmonitor.git
cd ocmonitor

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Install the package in development mode
python3 -m pip install -e .
```

### Verify Installation

After installation, verify everything works:

```bash
# Check if ocmonitor is accessible
ocmonitor --help

# Test with sample data
ocmonitor sessions test_sessions/
```

### PATH Configuration (If Needed)

If you get "command not found" errors:

```bash
# Find your Python user base
python3 -m site --user-base

# Add to your shell profile (~/.bashrc or ~/.zshrc)
export PATH="$(python3 -m site --user-base)/bin:$PATH"

# Reload your shell
source ~/.bashrc  # or ~/.zshrc
```

---

## 🎯 Basic Usage

### Quick Start Example

```bash
# Show current configuration
ocmonitor config show

# Analyze all your sessions
ocmonitor sessions ~/.local/share/opencode/storage/message

# Get a weekly breakdown
ocmonitor weekly ~/.local/share/opencode/storage/message

# Start live monitoring
ocmonitor live ~/.local/share/opencode/storage/message
```

### Default OpenCode Message Location

By default, OpenCode stores messages at:
```
~/.local/share/opencode/storage/message
```

You can use this path in all commands, or configure a custom path (see [Configuration](#configuration) section).

---

## 📋 Command Reference

### 1. Session Analysis Commands

#### `ocmonitor session <path>`
Analyze a single coding session in detail.

```bash
# Analyze a specific session directory
ocmonitor session ~/.local/share/opencode/storage/message/ses_20250118_143022

# With JSON output
ocmonitor session ~/.local/share/opencode/storage/message/ses_20250118_143022 --format json
```

**Example Output:**

[![Session Analysis Screenshot](screenshots/session-analysis.png)](screenshots/session-analysis.png)

*Click image to view full-size screenshot of session analysis output*


```

#### `ocmonitor sessions <path>`
Analyze all sessions in a directory with summary statistics.

```bash
# Analyze all sessions
ocmonitor sessions ~/.local/share/opencode/storage/message

# Limit to recent sessions
ocmonitor sessions ~/.local/share/opencode/storage/message --limit 10

# JSON format for programmatic use
ocmonitor sessions ~/.local/share/opencode/storage/message --format json
```

**Example Output:**

[![Sessions Summary Screenshot](screenshots/sessions-summary.png)](screenshots/sessions-summary.png)

*Click image to view full-size screenshot of sessions summary output*

```

### 2. Time-Based Analysis Commands

#### `ocmonitor daily <path>`
Daily usage breakdown with cost and token analysis.

```bash
# Daily breakdown for the last 30 days
ocmonitor daily ~/.local/share/opencode/storage/message

# Specific date range
ocmonitor daily ~/.local/share/opencode/storage/message --days 7

# JSON output
ocmonitor daily ~/.local/share/opencode/storage/message --format json
```

**Example Output:**

[![Daily Usage Breakdown Screenshot](screenshots/daily-usage-breakdown.png)](screenshots/daily-usage-breakdown.png)

*Click image to view full-size screenshot of daily usage breakdown*

```

#### `ocmonitor weekly <path>`
Weekly usage patterns and trends.

```bash
# Weekly breakdown
ocmonitor weekly ~/.local/share/opencode/storage/message

# Last 4 weeks
ocmonitor weekly ~/.local/share/opencode/storage/message --weeks 4
```

#### `ocmonitor monthly <path>`
Monthly usage analysis and cost tracking.

```bash
# Monthly breakdown
ocmonitor monthly ~/.local/share/opencode/storage/message

# Specific number of months
ocmonitor monthly ~/.local/share/opencode/storage/message --months 6
```

### 3. Model Analysis Commands

#### `ocmonitor models <path>`
Detailed breakdown of usage per AI model.

```bash
# Model usage statistics
ocmonitor models ~/.local/share/opencode/storage/message

# JSON format
ocmonitor models ~/.local/share/opencode/storage/message --format json
```

**Example Output:**

[![Model Usage Analysis Screenshot](screenshots/model-usage-analysis.png)](screenshots/model-usage-analysis.png)

*Click image to view full-size screenshot of model usage analytics*



### 4. Live Monitoring Commands

#### `ocmonitor live <path>`
Real-time monitoring dashboard that updates automatically.

```bash
# Start live monitoring (updates every 5 seconds)
ocmonitor live ~/.local/share/opencode/storage/message

# Custom refresh interval (in seconds)
ocmonitor live ~/.local/share/opencode/storage/message --refresh 10
```

**Features:**
- 🔄 Auto-refreshing display
- 📊 Real-time cost tracking
- ⏱️ Live session duration
- 📈 Token usage updates
- 🚦 Color-coded status indicators

[![Live Dashboard Screenshot](screenshots/live_dashboard.png)](screenshots/live_dashboard.png)

*Click image to view full-size screenshot of the live monitoring dashboard*

---

## ⚙️ Configuration

### Setting Custom Message Path

OpenCode Monitor can be configured to use custom paths for your message data.

#### Method 1: Edit Configuration File

Edit the `config.toml` file:

```toml
[paths]
# Custom path to OpenCode messages directory
messages_dir = "/custom/path/to/messages"
# Directory for exports
export_dir = "./my-exports"
```

#### Method 2: Environment Variable

Set the path via environment variable:

```bash
# Set custom path
export OCMONITOR_MESSAGES_DIR="/custom/path/to/messages"

# Use in commands
ocmonitor sessions
```

#### Method 3: Command Line Override

Override the path for individual commands:

```bash
# Use custom path for this command only
ocmonitor sessions /custom/path/to/messages
```

### Full Configuration Options

Here's a complete `config.toml` with all available options:

```toml
# OpenCode Monitor Configuration

[paths]
# Default path to OpenCode messages directory
messages_dir = "~/.local/share/opencode/storage/message"
# Directory for exports
export_dir = "./exports"

[ui]
# Table style: "rich", "simple", "minimal"
table_style = "rich"
# Enable progress bars
progress_bars = true
# Enable colors in output
colors = true
# Refresh interval for live dashboard (seconds)
live_refresh_interval = 5

[export]
# Default export format: "csv", "json"
default_format = "csv"
# Include metadata in exports
include_metadata = true
# Include raw data in exports
include_raw_data = false

[models]
# Path to models pricing configuration
config_file = "models.json"

[analytics]
# Default timeframe for reports: "daily", "weekly", "monthly"
default_timeframe = "daily"
# Number of recent sessions to analyze by default
recent_sessions_limit = 50

[quotas]
# Daily spending limits per model (in USD)
daily_limits = { claude-sonnet-4 = 10.0, claude-opus-4 = 20.0 }
# Monthly spending limits
monthly_limits = { claude-sonnet-4 = 200.0, claude-opus-4 = 400.0 }
# Enable quota warnings
enable_warnings = true
```

---

## 🤖 Adding New Models

### Understanding the Models Configuration

Models are defined in the `models.json` file. Each model includes pricing and technical specifications.

### Current Models Format

```json
{
  "claude-sonnet-4-20250514": {
    "input_cost_per_million": 3.0,
    "output_cost_per_million": 15.0,
    "context_window": 200000,
    "description": "Claude Sonnet 4 (2025-05-14)"
  },
  "claude-opus-4": {
    "input_cost_per_million": 15.0,
    "output_cost_per_million": 75.0,
    "context_window": 200000,
    "description": "Claude Opus 4"
  },
  "grok-code": {
    "input_cost_per_million": 0.0,
    "output_cost_per_million": 0.0,
    "context_window": 256000,
    "description": "Grok Code (Free)"
  }
}
```

### Adding a New Model

#### Step 1: Edit models.json

Add your new model to the `models.json` file:

```json
{
  "existing-models": "...",
  
  "new-ai-model": {
    "input_cost_per_million": 5.0,
    "output_cost_per_million": 25.0,
    "context_window": 128000,
    "description": "New AI Model"
  },
  
  "another-model": {
    "input_cost_per_million": 0.0,
    "output_cost_per_million": 0.0,
    "context_window": 100000,
    "description": "Another Free Model"
  }
}
```

#### Step 2: Verify the Addition

Test that your new model is recognized:

```bash
# Check if the model appears in configuration
ocmonitor config show

# Test with session data that uses the new model
ocmonitor sessions /path/to/sessions
```

#### Step 3: Handle Fully Qualified Names

For models with provider prefixes (like `provider/model-name`), add both versions:

```json
{
  "provider/model-name": {
    "input_cost_per_million": 2.0,
    "output_cost_per_million": 10.0,
    "context_window": 150000,
    "description": "Provider Model"
  },
  "model-name": {
    "input_cost_per_million": 2.0,
    "output_cost_per_million": 10.0,
    "context_window": 150000,
    "description": "Provider Model (short name)"
  }
}
```

### Model Configuration Fields

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| `input_cost_per_million` | Cost per 1M input tokens (USD) | ✅ | `3.0` |
| `output_cost_per_million` | Cost per 1M output tokens (USD) | ✅ | `15.0` |
| `context_window` | Maximum context window size | ✅ | `200000` |
| `description` | Human-readable model name | ✅ | `"Claude Sonnet 4"` |

### Free Models

For free models, set costs to `0.0`:

```json
{
  "free-model": {
    "input_cost_per_million": 0.0,
    "output_cost_per_million": 0.0,
    "context_window": 100000,
    "description": "Free AI Model"
  }
}
```

---

## 💰 Setting Usage Quotas

### Understanding Quotas

Quotas help you monitor and control your AI usage costs by setting spending limits.

### Configuring Quotas

#### Method 1: Configuration File

Edit `config.toml` to set quota limits:

```toml
[quotas]
# Daily spending limits per model (in USD)
daily_limits = { 
    claude-sonnet-4 = 10.0, 
    claude-opus-4 = 20.0,
    claude-opus-4.1 = 25.0
}

# Weekly spending limits
weekly_limits = { 
    claude-sonnet-4 = 50.0, 
    claude-opus-4 = 100.0 
}

# Monthly spending limits
monthly_limits = { 
    claude-sonnet-4 = 200.0, 
    claude-opus-4 = 400.0,
    "*" = 500.0  # Total limit across all models
}

# Enable quota warnings
enable_warnings = true

# Warning threshold (percentage of quota)
warning_threshold = 80.0

# Action when quota exceeded: "warn", "block"
quota_action = "warn"
```

#### Method 2: Environment Variables

Set quotas using environment variables:

```bash
# Daily limits
export OCMONITOR_DAILY_CLAUDE_SONNET_4=10.0
export OCMONITOR_DAILY_CLAUDE_OPUS_4=20.0

# Monthly limits
export OCMONITOR_MONTHLY_TOTAL=500.0
```

### Quota Examples

#### Basic Daily Limits

```toml
[quotas]
daily_limits = { 
    claude-sonnet-4 = 15.0,  # $15/day for Sonnet
    claude-opus-4 = 30.0     # $30/day for Opus
}
enable_warnings = true
```

#### Comprehensive Quota Setup

```toml
[quotas]
# Daily limits per model
daily_limits = { 
    claude-sonnet-4 = 10.0,
    claude-opus-4 = 20.0,
    "*" = 35.0  # Total daily limit
}

# Weekly limits
weekly_limits = { 
    claude-sonnet-4 = 60.0,
    claude-opus-4 = 120.0,
    "*" = 200.0
}

# Monthly limits
monthly_limits = { 
    claude-sonnet-4 = 250.0,
    claude-opus-4 = 500.0,
    "*" = 800.0
}

# Warning settings
enable_warnings = true
warning_threshold = 75.0  # Warn at 75% of quota
email_notifications = "admin@example.com"
```

### Viewing Quota Status

Check your current quota usage:

```bash
# Show quota status in daily report
ocmonitor daily ~/.local/share/opencode/storage/message --show-quotas

# Show quota status in model breakdown
ocmonitor models ~/.local/share/opencode/storage/message --show-quotas
```


---

## 📤 Exporting Reports

### Export Command Overview

OpenCode Monitor provides powerful export capabilities for creating reports and integrating with other tools.

### Basic Export Syntax

```bash
ocmonitor export <report_type> [path] [options]
```

### Export Types

#### 1. Sessions Export

Export detailed session data:

```bash
# Export all sessions to CSV
ocmonitor export sessions ~/.local/share/opencode/storage/message --format csv --output sessions_report.csv

# Export to JSON
ocmonitor export sessions ~/.local/share/opencode/storage/message --format json --output sessions_data.json

# Export recent sessions only
ocmonitor export sessions ~/.local/share/opencode/storage/message --limit 50 --format csv
```

#### 2. Daily Reports Export

```bash
# Export daily breakdown
ocmonitor export daily ~/.local/share/opencode/storage/message --format csv --output daily_usage.csv

# Last 30 days
ocmonitor export daily ~/.local/share/opencode/storage/message --days 30 --format json
```

#### 3. Weekly Reports Export

```bash
# Export weekly data
ocmonitor export weekly ~/.local/share/opencode/storage/message --format csv --output weekly_report.csv

# Last 12 weeks
ocmonitor export weekly ~/.local/share/opencode/storage/message --weeks 12 --format json
```

#### 4. Monthly Reports Export

```bash
# Export monthly analysis
ocmonitor export monthly ~/.local/share/opencode/storage/message --format csv --output monthly_analysis.csv

# Last 6 months
ocmonitor export monthly ~/.local/share/opencode/storage/message --months 6 --format json
```

#### 5. Model Usage Export

```bash
# Export model breakdown
ocmonitor export models ~/.local/share/opencode/storage/message --format csv --output model_usage.csv

# JSON format with metadata
ocmonitor export models ~/.local/share/opencode/storage/message --format json --include-metadata
```

### Export Options

| Option | Description | Example |
|--------|-------------|---------|
| `--format` | Output format (`csv`, `json`) | `--format csv` |
| `--output` | Output filename | `--output report.csv` |
| `--limit` | Limit number of records | `--limit 100` |
| `--days` | Number of days to include | `--days 30` |
| `--weeks` | Number of weeks to include | `--weeks 12` |
| `--months` | Number of months to include | `--months 6` |
| `--include-metadata` | Include additional metadata | `--include-metadata` |
| `--include-raw-data` | Include raw session data | `--include-raw-data` |

### CSV Export Example

```bash
ocmonitor export sessions ~/.local/share/opencode/storage/message --format csv --output sessions.csv
```

**Generated CSV Structure:**
```csv
session_id,date,start_time,end_time,duration_minutes,model,total_cost,input_tokens,output_tokens,cache_tokens
ses_20250118_143022,2025-01-18,14:30:22,14:53:37,23.25,claude-sonnet-4,2.45,15420,8340,2100
ses_20250118_120830,2025-01-18,12:08:30,12:53:38,45.13,claude-opus-4,4.32,18650,9240,1850
```

### JSON Export Example

```bash
ocmonitor export sessions ~/.local/share/opencode/storage/message --format json --output sessions.json --include-metadata
```

**Generated JSON Structure:**
```json
{
  "metadata": {
    "export_date": "2025-01-18T15:30:00Z",
    "tool_version": "1.0.0",
    "total_sessions": 25,
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-01-18"
    }
  },
  "sessions": [
    {
      "session_id": "ses_20250118_143022",
      "date": "2025-01-18",
      "start_time": "14:30:22",
      "end_time": "14:53:37",
      "duration_minutes": 23.25,
      "model": "claude-sonnet-4",
      "total_cost": 2.45,
      "tokens": {
        "input": 15420,
        "output": 8340,
        "cache": 2100,
        "total": 25860
      },
      "cost_breakdown": {
        "input_cost": 0.46,
        "output_cost": 1.25,
        "cache_cost": 0.63,
        "total_cost": 2.45
      }
    }
  ]
}
```

### Automated Export Scripts

#### Daily Export Automation

Create a script for daily exports:

```bash
#!/bin/bash
# daily_export.sh

DATE=$(date +%Y%m%d)
EXPORT_DIR="./reports"
MESSAGES_PATH="~/.local/share/opencode/storage/message"

mkdir -p $EXPORT_DIR

# Export daily report
ocmonitor export daily $MESSAGES_PATH \
  --format csv \
  --output "$EXPORT_DIR/daily_${DATE}.csv"

# Export sessions
ocmonitor export sessions $MESSAGES_PATH \
  --format json \
  --output "$EXPORT_DIR/sessions_${DATE}.json" \
  --include-metadata

echo "Reports exported to $EXPORT_DIR/"
```

#### Weekly Report Generation

```bash
#!/bin/bash
# weekly_report.sh

WEEK=$(date +%Y_W%U)
ocmonitor export weekly ~/.local/share/opencode/storage/message \
  --format csv \
  --output "weekly_report_${WEEK}.csv" \
  --weeks 1

ocmonitor export models ~/.local/share/opencode/storage/message \
  --format csv \
  --output "model_usage_${WEEK}.csv"
```

---

## 🔧 Configuration Commands

### `ocmonitor config` Command Reference

The configuration command helps you manage and view your OpenCode Monitor settings.

### Viewing Configuration

#### Show All Configuration

```bash
# Display complete configuration
ocmonitor config show
```


**Text Output Example:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                     ⚙️  Configuration                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📁 Paths:
   Messages Directory: ~/.local/share/opencode/storage/message
   Export Directory: ./exports

🎨 UI Settings:
   Table Style: rich
   Progress Bars: enabled
   Colors: enabled
   Live Refresh: 5 seconds

📤 Export Settings:
   Default Format: csv
   Include Metadata: enabled
   Include Raw Data: disabled

🤖 Models:
   Configuration File: models.json
   Supported Models: 6

📊 Analytics:
   Default Timeframe: daily
   Recent Sessions Limit: 50
```

#### Show Specific Configuration Sections

```bash
# Show only paths configuration
ocmonitor config show --section paths

# Show UI settings
ocmonitor config show --section ui

# Show model configuration
ocmonitor config show --section models
```

### Validating Configuration

#### Check Configuration Validity

```bash
# Validate configuration files
ocmonitor config validate
```

**Example Output:**


**Text Output Example:**
```
✅ Configuration validation successful

📋 Validation Results:
   ✅ config.toml: Valid TOML format
   ✅ models.json: Valid JSON format
   ✅ Paths: All directories accessible
   ✅ Models: 6 models configured correctly
   ✅ Quotas: Quota limits properly formatted

🔍 Configuration Details:
   Config File: /path/to/config.toml
   Models File: /path/to/models.json
   Messages Directory: ~/.local/share/opencode/storage/message (exists)
   Export Directory: ./exports (will be created)
```

#### Diagnose Configuration Issues

```bash
# Comprehensive configuration diagnosis
ocmonitor config diagnose
```

**Example Output:**


**Text Output Example:**
```
🔍 Configuration Diagnosis

✅ Configuration Files:
   ✅ config.toml found and valid
   ✅ models.json found and valid

⚠️  Path Issues:
   ⚠️  Messages directory not found: ~/.local/share/opencode/storage/message
   💡 Suggestion: Check if OpenCode is installed and has been run

✅ Model Configuration:
   ✅ 6 models configured
   ✅ All required fields present
   ✅ Valid pricing data

🔧 Recommendations:
   1. Verify OpenCode installation
   2. Run OpenCode at least once to create message directory
   3. Consider setting custom messages_dir if using different location
```

### Updating Configuration

#### Set Configuration Values

```bash
# Set messages directory
ocmonitor config set paths.messages_dir "/custom/path/to/messages"

# Set default export format
ocmonitor config set export.default_format "json"

# Enable/disable UI features
ocmonitor config set ui.colors true
ocmonitor config set ui.progress_bars false

# Set live refresh interval
ocmonitor config set ui.live_refresh_interval 10
```

#### Reset Configuration

```bash
# Reset to default configuration
ocmonitor config reset

# Reset specific section
ocmonitor config reset --section ui

# Backup current config before reset
ocmonitor config reset --backup
```

### Configuration File Locations

#### Find Configuration Files

```bash
# Show configuration file paths
ocmonitor config paths
```

**Example Output:**
```
📁 Configuration File Locations:

Main Configuration:
   File: ./config.toml
   Status: ✅ Found

Models Configuration:
   File: ./models.json
   Status: ✅ Found

User Configuration (if exists):
   File: ~/.config/ocmonitor/config.toml
   Status: ❌ Not found

Environment Overrides:
   OCMONITOR_MESSAGES_DIR: not set
   OCMONITOR_EXPORT_DIR: not set
```

### Environment Variable Override

You can override any configuration setting using environment variables:

```bash
# Override messages directory
export OCMONITOR_MESSAGES_DIR="/custom/path"

# Override export format
export OCMONITOR_EXPORT_FORMAT="json"

# Override UI settings
export OCMONITOR_UI_COLORS="false"
export OCMONITOR_UI_TABLE_STYLE="simple"

# Use the overrides
ocmonitor config show
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Command Not Found: `ocmonitor`

**Problem:** Terminal shows `command not found: ocmonitor`

**Solutions:**

```bash
# Check if Python scripts directory is in PATH
echo $PATH | grep -o '[^:]*python[^:]*bin'

# Find Python user base
python3 -m site --user-base

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$(python3 -m site --user-base)/bin:$PATH"

# Reload shell
source ~/.bashrc  # or ~/.zshrc

# Alternative: Use full path
python3 /path/to/ocmonitor/run_ocmonitor.py --help

# Alternative: Reinstall in development mode
cd /path/to/ocmonitor
python3 -m pip install -e .
```

#### 2. Import Errors and Dependencies

**Problem:** Python import errors when running commands

**Solutions:**

```bash
# Check Python version
python3 --version  # Should be 3.7+

# Reinstall dependencies
python3 -m pip install -r requirements.txt --force-reinstall

# Check for missing dependencies
python3 -c "import click, rich, pydantic, toml; print('All dependencies OK')"

# Install specific missing package
python3 -m pip install click rich pydantic toml

# Clear Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

#### 3. Architecture Compatibility Issues

**Problem:** Architecture mismatch errors (arm64 vs x86_64)

**Solutions:**

```bash
# Check system architecture
uname -m

# For Apple Silicon Macs, use native Python
which python3
/opt/homebrew/bin/python3 --version

# Reinstall with correct architecture
python3 -m pip uninstall pydantic pydantic-core
python3 -m pip install pydantic pydantic-core --no-cache-dir

# Force reinstall all dependencies
python3 -m pip install -r requirements.txt --force-reinstall --no-cache-dir
```

#### 4. Messages Directory Not Found

**Problem:** `Messages directory not found` error

**Solutions:**

```bash
# Check if OpenCode is installed
which opencode

# Check default location
ls -la ~/.local/share/opencode/storage/message

# Find OpenCode data directory
find ~ -name "opencode" -type d 2>/dev/null

# Check OpenCode configuration
opencode config list 2>/dev/null | grep storage

# Set custom path if different location
ocmonitor config set paths.messages_dir "/actual/path/to/messages"

# Verify path is accessible
ocmonitor config validate
```

#### 5. JSON Parsing Errors

**Problem:** Errors when reading session files

**Solutions:**

```bash
# Check for corrupted session files
find ~/.local/share/opencode/storage/message -name "*.json" -exec python3 -m json.tool {} \; > /dev/null

# Find specific problematic files
find ~/.local/share/opencode/storage/message -name "*.json" -print0 | while IFS= read -r -d '' file; do
    python3 -m json.tool "$file" > /dev/null 2>&1 || echo "Invalid JSON: $file"
done

# Test with specific session
ocmonitor session ~/.local/share/opencode/storage/message/problematic_session

# Use verbose mode for debugging
ocmonitor sessions ~/.local/share/opencode/storage/message --verbose
```

#### 6. Permission Errors

**Problem:** Permission denied errors when accessing files

**Solutions:**

```bash
# Check file permissions
ls -la ~/.local/share/opencode/storage/message

# Fix permissions if needed
chmod -R 755 ~/.local/share/opencode/storage/message

# Check if export directory is writable
mkdir -p ./exports
touch ./exports/test.txt && rm ./exports/test.txt

# Use alternative export directory
ocmonitor config set export.export_dir "/tmp/ocmonitor-exports"
```

#### 7. Model Not Recognized

**Problem:** "Unknown model" in reports

**Solutions:**

```bash
# Check which models are configured
ocmonitor config show --section models

# View current models.json
cat models.json

# Find unrecognized model names in your data
grep -r "model.*:" ~/.local/share/opencode/storage/message | grep -v claude | grep -v grok | head -5

# Add missing model to models.json
# Edit models.json and add the new model configuration

# Validate models configuration
ocmonitor config validate
```

#### 8. Export Failures

**Problem:** Export commands fail or produce empty files

**Solutions:**

```bash
# Test export with verbose output
ocmonitor export sessions ~/.local/share/opencode/storage/message --format csv --output test.csv --verbose

# Check export directory permissions
ls -la ./exports

# Try different export format
ocmonitor export sessions ~/.local/share/opencode/storage/message --format json --output test.json

# Test with limited data
ocmonitor export sessions ~/.local/share/opencode/storage/message --limit 5 --format csv

# Check disk space
df -h .
```

### Debug Mode

#### Enable Verbose Logging

```bash
# Run any command with verbose output
ocmonitor sessions ~/.local/share/opencode/storage/message --verbose

# Set debug environment variable
export OCMONITOR_DEBUG=1
ocmonitor sessions ~/.local/share/opencode/storage/message
```

#### Check System Information

```bash
# Show system information for bug reports
ocmonitor config system-info
```


**Text Output Example:**
```
🔍 System Information for Bug Reports

Environment:
   OS: macOS 12.6
   Architecture: arm64
   Python Version: 3.9.16
   OpenCode Monitor Version: 1.0.0

Python Environment:
   Python Path: /opt/homebrew/bin/python3
   Site Packages: /opt/homebrew/lib/python3.9/site-packages
   User Base: /Users/username/Library/Python/3.9

Dependencies:
   ✅ click: 8.1.7
   ✅ rich: 13.7.0
   ✅ pydantic: 2.5.2
   ✅ toml: 0.10.2

Configuration:
   Config File: ./config.toml (exists)
   Models File: ./models.json (exists)
   Messages Dir: ~/.local/share/opencode/storage/message (accessible)

Recent Errors: None
```

### Getting Help

#### Report Issues

When reporting issues, include:

1. **System Information:**
   ```bash
   ocmonitor config system-info
   ```

2. **Error Messages:** Full error output with `--verbose` flag

3. **Configuration:**
   ```bash
   ocmonitor config show
   ```

4. **Steps to Reproduce:** Exact commands that cause the issue

#### Community Support

- 🐛 **GitHub Issues:** For bug reports and feature requests
- 💬 **Discussions:** For questions and community help
- 📚 **Documentation:** Check this guide and README files

---

## 🚀 Advanced Tips

### Performance Optimization

#### Large Dataset Handling

```bash
# Process large datasets efficiently
ocmonitor sessions ~/.local/share/opencode/storage/message --limit 1000

# Use JSON format for faster processing
ocmonitor sessions ~/.local/share/opencode/storage/message --format json | jq '.sessions | length'

# Focus on recent data
ocmonitor daily ~/.local/share/opencode/storage/message --days 7
```

#### Batch Processing

```bash
# Process multiple directories
for dir in /path/to/project1/messages /path/to/project2/messages; do
    echo "Processing $dir"
    ocmonitor sessions "$dir" --format csv --output "$(basename $dir)_report.csv"
done
```

### Integration with Other Tools

#### Shell Scripts Integration

```bash
#!/bin/bash
# Monthly cost check script

COST=$(ocmonitor monthly ~/.local/share/opencode/storage/message --format json | jq '.summary.total_cost')
LIMIT=100.0

if (( $(echo "$COST > $LIMIT" | bc -l) )); then
    echo "⚠️ Monthly cost $COST exceeds limit $LIMIT"
    # Send notification, email, etc.
fi
```

#### Data Pipeline Integration

```bash
# Export for data analysis
ocmonitor export sessions ~/.local/share/opencode/storage/message \
    --format json \
    --include-raw-data \
    --output sessions.json

# Process with jq
cat sessions.json | jq '.sessions[] | select(.total_cost > 5.0)'

# Import into database (example)
python3 scripts/import_to_db.py sessions.json
```

### Customization

#### Custom Export Scripts

Create custom export formats:

```python
#!/usr/bin/env python3
# custom_export.py

import json
import sys
from datetime import datetime

def custom_export(sessions_file):
    with open(sessions_file) as f:
        data = json.load(f)
    
    # Custom processing
    for session in data['sessions']:
        print(f"{session['date']},{session['model']},{session['total_cost']}")

if __name__ == "__main__":
    custom_export(sys.argv[1])
```

Usage:
```bash
ocmonitor export sessions ~/.local/share/opencode/storage/message --format json --output temp.json
python3 custom_export.py temp.json > custom_report.csv
```

#### Configuration Templates

Create configuration templates for different use cases:

```bash
# Development configuration
cp config.toml config.dev.toml
# Edit config.dev.toml for development settings

# Production configuration  
cp config.toml config.prod.toml
# Edit config.prod.toml for production settings

# Use specific configuration
OCMONITOR_CONFIG=config.dev.toml ocmonitor sessions ~/.local/share/opencode/storage/message
```

---

*This completes the comprehensive documentation for OpenCode Monitor. For additional help, please refer to the GitHub repository or file an issue for support.*