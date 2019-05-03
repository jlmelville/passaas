set -e

coveralls || echo "Coveralls upload failed"
