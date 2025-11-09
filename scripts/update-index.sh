#!/bin/bash
# Update the INDEX.md file with current concepts and stories

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INDEX_FILE="$PROJECT_ROOT/INDEX.md"
CONCEPTS_DIR="$PROJECT_ROOT/concepts"
STORIES_DIR="$PROJECT_ROOT/stories"

echo "Updating index..."

# Count statistics
TOTAL_BATCHES=0
TOTAL_CONCEPTS=0
IN_DEVELOPMENT=0
TOTAL_STORIES=0

# Start building new index content
INDEX_CONTENT="# Story Concepts Index

This file tracks all story concepts in the database. Last updated: $(date +"%Y-%m-%d %H:%M")

"

# Calculate statistics
for file in "$CONCEPTS_DIR"/*/*.md; do
    if [ -f "$file" ]; then
        TOTAL_BATCHES=$((TOTAL_BATCHES + 1))
        COUNT=$(grep "^count:" "$file" | cut -d' ' -f2)
        TOTAL_CONCEPTS=$((TOTAL_CONCEPTS + ${COUNT:-0}))
    fi
done

TOTAL_STORIES=$(find "$STORIES_DIR" -name "*.md" 2>/dev/null | wc -l)
IN_DEVELOPMENT=$(grep -l "status: developing" "$STORIES_DIR"/*.md 2>/dev/null | wc -l)

INDEX_CONTENT+="## Statistics
- Total Batches: $TOTAL_BATCHES
- Total Concepts: $TOTAL_CONCEPTS
- Stories in Development: $IN_DEVELOPMENT
- Total Stories: $TOTAL_STORIES

---

## Concept Batches

"

# List all batches
for dir in "$CONCEPTS_DIR"/*; do
    if [ -d "$dir" ]; then
        SECTION=$(basename "$dir")
        INDEX_CONTENT+="### $(echo $SECTION | tr '[:lower:]' '[:upper:]')

"
        for file in "$dir"/*.md; do
            if [ -f "$file" ]; then
                BATCH_ID=$(grep "^batch_id:" "$file" | cut -d' ' -f2)
                GENRE=$(grep "^genre:" "$file" | cut -d' ' -f2- | tr -d '[]')
                DATE=$(grep "^date_generated:" "$file" | cut -d' ' -f2)
                COUNT=$(grep "^count:" "$file" | cut -d' ' -f2)

                RELPATH=$(realpath --relative-to="$PROJECT_ROOT" "$file")
                INDEX_CONTENT+="- **[$BATCH_ID]** $GENRE ($COUNT concepts) - $DATE - \`$RELPATH\`
"
            fi
        done
        INDEX_CONTENT+="
"
    fi
done

INDEX_CONTENT+="---

## Stories in Development

"

# List all stories
for file in "$STORIES_DIR"/*.md; do
    if [ -f "$file" ]; then
        TITLE=$(grep "^title:" "$file" | cut -d' ' -f2-)
        GENRE=$(grep "^genre:" "$file" | cut -d' ' -f2-)
        STATUS=$(grep "^status:" "$file" | cut -d' ' -f2)
        TROPES=$(grep "^tropes:" "$file" | cut -d' ' -f2- | tr -d '[]')

        RELPATH=$(realpath --relative-to="$PROJECT_ROOT" "$file")
        INDEX_CONTENT+="- **$TITLE** [$STATUS]
  - Genre: $GENRE
  - Tropes: $TROPES
  - File: \`$RELPATH\`

"
    fi
done

INDEX_CONTENT+="---

## Manual Updates
You can manually add notes and cross-references below this line.

"

# Write the index file
echo "$INDEX_CONTENT" > "$INDEX_FILE"

echo "✓ Index updated successfully!"
echo "  - $TOTAL_BATCHES batches"
echo "  - $TOTAL_CONCEPTS total concepts"
echo "  - $TOTAL_STORIES stories tracked"
