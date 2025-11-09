#!/bin/bash
# Create a new concept batch from template

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATE="$PROJECT_ROOT/templates/concept-batch.md"
CONCEPTS_DIR="$PROJECT_ROOT/concepts/generated"

# Get today's date
TODAY=$(date +%Y%m%d)

# Find next batch number for today
BATCH_NUM=1
while [ -f "$CONCEPTS_DIR/${TODAY}-$(printf '%03d' $BATCH_NUM).md" ]; do
    BATCH_NUM=$((BATCH_NUM + 1))
done

BATCH_ID="${TODAY}-$(printf '%03d' $BATCH_NUM)"
NEW_FILE="$CONCEPTS_DIR/${BATCH_ID}.md"

# Prompt for basic info
echo "=== Creating New Concept Batch ==="
echo
read -p "Genre: " GENRE
read -p "Tropes (comma-separated): " TROPES
read -p "LLM Model used (e.g., GPT-4, Claude): " MODEL
read -p "Number of concepts [10]: " COUNT
COUNT=${COUNT:-10}

# Copy template and replace placeholders
cp "$TEMPLATE" "$NEW_FILE"

# Use sed to replace placeholders
sed -i "s/YYYYMMDD-001/$BATCH_ID/" "$NEW_FILE"
sed -i "s/YYYY-MM-DD/$(date +%Y-%m-%d)/" "$NEW_FILE"
sed -i "s/\[genre\]/$GENRE/g" "$NEW_FILE"
sed -i "s/\[trope1, trope2, trope3\]/$TROPES/" "$NEW_FILE"
sed -i "s/count: 10/count: $COUNT/" "$NEW_FILE"
sed -i "s/\"model used\"/\"$MODEL\"/" "$NEW_FILE"

echo
echo "✓ Created: $NEW_FILE"
echo
echo "Next steps:"
echo "1. Open the file in your editor"
echo "2. Paste your LLM prompt in the frontmatter"
echo "3. Fill in the generated concepts"
echo "4. Run './scripts/update-index.sh' when done"
echo
echo "Opening file..."

# Open in default editor or just show path
${EDITOR:-nano} "$NEW_FILE"
