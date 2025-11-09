# MCP Server Quick Start

## Add to Claude Desktop

Edit your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this section (replace the path!):

```json
{
  "mcpServers": {
    "aiwynns-idea-factory": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/kalisti/aiwynns-idea-factory",
        "idea-factory-mcp"
      ]
    }
  }
}
```

## Restart Claude Desktop

After saving the config, restart Claude Desktop completely.

## Test It

Try these natural language commands in Claude Desktop:

```
"Show me all my concept batches"
"Read batch 20251108-001"
"What are my story statistics?"
"Create a new romantasy batch with enemies-to-lovers and magic academy tropes"
"Develop concept 7 from batch 20251108-001"
"Search for concepts with 'bond' in them"
```

## Available Capabilities

### Resources (Read)
- List all batches
- Read specific batch with all concepts
- List all stories
- Read specific story
- Get statistics
- Read INDEX.md

### Tools (Actions)
- create_batch
- develop_concept
- add_note
- search_concepts
- update_index

### Prompts (Templates)
- generate_romantasy_concepts
- develop_character_profile
- expand_plot_structure

## Troubleshooting

If Claude doesn't see the server:
1. Check the path is absolute (no ~, no relative paths)
2. Verify `uv` is in your PATH
3. Restart Claude Desktop
4. Check for errors in Claude's developer console

## Test Manually

```bash
# This should start without errors
uv run idea-factory-mcp

# It will wait for stdin (that's correct!)
# Press Ctrl+C to exit
```

See MCP-README.md for full documentation.
