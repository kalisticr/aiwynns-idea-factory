#!/bin/bash
# List all concept batches with metadata

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONCEPTS_DIR="$PROJECT_ROOT/concepts"

echo "=== Story Concept Batches ==="
echo

TOTAL=0

for dir in "$CONCEPTS_DIR"/*; do
    if [ -d "$dir" ]; then
        SECTION=$(basename "$dir")
        echo "[$SECTION]"
        echo

        for file in "$dir"/*.md; do
            if [ -f "$file" ]; then
                TOTAL=$((TOTAL + 1))

                # Extract metadata from frontmatter
                BATCH_ID=$(grep "^batch_id:" "$file" | cut -d' ' -f2)
                GENRE=$(grep "^genre:" "$file" | cut -d' ' -f2- | tr -d '[]')
                DATE=$(grep "^date_generated:" "$file" | cut -d' ' -f2)
                COUNT=$(grep "^count:" "$file" | cut -d' ' -f2)
                STATUS=$(grep "^status:" "$file" | cut -d' ' -f2)

                echo "  $BATCH_ID | $DATE | $GENRE"
                echo "    Count: $COUNT | Status: $STATUS"
                echo "    File: $(basename "$file")"
                echo
            fi
        done
    fi
done

echo "---"
echo "Total batches: $TOTAL"

# Count stories in development
STORY_COUNT=$(find "$PROJECT_ROOT/stories" -name "*.md" 2>/dev/null | wc -l)
echo "Stories in development: $STORY_COUNT"
