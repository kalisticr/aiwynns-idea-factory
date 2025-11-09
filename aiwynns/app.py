#!/usr/bin/env python3
"""
Aiwynn's Idea Factory - Main CLI Manager
A sophisticated tool for managing AI-generated story concepts
"""

import os
import sys
from pathlib import Path
from importlib.metadata import version

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box

# Get workspace root
# When installed as package, use CWD (user's workspace)
# When developing, use package parent directory
if Path.cwd().name == "aiwynns-idea-factory":
    # Development mode: running from repo
    PROJECT_ROOT = Path(__file__).parent.parent
else:
    # Installed mode: use current working directory as workspace
    PROJECT_ROOT = Path.cwd()

from aiwynns.database import ConceptDatabase
from aiwynns.search import SearchEngine
from aiwynns.stats import StatsGenerator
from aiwynns.creator import Creator
from aiwynns.logging_config import setup_logging
import logging

# Setup logging (INFO level for CLI, logs to file if AIWYNNS_LOG_FILE env var is set)
setup_logging(level=logging.INFO, console_output=False)
logger = logging.getLogger(__name__)

console = Console()
db = ConceptDatabase(PROJECT_ROOT)


@click.group()
@click.version_option(version=version("aiwynns-idea-factory"))
def cli():
    """
    Aiwynn's Idea Factory - Manage your story concepts with style!

    A sophisticated system for capturing, organizing, and developing
    AI-generated fiction novel ideas.
    """
    pass


@cli.command()
@click.option('--status', '-s', help='Filter by status')
@click.option('--genre', '-g', help='Filter by genre')
@click.option('--sort', '-S', type=click.Choice(['date', 'count', 'genre']), default='date')
def list_batches(status, genre, sort):
    """List all concept batches"""
    batches = db.get_all_batches()

    # Apply filters
    if status:
        batches = [b for b in batches if b.get('status') == status]
    if genre:
        batches = [b for b in batches if genre.lower() in str(b.get('genre', '')).lower()]

    # Sort
    if sort == 'date':
        batches.sort(key=lambda x: x.get('date_generated', ''), reverse=True)
    elif sort == 'count':
        batches.sort(key=lambda x: x.get('count', 0), reverse=True)
    elif sort == 'genre':
        batches.sort(key=lambda x: x.get('genre', ''))

    if not batches:
        console.print("[yellow]No batches found.[/yellow]")
        return

    # Create table
    table = Table(title="📚 Concept Batches", box=box.ROUNDED)
    table.add_column("Batch ID", style="cyan", no_wrap=True)
    table.add_column("Date", style="green")
    table.add_column("Genre", style="magenta")
    table.add_column("Count", justify="right", style="yellow")
    table.add_column("Status", style="blue")
    table.add_column("Location", style="dim")

    for batch in batches:
        table.add_row(
            str(batch.get('batch_id', 'N/A')),
            str(batch.get('date_generated', 'N/A')),
            str(batch.get('genre', 'N/A')),
            str(batch.get('count', 0)),
            str(batch.get('status', 'N/A')),
            str(batch.get('location', 'N/A'))
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(batches)} batches[/dim]")


@cli.command()
@click.option('--status', '-s', help='Filter by status')
@click.option('--genre', '-g', help='Filter by genre')
@click.option('--sort', '-S', type=click.Choice(['title', 'created', 'updated', 'genre']), default='updated')
def list_stories(status, genre, sort):
    """List all stories in development"""
    stories = db.get_all_stories()

    # Apply filters
    if status:
        stories = [s for s in stories if s.get('status') == status]
    if genre:
        stories = [s for s in stories if genre.lower() in str(s.get('genre', '')).lower()]

    # Sort
    if sort == 'title':
        stories.sort(key=lambda x: str(x.get('title', '')))
    elif sort == 'created':
        stories.sort(key=lambda x: str(x.get('date_created', '')), reverse=True)
    elif sort == 'updated':
        stories.sort(key=lambda x: str(x.get('date_updated', '')), reverse=True)
    elif sort == 'genre':
        stories.sort(key=lambda x: str(x.get('genre', '')))

    if not stories:
        console.print("[yellow]No stories found.[/yellow]")
        return

    # Create table
    table = Table(title="📖 Stories in Development", box=box.ROUNDED)
    table.add_column("Story Name", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Genre", style="magenta")
    table.add_column("Status", style="blue")
    table.add_column("Created", style="green")
    table.add_column("Updated", style="yellow")

    for story in stories:
        # Extract story name (filename without .md) from file_path
        file_path = story.get('file_path', '')
        if file_path:
            story_name = Path(file_path).stem  # Gets filename without extension
        else:
            story_name = 'N/A'

        table.add_row(
            story_name,
            str(story.get('title', 'N/A')),
            str(story.get('genre', 'N/A')),
            str(story.get('status', 'N/A')),
            str(story.get('date_created', 'N/A')),
            str(story.get('date_updated', 'N/A'))
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(stories)} stories[/dim]")
    console.print(f"[dim]Use: idea-factory review-story <story-name>[/dim]")


@cli.command()
@click.argument('query')
@click.option('--genre', '-g', help='Filter by genre')
@click.option('--trope', '-t', help='Filter by trope')
@click.option('--status', '-s', help='Filter by status')
@click.option('--fuzzy', '-f', is_flag=True, help='Use fuzzy matching')
@click.option('--limit', '-l', default=20, help='Max results to show')
def search(query, genre, trope, status, fuzzy, limit):
    """Search through concepts and stories"""
    search_engine = SearchEngine(db)

    results = search_engine.search(
        query=query,
        genre=genre,
        trope=trope,
        status=status,
        fuzzy=fuzzy,
        limit=limit
    )

    if not results:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return

    console.print(Panel(
        f"🔍 Search Results for: [bold cyan]{query}[/bold cyan]",
        box=box.DOUBLE
    ))

    for i, result in enumerate(results, 1):
        console.print(f"\n[bold cyan]{i}. {result['title']}[/bold cyan]")
        console.print(f"   [dim]Type:[/dim] {result['type']}")
        console.print(f"   [dim]Genre:[/dim] {result.get('genre', 'N/A')}")
        console.print(f"   [dim]File:[/dim] {result['file']}")

        if 'score' in result:
            console.print(f"   [dim]Match:[/dim] {result['score']:.0%}")

        if 'preview' in result:
            console.print(f"   [dim]Preview:[/dim] {result['preview'][:150]}...")

    console.print(f"\n[dim]Showing {len(results)} of {len(results)} results[/dim]")


@cli.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed statistics')
def stats(detailed):
    """Display statistics and analytics"""
    stats_gen = StatsGenerator(db)
    stats_data = stats_gen.generate_stats()

    # Overview panel
    overview = f"""
[bold cyan]📊 Batches:[/bold cyan] {stats_data['total_batches']}
    Generated: {stats_data['batches_by_status'].get('generated', 0)}
    Developing: {stats_data['batches_by_status'].get('developing', 0)}
    Favorites: {stats_data['batches_by_status'].get('favorites', 0)}

[bold cyan]💡 Concepts:[/bold cyan] {stats_data['total_concepts']}

[bold cyan]📚 Stories:[/bold cyan] {stats_data['total_stories']}
    In Development: {stats_data['stories_in_development']}
    """

    console.print(Panel(overview, title="Aiwynn's Idea Factory", box=box.DOUBLE))

    # Top genres
    if stats_data['top_genres']:
        console.print("\n[bold]🏷️  Top Genres[/bold]")
        for genre, count in stats_data['top_genres'][:5]:
            console.print(f"  {genre}: [cyan]{count}[/cyan]")

    # Top tropes
    if stats_data['top_tropes']:
        console.print("\n[bold]🔖 Top Tropes[/bold]")
        for trope, count in stats_data['top_tropes'][:5]:
            console.print(f"  {trope}: [cyan]{count}[/cyan]")

    if detailed:
        # Recent activity
        if stats_data['recent_batches']:
            console.print("\n[bold]📅 Recent Activity[/bold]")
            for batch in stats_data['recent_batches'][:5]:
                console.print(f"  {batch['date_generated']}: {batch['batch_id']} ({batch['genre']})")


@cli.command()
@click.option('--genre', '-g', prompt='Genre', help='Story genre')
@click.option('--tropes', '-t', prompt='Tropes (comma-separated)', help='Story tropes')
@click.option('--model', '-m', prompt='LLM model used', help='Which LLM generated these')
@click.option('--count', '-c', default=10, help='Number of concepts')
def new_batch(genre, tropes, model, count):
    """Create a new concept batch"""
    creator = Creator(PROJECT_ROOT)
    file_path = creator.create_batch(genre, tropes, model, count)

    console.print(Panel(
        f"[green]✓[/green] Created new batch: [cyan]{file_path.name}[/cyan]\n\n"
        f"Next steps:\n"
        f"1. Open the file and paste your LLM-generated concepts\n"
        f"2. Fill in the 'Initial Thoughts' for each concept\n"
        f"3. Mark your favorites\n"
        f"4. Run: [cyan]./idea-factory.py update-index[/cyan]",
        title="New Batch Created",
        box=box.ROUNDED
    ))

    console.print(f"\n[dim]File: {file_path}[/dim]")


@cli.command()
@click.option('--title', '-t', prompt='Story title', help='Working title')
@click.option('--genre', '-g', prompt='Genre', help='Story genre')
@click.option('--origin', '-o', help='Origin batch ID (if any)')
def new_story(title, genre, origin):
    """Create a new story development file"""
    creator = Creator(PROJECT_ROOT)
    file_path = creator.create_story(title, genre, origin)

    console.print(Panel(
        f"[green]✓[/green] Created new story: [cyan]{title}[/cyan]\n\n"
        f"The comprehensive development template is ready for you to fill in.",
        title="New Story Created",
        box=box.ROUNDED
    ))

    console.print(f"\n[dim]File: {file_path}[/dim]")


@cli.command()
def update_index():
    """Update the INDEX.md database file"""
    from aiwynns.indexer import Indexer

    indexer = Indexer(PROJECT_ROOT, db)
    indexer.update_index()

    console.print("[green]✓[/green] INDEX.md updated successfully!")


@cli.command()
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'yaml']), default='json')
@click.option('--output', '-o', help='Output file path')
@click.option('--type', '-t', type=click.Choice(['batches', 'stories', 'all']), default='all')
def export(format, output, type):
    """Export data to various formats"""
    from aiwynns.exporter import Exporter

    exporter = Exporter(db)

    if not output:
        output = f"export-{type}.{format}"

    exporter.export(type=type, format=format, output_path=output)

    console.print(f"[green]✓[/green] Exported to: [cyan]{output}[/cyan]")


@cli.command()
@click.argument('batch_id')
def show(batch_id):
    """Show detailed view of a specific batch"""
    batch = db.get_batch(batch_id)

    if not batch:
        console.print(f"[red]Batch '{batch_id}' not found[/red]")
        return

    # Display batch details
    panel_content = f"""
[bold]Genre:[/bold] {batch.get('genre', 'N/A')}
[bold]Date:[/bold] {batch.get('date_generated', 'N/A')}
[bold]Status:[/bold] {batch.get('status', 'N/A')}
[bold]Count:[/bold] {batch.get('count', 0)}
[bold]Tropes:[/bold] {batch.get('tropes', 'N/A')}
[bold]Model:[/bold] {batch.get('llm_model', 'N/A')}
    """

    console.print(Panel(panel_content, title=f"📦 {batch_id}", box=box.ROUNDED))

    # Show prompt if available
    if batch.get('prompt_used'):
        console.print("\n[bold]Prompt Used:[/bold]")
        console.print(Panel(batch['prompt_used'], box=box.SIMPLE))

    console.print(f"\n[dim]File: {batch.get('file_path')}[/dim]")


@cli.command()
@click.argument('batch_id')
@click.option('--concept', '-c', type=int, help='Show only specific concept number')
@click.option('--no-metadata', is_flag=True, help='Hide YAML frontmatter')
def review_batch(batch_id, concept, no_metadata):
    """Review a batch with beautiful markdown rendering"""
    batch = db.get_batch(batch_id)

    if not batch:
        console.print(f"[red]Batch '{batch_id}' not found[/red]")
        return

    file_path = batch.get('file_path')

    if not file_path:
        console.print("[red]Batch file path not found[/red]")
        return

    # Read the raw file
    with open(file_path, 'r') as f:
        content = f.read()

    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[1].strip()
        markdown_content = parts[2].strip()
    else:
        frontmatter = ""
        markdown_content = content

    # Show metadata unless disabled
    if not no_metadata:
        console.print(Panel(
            f"[bold cyan]Batch:[/bold cyan] {batch_id}\n"
            f"[bold cyan]Genre:[/bold cyan] {batch.get('genre')}\n"
            f"[bold cyan]Date:[/bold cyan] {batch.get('date_generated')}\n"
            f"[bold cyan]Concepts:[/bold cyan] {batch.get('count')}\n"
            f"[bold cyan]Tropes:[/bold cyan] {batch.get('tropes')}",
            title="📦 Batch Info",
            box=box.ROUNDED
        ))
        console.print()

    # If specific concept requested, filter to that
    if concept:
        # Extract just that concept
        lines = markdown_content.split('\n')
        concept_lines = []
        in_target_concept = False

        for line in lines:
            if line.startswith(f'## Concept {concept}:'):
                in_target_concept = True
                concept_lines.append(line)
            elif in_target_concept:
                if line.startswith('## Concept '):
                    break
                concept_lines.append(line)

        if concept_lines:
            markdown_content = '\n'.join(concept_lines)
        else:
            console.print(f"[yellow]Concept #{concept} not found in this batch[/yellow]")
            return

    # Render the markdown
    md = Markdown(markdown_content)
    console.print(md)

    # Show file path at bottom
    console.print()
    console.print(f"[dim]File: {file_path}[/dim]")


@cli.command()
@click.argument('batch_id')
@click.argument('concept_number', type=int)
def develop_concept(batch_id, concept_number):
    """Extract a concept from a batch and create a story development file"""
    from datetime import datetime

    # Get the batch
    batch = db.get_batch(batch_id)

    if not batch:
        console.print(f"[red]Batch '{batch_id}' not found[/red]")
        return

    # Find the concept
    concepts = batch.get('concepts', [])

    target_concept = None
    for concept in concepts:
        if concept.get('number') == str(concept_number):
            target_concept = concept
            break

    if not target_concept:
        console.print(f"[red]Concept #{concept_number} not found in batch {batch_id}[/red]")
        console.print(f"[dim]This batch has {len(concepts)} concepts[/dim]")
        return

    # Extract concept data
    title = target_concept.get('title', f'Concept {concept_number}')
    content = target_concept.get('content', '')

    # Parse content to extract high concept, synopsis, key elements
    lines = content.split('\n')
    high_concept = ""
    synopsis = ""
    key_elements = []
    initial_thoughts = ""

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
        elif line.startswith('**Initial Thoughts**:'):
            current_section = 'initial_thoughts'
            initial_thoughts = line.replace('**Initial Thoughts**:', '').strip()
        elif line.startswith('-') and current_section == 'key_elements':
            key_elements.append(line[1:].strip())
        elif line and current_section == 'synopsis' and not line.startswith('**'):
            synopsis += ' ' + line
        elif line and current_section == 'initial_thoughts' and not line.startswith('**'):
            initial_thoughts += ' ' + line

    # Create story filename from title
    from aiwynns.creator import Creator
    creator = Creator(PROJECT_ROOT)
    filename = creator._slugify(title)
    story_id = f"{filename}-{int(datetime.now().timestamp())}"

    story_file = PROJECT_ROOT / "stories" / f"{filename}.md"

    # Check if file exists
    if story_file.exists():
        if not click.confirm(f"Story file '{filename}.md' already exists. Overwrite?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    # Read the story template
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

    # Replace high concept and logline with extracted data
    story_content = story_content.replace(
        "[One-line pitch that captures the essence]",
        high_concept if high_concept else "[One-line pitch that captures the essence]"
    )
    story_content = story_content.replace(
        "[2-3 sentence compelling description]",
        synopsis if synopsis else "[2-3 sentence compelling description]"
    )

    # Add key elements and initial thoughts to Development Notes
    dev_notes = f"\n### [{today}] From Batch {batch_id}, Concept #{concept_number}\n\n"

    if key_elements:
        dev_notes += "**Key Elements from Concept:**\n"
        for element in key_elements:
            dev_notes += f"- {element}\n"
        dev_notes += "\n"

    if initial_thoughts:
        dev_notes += f"**Initial Thoughts:**\n{initial_thoughts}\n"

    # Add to development notes section
    if "## Development Notes" in story_content:
        story_content = story_content.replace(
            "## Development Notes",
            f"## Development Notes{dev_notes}"
        )

    # Write the story file
    with open(story_file, 'w') as f:
        f.write(story_content)

    console.print(Panel(
        f"[green]✓[/green] Created story development file: [cyan]{filename}[/cyan]\n\n"
        f"[bold]Origin:[/bold] Batch {batch_id}, Concept #{concept_number}\n"
        f"[bold]Title:[/bold] {title}\n"
        f"[bold]Genre:[/bold] {genre}\n\n"
        f"[dim]Next steps:[/dim]\n"
        f"  ./idea-factory review-story {filename}\n"
        f"  ./idea-factory note {filename} \"your ideas here\"",
        title="Story Development File Created",
        box=box.ROUNDED
    ))

    console.print(f"\n[dim]File: {story_file}[/dim]")


@cli.command()
@click.argument('story_name')
@click.option('--section', '-s', help='Show only specific section (e.g., "characters", "plot")')
@click.option('--no-metadata', is_flag=True, help='Hide YAML frontmatter')
def review_story(story_name, section, no_metadata):
    """Review a story development file with beautiful markdown rendering"""
    # Find the story file
    story_file = PROJECT_ROOT / "stories" / f"{story_name}.md"

    if not story_file.exists():
        # Try without extension
        story_file = PROJECT_ROOT / "stories" / story_name
        if not story_file.exists():
            console.print(f"[red]Story '{story_name}' not found[/red]")
            console.print(f"[dim]Looked in: stories/{story_name}.md[/dim]")
            return

    # Read and parse the file
    with open(story_file, 'r') as f:
        content = f.read()

    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter_text = parts[1].strip()
        markdown_content = parts[2].strip()

        # Parse frontmatter for display
        import yaml
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except:
            frontmatter = {}
    else:
        frontmatter = {}
        markdown_content = content

    # Show metadata unless disabled
    if not no_metadata and frontmatter:
        metadata_display = []
        for key in ['title', 'genre', 'status', 'origin_batch', 'date_created', 'date_updated']:
            if key in frontmatter:
                display_key = key.replace('_', ' ').title()
                metadata_display.append(f"[bold cyan]{display_key}:[/bold cyan] {frontmatter[key]}")

        if metadata_display:
            console.print(Panel(
                '\n'.join(metadata_display),
                title="📖 Story Info",
                box=box.ROUNDED
            ))
            console.print()

    # If specific section requested, filter to that
    if section:
        # Try to extract the section
        lines = markdown_content.split('\n')
        section_lines = []
        in_target_section = False
        section_header = f"## {section.title()}"

        for line in lines:
            # Check for section start (case-insensitive)
            if line.lower().startswith(f"## {section.lower()}") or line.lower().startswith(f"### {section.lower()}"):
                in_target_section = True
                section_lines.append(line)
            elif in_target_section:
                # Stop at next major section
                if line.startswith('## ') or line.startswith('# '):
                    break
                section_lines.append(line)

        if section_lines:
            markdown_content = '\n'.join(section_lines)
        else:
            console.print(f"[yellow]Section '{section}' not found in this story[/yellow]")
            return

    # Render the markdown
    md = Markdown(markdown_content)
    console.print(md)

    # Show file path at bottom
    console.print()
    console.print(f"[dim]File: {story_file}[/dim]")


@cli.command()
@click.argument('story_name')
@click.argument('note_text', required=False)
@click.option('--section', '-s', help='Add note to specific section')
def note(story_name, note_text, section):
    """Add a quick note/idea to a story development file"""
    from datetime import datetime

    # Find the story file
    story_file = PROJECT_ROOT / "stories" / f"{story_name}.md"

    if not story_file.exists():
        story_file = PROJECT_ROOT / "stories" / story_name
        if not story_file.exists():
            console.print(f"[red]Story '{story_name}' not found[/red]")
            return

    # If no note text provided, prompt for it
    if not note_text:
        note_text = click.prompt("Note")

    # Read the file
    with open(story_file, 'r') as f:
        content = f.read()

    # Format the note with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_entry = f"\n### [{timestamp}]\n{note_text}\n"

    # If section specified, try to add to that section
    if section:
        # Look for "Development Notes" or specified section
        target_section = f"## {section.title()}"
        if target_section in content:
            # Add note at end of that section
            parts = content.split(target_section)
            if len(parts) > 1:
                # Find the next section
                next_section_idx = parts[1].find('\n## ')
                if next_section_idx != -1:
                    parts[1] = parts[1][:next_section_idx] + note_entry + parts[1][next_section_idx:]
                else:
                    parts[1] += note_entry
                content = target_section.join(parts)
        else:
            console.print(f"[yellow]Section '{section}' not found, adding to Development Notes[/yellow]")
            section = None

    # If no section or section not found, add to Development Notes
    if not section:
        if "## Development Notes" in content:
            content = content.replace("## Development Notes", f"## Development Notes{note_entry}", 1)
        else:
            # Add Development Notes section at the end
            content += f"\n\n## Development Notes{note_entry}"

    # Update the date_updated in frontmatter
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter_text = parts[1]
        # Update or add date_updated
        import yaml
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            frontmatter['date_updated'] = datetime.now().strftime("%Y-%m-%d")
            parts[1] = '\n' + yaml.dump(frontmatter, default_flow_style=False)
            content = '---'.join(parts)
        except:
            pass

    # Write back
    with open(story_file, 'w') as f:
        f.write(content)

    console.print(f"[green]✓[/green] Note added to {story_name}")
    console.print(f"[dim]'{note_text}'[/dim]")


@cli.command()
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def find_similar(interactive):
    """Find similar concepts across batches"""
    from aiwynns.similarity import SimilarityFinder

    finder = SimilarityFinder(db)
    duplicates = finder.find_similar_concepts(threshold=0.8)

    if not duplicates:
        console.print("[green]No similar concepts found[/green]")
        return

    console.print(Panel("🔗 Similar Concepts Found", box=box.DOUBLE))

    for i, (concept1, concept2, score) in enumerate(duplicates, 1):
        console.print(f"\n[bold cyan]{i}. Similarity: {score:.0%}[/bold cyan]")
        console.print(f"   [dim]A:[/dim] {concept1['title']} ({concept1['batch']})")
        console.print(f"   [dim]B:[/dim] {concept2['title']} ({concept2['batch']})")


if __name__ == '__main__':
    cli()
