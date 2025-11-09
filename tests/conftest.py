"""
Pytest configuration and shared fixtures
"""

import pytest
from pathlib import Path
from datetime import datetime


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace with proper directory structure"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()

    # Create directory structure
    (workspace / "concepts" / "generated").mkdir(parents=True)
    (workspace / "concepts" / "developing").mkdir(parents=True)
    (workspace / "concepts" / "favorites").mkdir(parents=True)
    (workspace / "stories").mkdir(parents=True)
    (workspace / "templates").mkdir(parents=True)
    (workspace / "resources").mkdir(parents=True)

    return workspace


@pytest.fixture
def sample_batch_content():
    """Sample batch file content with valid frontmatter"""
    return """---
batch_id: 20250101-001
date_generated: 2025-01-01
genre: Fantasy
tropes: magic, adventure, chosen one
count: 3
status: generated
llm_model: Claude Sonnet 4.5
prompt_used: Generate fantasy concepts
---

# Test Batch

## Concept 1: The Magic Sword
**High Concept**: A young hero discovers a magical sword

**Synopsis**: This is a test synopsis for concept 1.

**Key Elements**:
- Magic sword
- Young hero
- Epic quest

---

## Concept 2: The Dark Forest
**High Concept**: Adventurers must traverse a haunted forest

**Synopsis**: This is a test synopsis for concept 2.

**Key Elements**:
- Dark forest
- Haunted creatures
- Teamwork

---

## Concept 3: The Lost Kingdom
**High Concept**: Archaeologists discover ancient ruins

**Synopsis**: This is a test synopsis for concept 3.

**Key Elements**:
- Ancient ruins
- Lost civilization
- Mystery
"""


@pytest.fixture
def sample_story_content():
    """Sample story file content with valid frontmatter"""
    return """---
story_id: test-story-001
title: Test Story
genre: Fantasy
subgenre: Epic Fantasy
tropes: [chosen one, magic academy]
status: developing
origin_batch: 20250101-001
date_created: 2025-01-01
date_updated: 2025-01-01
target_length: novel
---

# Test Story

## High Concept
A test high concept for testing

## Logline
This is a test logline for testing purposes.

## Extended Synopsis
This is an extended synopsis for testing.

## Development Notes
Test notes here.
"""


@pytest.fixture
def invalid_yaml_content():
    """Content with invalid YAML frontmatter"""
    return """---
batch_id: test
invalid: yaml: syntax: here
more: bad: yaml
---

# Content
"""


@pytest.fixture
def mock_templates(temp_workspace):
    """Create mock template files"""
    templates_dir = temp_workspace / "templates"

    # Batch template
    batch_template = templates_dir / "concept-batch.md"
    batch_template.write_text("""---
batch_id: YYYYMMDD-001
date_generated: YYYY-MM-DD
genre: [genre]
tropes: [trope1, trope2, trope3]
count: 10
status: generated
llm_model: "model used"
---

# Batch Template
""")

    # Story template
    story_template = templates_dir / "story-development.md"
    story_template.write_text("""---
story_id: [unique-id]
title: [Working Title]
genre: [genre]
status: developing
origin_batch: [batch_id if from generated concepts]
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---

# [Story Title]

## High Concept
[One-line pitch]

## Logline
[2-3 sentence description]
""")

    return templates_dir
