# Aiwynn's Idea Factory 📚✨

A structured workspace for capturing, organizing, and developing AI-generated fiction novel ideas.

## Overview

This system is designed for writers who use LLMs to generate batches of story concepts and need an organized way to capture, search, and develop those ideas into full stories.

## Directory Structure

```
aiwynns-idea-factory/
├── concepts/              # AI-generated story concepts
│   ├── generated/        # Newly generated batches
│   ├── developing/       # Batches being refined
│   └── favorites/        # Cherry-picked favorites
├── stories/              # Stories in active development
├── templates/            # Templates for creating new content
│   ├── concept-batch.md        # For capturing 10+ concepts at once
│   └── story-development.md    # For developing a single story
├── scripts/              # Helper bash scripts
├── archive/              # Completed or abandoned projects
├── resources/            # Reference materials and inspiration
└── INDEX.md             # Auto-generated database index

```

## Quick Start

### 1. Generate concepts with an LLM

Example prompt:
```
Please generate 10 different high concept romantasy story ideas with these tropes:
enemies-to-lovers, magic academy, chosen one subversion
```

### 2. Capture the batch

```bash
./scripts/new-batch.sh
```

This will:
- Create a new batch file with today's date
- Prompt you for genre, tropes, and metadata
- Open the file for you to paste in the LLM's output

### 3. Review and organize

Browse your concepts:
```bash
./scripts/list-concepts.sh    # List all batches
./scripts/stats.sh             # View statistics
```

Search for specific elements:
```bash
./scripts/search.sh "time travel"
./scripts/search.sh -g fantasy -t "chosen one"
```

### 4. Develop a story

When you find a concept you want to expand:

```bash
./scripts/new-story.sh
```

This creates a comprehensive development file with sections for:
- Characters
- Plot structure
- World-building
- Themes
- Market positioning

### 5. Keep your index updated

```bash
./scripts/update-index.sh
```

This regenerates `INDEX.md` with all your concepts and stories.

## Workflow

```
LLM Generation → Capture Batch → Review → Mark Favorites → Develop Story → Archive
```

### Typical Session

1. **Brainstorm with LLM**: Generate 10-20 concepts around a theme
2. **Batch capture**: Run `new-batch.sh` and paste concepts
3. **Review**: Read through, add notes in "Initial Thoughts"
4. **Mark favorites**: Check boxes for standout concepts
5. **Extract**: Move favorite batches to `concepts/favorites/`
6. **Develop**: Use `new-story.sh` to expand chosen concepts
7. **Iterate**: Generate variations of promising ideas

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `new-batch.sh` | Create new concept batch from template |
| `new-story.sh` | Create new story development file |
| `list-concepts.sh` | List all concept batches with metadata |
| `search.sh` | Search through all concepts and stories |
| `update-index.sh` | Rebuild INDEX.md with current database |
| `stats.sh` | Display quick statistics dashboard |

### Search Examples

```bash
# Basic text search
./scripts/search.sh "magical realism"

# Filter by genre
./scripts/search.sh "murder mystery" -g thriller

# Filter by trope
./scripts/search.sh "romance" -t "enemies to lovers"

# Filter by status
./scripts/search.sh "space opera" -s developing
```

## Templates

### concept-batch.md

Optimized for capturing 10+ AI-generated concepts in one session. Includes:
- YAML frontmatter for metadata (genre, tropes, date, LLM model)
- Structured sections for each concept
- Checkboxes for marking favorites
- Space for initial reactions and notes

### story-development.md

Comprehensive template for fleshing out a single story:
- High concept and logline
- Character profiles (protagonist, antagonist, supporting)
- Three-act plot structure
- World-building details
- Theme exploration
- Market positioning (comps, target audience)
- Development log

## Best Practices

### Capturing Concepts

- **Be consistent**: Always fill in the YAML frontmatter
- **Save your prompts**: Keep the LLM prompt you used for reference
- **Initial reactions**: Jot down first impressions while fresh
- **Mark favorites immediately**: Don't wait - flag standouts right away

### Organization

- **Generated**: Keep raw LLM output here initially
- **Developing**: Move batches you're actively refining
- **Favorites**: Extract and store your best concepts
- **Update regularly**: Run `update-index.sh` after changes

### Development

- **Start small**: Don't develop every concept - be selective
- **Iterate with LLM**: Use the story template to generate more details with AI
- **Cross-reference**: Note the origin batch ID in story files
- **Version control**: Consider using git to track changes

## Tips for Working with LLMs

### Good prompts for concept generation:

```
Generate 10 [genre] story concepts that combine:
- Trope 1
- Trope 2
- Setting/constraint
Include: title, one-line hook, brief synopsis
```

### Iterating on concepts:

```
I have this story concept: [paste concept]
Generate 5 variations that explore different angles on this premise.
```

### Developing details:

```
For this story: [paste concept]
Create detailed character profiles for the protagonist and antagonist,
including motivation, backstory, and character arc.
```

## Maintenance

### Regular tasks

- Run `./scripts/update-index.sh` weekly
- Review and organize batches monthly
- Archive completed/abandoned stories quarterly
- Back up the entire directory regularly

### File naming

- Batches: `YYYYMMDD-NNN.md` (auto-generated)
- Stories: `story-title-lowercase.md` (descriptive, hyphenated)

## Customization

### Modify templates

Edit files in `templates/` to match your workflow. You might want to:
- Adjust the number of concepts per batch
- Add custom metadata fields
- Change the story development structure

### Add new scripts

The `scripts/` directory is yours to expand. Consider adding:
- Export scripts (to PDF, DOCX, etc.)
- Integration with writing tools
- Backup automation
- Statistical analysis

## Database Format

All data is stored as Markdown files with YAML frontmatter:

```yaml
---
batch_id: 20250108-001
genre: fantasy
tropes: [chosen one, magic academy]
status: generated
---

# Content follows...
```

This format is:
- Human-readable
- Version-control friendly
- Easy to parse with scripts
- Compatible with many static site generators
- LLM-friendly for further processing

## Getting Help

- Read the templates to understand expected formats
- Check `INDEX.md` to see the current state
- Run `./scripts/stats.sh` for an overview
- Use `search.sh` to find examples of how others structured things

## License

This is your personal workspace - customize freely!

---

**Happy writing!** 🖋️✨
