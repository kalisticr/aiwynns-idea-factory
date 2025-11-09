#!/bin/bash
# Search through all concepts and stories

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <search-term> [options]"
    echo
    echo "Options:"
    echo "  -g, --genre <genre>     Filter by genre"
    echo "  -t, --trope <trope>     Filter by trope"
    echo "  -s, --status <status>   Filter by status"
    echo
    echo "Examples:"
    echo "  $0 'enemies to lovers'"
    echo "  $0 -g fantasy -t 'chosen one'"
    echo "  $0 'magic' -s developing"
    exit 1
fi

SEARCH_TERM="$1"
shift

GENRE_FILTER=""
TROPE_FILTER=""
STATUS_FILTER=""

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--genre)
            GENRE_FILTER="$2"
            shift 2
            ;;
        -t|--trope)
            TROPE_FILTER="$2"
            shift 2
            ;;
        -s|--status)
            STATUS_FILTER="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "=== Searching for: '$SEARCH_TERM' ==="
[ -n "$GENRE_FILTER" ] && echo "Genre filter: $GENRE_FILTER"
[ -n "$TROPE_FILTER" ] && echo "Trope filter: $TROPE_FILTER"
[ -n "$STATUS_FILTER" ] && echo "Status filter: $STATUS_FILTER"
echo

RESULTS=0

# Search in concepts
for file in "$PROJECT_ROOT"/concepts/*/*.md; do
    if [ -f "$file" ]; then
        # Apply filters
        if [ -n "$GENRE_FILTER" ]; then
            grep -q "genre:.*$GENRE_FILTER" "$file" || continue
        fi
        if [ -n "$TROPE_FILTER" ]; then
            grep -q "tropes:.*$TROPE_FILTER" "$file" || continue
        fi
        if [ -n "$STATUS_FILTER" ]; then
            grep -q "status:.*$STATUS_FILTER" "$file" || continue
        fi

        # Search for term
        if grep -qi "$SEARCH_TERM" "$file"; then
            RESULTS=$((RESULTS + 1))
            BATCH_ID=$(grep "^batch_id:" "$file" | cut -d' ' -f2)
            GENRE=$(grep "^genre:" "$file" | cut -d' ' -f2- | tr -d '[]')

            echo "[$BATCH_ID] $GENRE"
            echo "File: $file"
            echo
            # Show matching lines with context
            grep -ni -C 1 "$SEARCH_TERM" "$file" | head -20
            echo
            echo "---"
            echo
        fi
    fi
done

# Search in stories
for file in "$PROJECT_ROOT"/stories/*.md; do
    if [ -f "$file" ]; then
        if grep -qi "$SEARCH_TERM" "$file"; then
            RESULTS=$((RESULTS + 1))
            TITLE=$(grep "^title:" "$file" | cut -d' ' -f2-)
            GENRE=$(grep "^genre:" "$file" | cut -d' ' -f2-)

            echo "[STORY] $TITLE - $GENRE"
            echo "File: $file"
            echo
            grep -ni -C 1 "$SEARCH_TERM" "$file" | head -20
            echo
            echo "---"
            echo
        fi
    fi
done

echo "Total results: $RESULTS"
