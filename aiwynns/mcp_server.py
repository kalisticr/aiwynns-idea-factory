#!/usr/bin/env python3
"""
Aiwynn's Idea Factory - MCP Server
Exposes story concept management via Model Context Protocol
"""

import os
import json
from pathlib import Path
from typing import Optional, Any
from datetime import datetime, date

from fastmcp import FastMCP

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent

# Import our modules
from aiwynns.database import ConceptDatabase
from aiwynns.search import SearchEngine
from aiwynns.stats import StatsGenerator
from aiwynns.creator import Creator

# Initialize
db = ConceptDatabase(PROJECT_ROOT)
search_engine = SearchEngine(db)
stats_gen = StatsGenerator(db)
creator = Creator(PROJECT_ROOT)

# Create MCP server
mcp = FastMCP("Aiwynn's Idea Factory")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def serialize_for_json(obj: Any) -> Any:
    """Convert Python objects to JSON-serializable types"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj


# ============================================================================
# RESOURCES - Things the LLM can read
# ============================================================================

@mcp.resource("aiwynns://batches/list")
def list_batches() -> str:
    """List all concept batches in the database"""
    batches = db.get_all_batches()

    result = {
        "total": len(batches),
        "batches": []
    }

    for batch in batches:
        result["batches"].append({
            "batch_id": batch.get("batch_id"),
            "date": batch.get("date_generated"),
            "genre": batch.get("genre"),
            "tropes": batch.get("tropes"),
            "count": batch.get("count"),
            "status": batch.get("status"),
            "location": batch.get("location")
        })

    return json.dumps(serialize_for_json(result), indent=2)


@mcp.resource("aiwynns://batch/{batch_id}")
def read_batch(batch_id: str) -> str:
    """Read a specific batch with all its concepts"""
    batch = db.get_batch(batch_id)

    if not batch:
        return json.dumps({"error": f"Batch {batch_id} not found"})

    # Include full content
    result = {
        "batch_id": batch.get("batch_id"),
        "date_generated": batch.get("date_generated"),
        "genre": batch.get("genre"),
        "tropes": batch.get("tropes"),
        "count": batch.get("count"),
        "status": batch.get("status"),
        "llm_model": batch.get("llm_model"),
        "prompt_used": batch.get("prompt_used"),
        "concepts": []
    }

    for concept in batch.get("concepts", []):
        result["concepts"].append({
            "number": concept.get("number"),
            "title": concept.get("title"),
            "content": concept.get("content")
        })

    return json.dumps(serialize_for_json(result), indent=2)


@mcp.resource("aiwynns://stories/list")
def list_stories() -> str:
    """List all stories in development"""
    stories = db.get_all_stories()

    result = {
        "total": len(stories),
        "stories": []
    }

    for story in stories:
        result["stories"].append({
            "story_id": story.get("story_id"),
            "title": story.get("title"),
            "genre": story.get("genre"),
            "status": story.get("status"),
            "origin_batch": story.get("origin_batch"),
            "date_created": story.get("date_created"),
            "date_updated": story.get("date_updated"),
            "file_path": story.get("file_path")
        })

    return json.dumps(serialize_for_json(result), indent=2)


@mcp.resource("aiwynns://story/{story_name}")
def read_story(story_name: str) -> str:
    """Read a specific story development file"""
    story_file = PROJECT_ROOT / "stories" / f"{story_name}.md"

    if not story_file.exists():
        story_file = PROJECT_ROOT / "stories" / story_name
        if not story_file.exists():
            return json.dumps({"error": f"Story {story_name} not found"})

    with open(story_file, 'r') as f:
        content = f.read()

    return content


@mcp.resource("aiwynns://stats")
def get_stats() -> str:
    """Get database statistics"""
    stats = stats_gen.generate_stats()

    result = {
        "total_batches": stats["total_batches"],
        "total_concepts": stats["total_concepts"],
        "total_stories": stats["total_stories"],
        "stories_in_development": stats["stories_in_development"],
        "batches_by_status": dict(stats["batches_by_status"]),
        "top_genres": stats["top_genres"][:10],
        "top_tropes": stats["top_tropes"][:10]
    }

    return json.dumps(serialize_for_json(result), indent=2)


@mcp.resource("aiwynns://index")
def read_index() -> str:
    """Read the INDEX.md database file"""
    index_file = PROJECT_ROOT / "INDEX.md"

    if not index_file.exists():
        return "Index file not found. Run update_index tool to create it."

    with open(index_file, 'r') as f:
        return f.read()


# ============================================================================
# TOOLS - Actions the LLM can take
# ============================================================================

@mcp.tool()
def create_batch(genre: str, tropes: str, model: str, count: int = 10) -> str:
    """
    Create a new concept batch file from template

    Args:
        genre: Story genre (e.g., "Romantasy", "Fantasy", "SciFi")
        tropes: Comma-separated list of tropes
        model: LLM model used for generation (e.g., "Claude Sonnet 4.5")
        count: Number of concepts in batch (default: 10)
    """
    try:
        file_path = creator.create_batch(genre, tropes, model, count)
        return json.dumps({
            "success": True,
            "file": str(file_path),
            "message": f"Created batch file: {file_path.name}"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def develop_concept(batch_id: str, concept_number: int) -> str:
    """
    Extract a concept from a batch and create a story development file

    Args:
        batch_id: The batch ID (e.g., "20251108-001")
        concept_number: The concept number to develop (1-10)
    """
    try:
        # Get the batch
        batch = db.get_batch(batch_id)
        if not batch:
            return json.dumps({
                "success": False,
                "error": f"Batch {batch_id} not found"
            })

        # Find the concept
        concepts = batch.get('concepts', [])
        target_concept = None
        for concept in concepts:
            if concept.get('number') == str(concept_number):
                target_concept = concept
                break

        if not target_concept:
            return json.dumps({
                "success": False,
                "error": f"Concept #{concept_number} not found in batch {batch_id}"
            })

        # Extract concept data
        title = target_concept.get('title', f'Concept {concept_number}')
        content = target_concept.get('content', '')

        # Parse content for high concept, synopsis, etc.
        lines = content.split('\n')
        high_concept = ""
        synopsis = ""
        key_elements = []

        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith('**High Concept**:'):
                current_section = 'high_concept'
                high_concept = line.replace('**High Concept**:', '').strip()
            elif line.startswith('**Synopsis**:'):
                current_section = 'synopsis'
                synopsis = line.replace('**Synopsis**:', '').strip()
            elif line.startswith('**Key Elements**:'):
                current_section = 'key_elements'
            elif line.startswith('-') and current_section == 'key_elements':
                key_elements.append(line[1:].strip())
            elif line and current_section == 'synopsis' and not line.startswith('**'):
                synopsis += ' ' + line

        # Create story file
        filename = creator._slugify(title)
        story_id = f"{filename}-{int(datetime.now().timestamp())}"
        story_file = PROJECT_ROOT / "stories" / f"{filename}.md"

        if story_file.exists():
            return json.dumps({
                "success": False,
                "error": f"Story file {filename}.md already exists"
            })

        # Read template
        template_file = PROJECT_ROOT / "templates" / "story-development.md"
        with open(template_file, 'r') as f:
            template_content = f.read()

        # Replace placeholders
        genre = batch.get('genre', 'Unknown')
        today = datetime.now().strftime("%Y-%m-%d")

        story_content = template_content.replace("[unique-id]", story_id)
        story_content = story_content.replace("[Working Title]", title)
        story_content = story_content.replace("[Story Title]", title)
        story_content = story_content.replace("[genre]", genre)
        story_content = story_content.replace("[batch_id if from generated concepts]", batch_id)
        story_content = story_content.replace("YYYY-MM-DD", today)
        story_content = story_content.replace(
            "[One-line pitch that captures the essence]",
            high_concept if high_concept else "[One-line pitch that captures the essence]"
        )
        story_content = story_content.replace(
            "[2-3 sentence compelling description]",
            synopsis if synopsis else "[2-3 sentence compelling description]"
        )

        # Add key elements to dev notes
        dev_notes = f"\n### [{today}] From Batch {batch_id}, Concept #{concept_number}\n\n"
        if key_elements:
            dev_notes += "**Key Elements from Concept:**\n"
            for element in key_elements:
                dev_notes += f"- {element}\n"

        if "## Development Notes" in story_content:
            story_content = story_content.replace(
                "## Development Notes",
                f"## Development Notes{dev_notes}"
            )

        # Write file
        with open(story_file, 'w') as f:
            f.write(story_content)

        return json.dumps({
            "success": True,
            "story_file": str(story_file),
            "story_name": filename,
            "title": title,
            "message": f"Created story development file: {filename}.md"
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def add_note(story_name: str, note_text: str, section: Optional[str] = None) -> str:
    """
    Add a note to a story development file

    Args:
        story_name: Name of the story (without .md extension)
        note_text: The note content to add
        section: Optional section to add note to (default: Development Notes)
    """
    try:
        story_file = PROJECT_ROOT / "stories" / f"{story_name}.md"

        if not story_file.exists():
            story_file = PROJECT_ROOT / "stories" / story_name
            if not story_file.exists():
                return json.dumps({
                    "success": False,
                    "error": f"Story {story_name} not found"
                })

        with open(story_file, 'r') as f:
            content = f.read()

        # Format note with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        note_entry = f"\n### [{timestamp}]\n{note_text}\n"

        # Add to appropriate section
        if section:
            target_section = f"## {section.title()}"
            if target_section in content:
                parts = content.split(target_section)
                if len(parts) > 1:
                    next_section_idx = parts[1].find('\n## ')
                    if next_section_idx != -1:
                        parts[1] = parts[1][:next_section_idx] + note_entry + parts[1][next_section_idx:]
                    else:
                        parts[1] += note_entry
                    content = target_section.join(parts)
            else:
                section = None

        if not section:
            if "## Development Notes" in content:
                content = content.replace("## Development Notes", f"## Development Notes{note_entry}", 1)
            else:
                content += f"\n\n## Development Notes{note_entry}"

        # Update date_updated
        import yaml
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                frontmatter['date_updated'] = datetime.now().strftime("%Y-%m-%d")
                parts[1] = '\n' + yaml.dump(frontmatter, default_flow_style=False)
                content = '---'.join(parts)
            except:
                pass

        with open(story_file, 'w') as f:
            f.write(content)

        return json.dumps({
            "success": True,
            "message": f"Note added to {story_name}",
            "note": note_text
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def search_concepts(
    query: str,
    genre: Optional[str] = None,
    trope: Optional[str] = None,
    status: Optional[str] = None,
    fuzzy: bool = False,
    limit: int = 20
) -> str:
    """
    Search through all concepts and stories

    Args:
        query: Search term
        genre: Optional genre filter
        trope: Optional trope filter
        status: Optional status filter
        fuzzy: Use fuzzy matching (default: False)
        limit: Maximum results to return (default: 20)
    """
    try:
        results = search_engine.search(
            query=query,
            genre=genre,
            trope=trope,
            status=status,
            fuzzy=fuzzy,
            limit=limit
        )

        return json.dumps(serialize_for_json({
            "success": True,
            "count": len(results),
            "results": results
        }), indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def update_index() -> str:
    """Update the INDEX.md database file with current state"""
    try:
        from aiwynns.indexer import Indexer

        indexer = Indexer(PROJECT_ROOT, db)
        indexer.update_index()

        return json.dumps({
            "success": True,
            "message": "INDEX.md updated successfully"
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


# ============================================================================
# PROMPTS - Reusable templates
# ============================================================================

@mcp.prompt()
def generate_romantasy_concepts(tropes: str, count: int = 10) -> str:
    """
    Template for generating romantasy story concepts

    Args:
        tropes: Comma-separated list of tropes to include
        count: Number of concepts to generate (default: 10)
    """
    return f"""Generate {count} high-concept romantasy story ideas that incorporate these tropes: {tropes}

For each concept, provide:
1. A compelling title
2. A one-line high concept hook
3. A 2-3 sentence synopsis
4. Key story elements (3-5 bullet points)

Make each concept unique and compelling with strong romantic and fantasy elements. Focus on fresh takes and unexpected combinations of the tropes."""


@mcp.prompt()
def develop_character_profile(character_role: str, story_context: str) -> str:
    """
    Template for developing a character profile

    Args:
        character_role: Role in story (e.g., "protagonist", "love interest", "antagonist")
        story_context: Brief story context to inform character development
    """
    return f"""Develop a detailed character profile for a {character_role} in this story context:

{story_context}

Include:
1. Name and physical appearance
2. Personality traits and quirks
3. Backstory and formative experiences
4. Goals and motivations
5. Internal conflicts and fears
6. Character arc (how they change)
7. Relationships with other characters
8. Unique voice or mannerisms

Make the character complex, flawed, and compelling."""


@mcp.prompt()
def expand_plot_structure(premise: str) -> str:
    """
    Template for expanding a premise into full plot structure

    Args:
        premise: The story premise or high concept
    """
    return f"""Expand this story premise into a detailed three-act plot structure:

{premise}

Provide:

**ACT 1 - SETUP**
- Opening scene/hook
- Inciting incident
- First major turning point

**ACT 2 - CONFRONTATION**
- Rising complications (3-5 major plot points)
- Midpoint twist
- Low point/crisis

**ACT 3 - RESOLUTION**
- Climax
- Resolution
- Ending

Also include:
- 2-3 subplots that weave through the main plot
- Key character development moments
- Pacing notes"""


# ============================================================================
# MAIN - Run the server
# ============================================================================

def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
