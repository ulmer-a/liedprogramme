#! /bin/bash

cat head.md > index.md
python3 gen_markdown.py >> index.md
echo >> index.md
echo "Dem höchsten Gott allein zu Ehren. Letze Aktualisierung: $(date)" >> index.md

markdown index.md >> www/index.html
echo "</body></html>" >> www/index.html