#!/bin/bash
# Create a new story development file from template

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATE="$PROJECT_ROOT/templates/story-development.md"
STORIES_DIR="$PROJECT_ROOT/stories"

echo "=== Creating New Story Development File ==="
echo

read -p "Working title: " TITLE
read -p "Genre: " GENRE
read -p "Origin batch ID (if any): " ORIGIN

# Create a filename from title (lowercase, hyphens)
FILENAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')
STORY_ID="${FILENAME}-$(date +%s)"
NEW_FILE="$STORIES_DIR/${FILENAME}.md"

# Check if file exists
if [ -f "$NEW_FILE" ]; then
    echo "Warning: File already exists. Adding timestamp..."
    NEW_FILE="$STORIES_DIR/${FILENAME}-$(date +%Y%m%d).md"
fi

# Copy template and replace placeholders
cp "$TEMPLATE" "$NEW_FILE"

sed -i "s/\[unique-id\]/$STORY_ID/" "$NEW_FILE"
sed -i "s/\[Working Title\]/$TITLE/" "$NEW_FILE"
sed -i "s/\[Story Title\]/$TITLE/" "$NEW_FILE"
sed -i "s/\[genre\]/$GENRE/" "$NEW_FILE"
sed -i "s/\[batch_id if from generated concepts\]/${ORIGIN:-none}/" "$NEW_FILE"
sed -i "s/YYYY-MM-DD/$(date +%Y-%m-%d)/g" "$NEW_FILE"

echo
echo "✓ Created: $NEW_FILE"
echo
echo "Story ID: $STORY_ID"
echo
echo "Opening file..."

${EDITOR:-nano} "$NEW_FILE"
