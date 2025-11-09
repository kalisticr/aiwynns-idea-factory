#!/bin/bash
# Display quick statistics about the idea factory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔════════════════════════════════════════╗"
echo "║   Aiwynn's Idea Factory - Stats       ║"
echo "╚════════════════════════════════════════╝"
echo

# Count batches
TOTAL_BATCHES=$(find "$PROJECT_ROOT/concepts" -name "*.md" 2>/dev/null | wc -l)
GENERATED=$(find "$PROJECT_ROOT/concepts/generated" -name "*.md" 2>/dev/null | wc -l)
DEVELOPING_BATCHES=$(find "$PROJECT_ROOT/concepts/developing" -name "*.md" 2>/dev/null | wc -l)
FAVORITES=$(find "$PROJECT_ROOT/concepts/favorites" -name "*.md" 2>/dev/null | wc -l)

# Count concepts
TOTAL_CONCEPTS=0
for file in "$PROJECT_ROOT"/concepts/*/*.md; do
    if [ -f "$file" ]; then
        COUNT=$(grep "^count:" "$file" | cut -d' ' -f2)
        TOTAL_CONCEPTS=$((TOTAL_CONCEPTS + ${COUNT:-0}))
    fi
done

# Count stories
TOTAL_STORIES=$(find "$PROJECT_ROOT/stories" -name "*.md" 2>/dev/null | wc -l)

# Count by genre (top 5)
echo "📊 BATCHES"
echo "  Total: $TOTAL_BATCHES"
echo "  Generated: $GENERATED"
echo "  Developing: $DEVELOPING_BATCHES"
echo "  Favorites: $FAVORITES"
echo

echo "💡 CONCEPTS"
echo "  Total concepts: $TOTAL_CONCEPTS"
echo

echo "📚 STORIES"
echo "  In development: $TOTAL_STORIES"
echo

echo "🏷️  TOP GENRES"
find "$PROJECT_ROOT/concepts" "$PROJECT_ROOT/stories" -name "*.md" -exec grep "^genre:" {} \; 2>/dev/null | \
    cut -d' ' -f2- | tr -d '[]' | sort | uniq -c | sort -rn | head -5 | \
    while read count genre; do
        echo "  $genre: $count"
    done

echo

echo "🔖 TOP TROPES"
find "$PROJECT_ROOT/concepts" "$PROJECT_ROOT/stories" -name "*.md" -exec grep "^tropes:" {} \; 2>/dev/null | \
    cut -d'[' -f2 | cut -d']' -f1 | tr ',' '\n' | sed 's/^ *//' | sort | uniq -c | sort -rn | head -5 | \
    while read count trope; do
        [ -n "$trope" ] && echo "  $trope: $count"
    done

echo
echo "Last updated: $(date +"%Y-%m-%d %H:%M")"
