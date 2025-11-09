# Aiwynn's Idea Factory - MCP Server

The Idea Factory can be used as a Model Context Protocol (MCP) server, allowing Claude Desktop, Claude Code, and other MCP-enabled applications to interact with your story database using natural language.

## Features

### Resources (Read Access)
- `aiwynns://batches/list` - List all concept batches
- `aiwynns://batch/{batch_id}` - Read a specific batch with all concepts
- `aiwynns://stories/list` - List all stories in development
- `aiwynns://story/{story_name}` - Read a specific story file
- `aiwynns://stats` - Get database statistics
- `aiwynns://index` - Read the INDEX.md file

### Tools (Actions)
- `create_batch` - Create a new concept batch
- `develop_concept` - Extract concept from batch and create story file
- `add_note` - Add timestamped notes to story files
- `search_concepts` - Search through concepts and stories
- `update_index` - Update INDEX.md

### Prompts (Templates)
- `generate_romantasy_concepts` - Template for generating romantasy ideas
- `develop_character_profile` - Template for character development
- `expand_plot_structure` - Template for plot expansion

## Installation

1. Install dependencies:
```bash
uv sync
```

2. The MCP server is installed as `idea-factory-mcp` command.

## Configuration

### For Claude Desktop

Add this to your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "aiwynns-idea-factory": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/FULL/PATH/TO/aiwynns-idea-factory",
        "idea-factory-mcp"
      ]
    }
  }
}
```

**Important**: Replace `/FULL/PATH/TO/aiwynns-idea-factory` with the actual absolute path to this directory.

### For Claude Code

Add to your workspace `.claude/config.json`:

```json
{
  "mcpServers": {
    "aiwynns-idea-factory": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${workspaceFolder}",
        "idea-factory-mcp"
      ]
    }
  }
}
```

## Usage Examples

Once configured, you can interact with your story database naturally:

### Viewing Concepts
```
"Show me all my romantasy concept batches"
"Read batch 20251108-001 and show me concept 7"
"What are my database statistics?"
```

### Creating Content
```
"Create a new romantasy batch with enemies-to-lovers and fated mates tropes"
"Develop concept 7 from batch 20251108-001 into a full story"
"Add a note to bond-thief-academy: 'What if bonds glow like threads?'"
```

### Searching
```
"Search for all concepts with 'magic academy' trope"
"Find stories with enemies to lovers theme using fuzzy search"
```

### Story Development
```
"Show me the Bond Thief Academy story"
"Help me develop the protagonist for Bond Thief Academy"
"Expand the plot structure for The Rejection Protocol"
```

### Using Prompts
```
"Use the romantasy concepts prompt to generate 10 ideas with fake relationship and grumpy sunshine tropes"
"Use the character profile prompt to develop the antagonist for my story"
```

## Testing the MCP Server

Test that the server works:

```bash
# Run the MCP server directly (it will wait for stdio commands)
uv run idea-factory-mcp
```

The server should start and wait for MCP protocol messages via stdin/stdout.

You can also use MCP inspector tools:
```bash
npx @modelcontextprotocol/inspector uv run --directory /path/to/aiwynns-idea-factory idea-factory-mcp
```

## Architecture

The MCP server uses:
- **FastMCP** for clean, decorator-based MCP protocol implementation
- **stdio transport** for local, secure communication
- **Existing aiwynns package** - all the database, search, and creation logic you already have
- **Same data files** - works on the same markdown files as the CLI

This means:
- You can use CLI and MCP simultaneously
- No data duplication
- Changes made via MCP are immediately visible in CLI and vice versa
- Simple, file-based architecture

## Workflow Comparison

### CLI Workflow
```bash
./idea-factory new-batch
# ... manually edit file ...
./idea-factory review-batch 20251108-001 -c 7
./idea-factory develop-concept 20251108-001 7
```

### MCP Workflow (via Claude)
```
"Create a romantasy batch with vampires and forbidden love"
"Show me concept 3 from the latest batch"
"Develop concept 3 into a full story and help me flesh out the characters"
```

Both work on the same files, use the same logic, just different interfaces!

## Troubleshooting

### Server not showing up in Claude
1. Check the config file path is correct
2. Verify the absolute path in the config matches your installation
3. Restart Claude Desktop/Code after editing config
4. Check Claude's logs for MCP errors

### Permission errors
Make sure the server script is executable:
```bash
chmod +x aiwynns/mcp_server.py
```

### Import errors
Reinstall dependencies:
```bash
uv sync
```

### Testing without Claude
Use the MCP inspector:
```bash
npx @modelcontextprotocol/inspector uv run idea-factory-mcp
```

## Security

The MCP server:
- ✅ Runs locally only (no network)
- ✅ Uses stdio (only accessible to local user)
- ✅ Only accesses files in the idea-factory directory
- ✅ No external API calls
- ✅ File-based authentication (Unix file permissions)

## Development

The MCP server code is in `aiwynns/mcp_server.py`. It's a FastMCP application that:

1. Imports existing modules (database, search, creator, stats)
2. Exposes resources via `@mcp.resource()` decorator
3. Exposes tools via `@mcp.tool()` decorator
4. Exposes prompts via `@mcp.prompt()` decorator
5. Runs as stdio server via `mcp.run()`

To add new functionality:
1. Add the logic to an existing aiwynns module
2. Expose it via MCP decorator in mcp_server.py
3. Test with MCP inspector
4. Document in this file

## Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/model-context-protocol)
