#!/usr/bin/env bash
set -e

# Aiwynn's Idea Factory - Workspace Setup Script
# Downloads and configures a new content workspace

WORKSPACE_NAME="${1:-my-stories}"
FRAMEWORK_REPO="https://github.com/kalisticr/aiwynns-idea-factory.git"

echo "📚 Aiwynn's Idea Factory - Workspace Setup"
echo "==========================================="
echo ""
echo "Creating workspace: $WORKSPACE_NAME"
echo ""

# Create workspace directory
mkdir -p "$WORKSPACE_NAME"
cd "$WORKSPACE_NAME"

# Create directory structure
mkdir -p concepts/{generated,developing,favorites}
mkdir -p stories
mkdir -p archive
mkdir -p resources

echo "✓ Created directory structure"

# Set up Python virtual environment with uv
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "Setting up Python virtual environment..."
uv venv --python 3.12

echo "✓ Created virtual environment"

# Install the framework package
echo "Installing Aiwynn's Idea Factory framework..."
uv pip install "git+${FRAMEWORK_REPO}"

echo "✓ Installed framework package"

# Download templates from repo
echo "Downloading templates..."
TEMPLATES_URL="https://raw.githubusercontent.com/kalisticr/aiwynns-idea-factory/master/templates"
mkdir -p templates

curl -sL "${TEMPLATES_URL}/story-development.md" -o templates/story-development.md
curl -sL "${TEMPLATES_URL}/concept-batch.md" -o templates/concept-batch.md

echo "✓ Downloaded templates"

# Create .gitignore for content workspace
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Exports
export-*.json
export-*.csv
export-*.yaml
*.bak

# Claude Code
.claude/logs/

# Optional: Track your content, or ignore it
# Uncomment lines below to keep your stories private:
# concepts/
# stories/
# INDEX.md
# archive/
EOF

echo "✓ Created .gitignore"

# Create .mcp.json for Claude Code
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "aiwynns-idea-factory": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "WORKSPACE_PATH",
        "idea-factory-mcp"
      ]
    }
  }
}
EOF

# Replace WORKSPACE_PATH with actual path
WORKSPACE_PATH=$(pwd)
sed -i "s|WORKSPACE_PATH|$WORKSPACE_PATH|g" .mcp.json

echo "✓ Created MCP configuration"

# Create initial INDEX.md
cat > INDEX.md << 'EOF'
# Story Concepts Index

This file tracks all story concepts in the database.

## Statistics
- Total Batches: 0
- Total Concepts: 0
- Stories in Development: 0
- Total Stories: 0

---

## Concept Batches

---

## Stories in Development

---

## Manual Updates
You can manually add notes and cross-references below this line.
EOF

echo "✓ Created INDEX.md"

# Create .claude directory for Claude Code
mkdir -p .claude

cat > .claude/README.md << 'EOF'
# Claude Code Configuration

This directory contains Claude Code configuration for this workspace.

The MCP server is configured to use the installed `aiwynns-idea-factory` package.
EOF

echo "✓ Created Claude Code configuration"

# Initialize git repo (optional)
if command -v git &> /dev/null; then
    git init
    echo "✓ Initialized git repository"
fi

echo ""
echo "🎉 Workspace setup complete!"
echo ""
echo "Next steps:"
echo "  1. cd $WORKSPACE_NAME"
echo "  2. source .venv/bin/activate"
echo "  3. Open in Claude Code to start creating stories!"
echo ""
echo "Available commands:"
echo "  idea-factory --help        # CLI help"
echo "  idea-factory stats         # View statistics"
echo "  idea-factory list-batches  # List concept batches"
echo "  idea-factory list-stories  # List stories in development"
echo ""
echo "MCP server is configured and ready for Claude Code integration."
