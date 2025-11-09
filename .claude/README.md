# Claude Code MCP Configuration

This directory contains the MCP server configuration for Claude Code.

## Configuration

The `config.json` file configures the Aiwynn's Idea Factory MCP server for this workspace.

The MCP server allows Claude Code to:
- Browse and search your story concept database
- Create new concept batches
- Develop concepts into full stories
- Add notes and manage story development
- Use natural language to interact with your ideas

## Usage

The MCP server is automatically available in Claude Code. You can use natural language like:

```
"Show me all my concept batches"
"Read batch 20251108-001"
"What concepts do I have with enemies-to-lovers?"
"Create a new romantasy batch with vampires and forbidden love"
"Develop concept 7 from batch 20251108-001"
"Add a note to bond-thief-academy about the magic system"
```

## Available Capabilities

### Resources (Read)
- List/read concept batches
- List/read story development files
- View database statistics
- Access INDEX.md

### Tools (Actions)
- `create_batch` - Create new concept batches
- `develop_concept` - Extract concept and create story file
- `add_note` - Add timestamped notes to stories
- `search_concepts` - Search through all content
- `update_index` - Rebuild INDEX.md

### Prompts (Templates)
- `generate_romantasy_concepts` - Generate story ideas
- `develop_character_profile` - Character development template
- `expand_plot_structure` - Plot structure template

## Troubleshooting

If the MCP server isn't working:

1. **Reload Claude Code window** - Changes to config require reload
2. **Check server is installed**:
   ```bash
   uv run idea-factory-mcp
   # Should start without errors (Ctrl+C to exit)
   ```
3. **Verify dependencies**:
   ```bash
   uv sync
   ```
4. **Check Claude Code logs** for MCP errors

## Architecture

The MCP server:
- Lives in `aiwynns/mcp_server.py`
- Uses FastMCP for clean stdio protocol
- Reuses all existing CLI modules (database, search, creator)
- Works on the same markdown files as the CLI
- No network/external dependencies

This means CLI and MCP work seamlessly together on the same data!

## See Also

- `../MCP-README.md` - Full MCP server documentation
- `../MCP-QUICKSTART.md` - Quick setup guide
