# Workspace Setup Guide

This guide explains how to set up a new Aiwynn's Idea Factory workspace for your story concepts.

## Quick Start

Run this command to create a new workspace:

```bash
curl -sSL https://raw.githubusercontent.com/kalisticr/aiwynns-idea-factory/master/setup-idea-factory.sh | bash -s my-stories
```

Replace `my-stories` with your desired workspace name.

## What Gets Created

The setup script creates:

```
my-stories/
├── .venv/                      # Python virtual environment
├── concepts/
│   ├── generated/             # Generated concept batches
│   ├── developing/            # Concepts being developed
│   └── favorites/             # Favorite concepts
├── stories/                   # Story development files
├── templates/                 # Story and batch templates
├── resources/                 # Reference materials (tropes, etc.)
├── archive/                   # Old/experimental content
├── .mcp.json                  # MCP server configuration for Claude Code
├── .gitignore                 # Git ignore rules
└── INDEX.md                   # Content database index
```

## How It Works

### Framework vs Content Separation

- **Framework**: Installed as a Python package in your venv (`aiwynns-idea-factory`)
- **Content**: Your stories, concepts, and notes live in the workspace directory
- **Templates & Resources**: Downloaded from the framework repo into your workspace

### The Framework Package

The installed package provides:
- `idea-factory` CLI tool
- `idea-factory-mcp` MCP server for Claude Code
- All Python modules (database, search, stats, etc.)

### MCP Server Configuration

The `.mcp.json` file is pre-configured to run the MCP server from the installed package, pointing at your workspace directory. Claude Code will automatically detect and connect to it.

## Usage

After setup:

```bash
cd my-stories
source .venv/bin/activate

# Use the CLI
idea-factory stats
idea-factory list
idea-factory --help

# Or use with Claude Code
# Open the workspace directory in Claude Code and the MCP server will be available
```

## Updating the Framework

To update to the latest framework version:

```bash
cd my-stories
source .venv/bin/activate
uv pip install --upgrade "git+https://github.com/kalisticr/aiwynns-idea-factory.git"
```

Your content stays separate and safe during updates.

## Git Integration

The workspace is initialized as a git repository (optional). You can:

1. **Track your content**: Push to your own GitHub repo
   ```bash
   git remote add origin https://github.com/you/my-stories.git
   git add .
   git commit -m "Initial stories"
   git push -u origin master
   ```

2. **Keep content private**: The `.gitignore` includes commented-out rules. Uncomment them to exclude your stories from git.

## Multiple Workspaces

You can create as many workspaces as you want:

```bash
curl -sSL ... | bash -s romance-stories
curl -sSL ... | bash -s scifi-stories
curl -sSL ... | bash -s fantasy-stories
```

Each workspace is completely independent with its own:
- Virtual environment
- Content and stories
- Git repository (optional)

## Development Mode

If you want to contribute to the framework itself, clone the repo directly:

```bash
git clone https://github.com/kalisticr/aiwynns-idea-factory.git
cd aiwynns-idea-factory
./setup.sh
```

The MCP server automatically detects when it's running from the development repo vs an installed package.
