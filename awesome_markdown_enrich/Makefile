all:
	./get_info.sh README.md > info.csv
	./sort_file.sh info.csv > sorted.csv
	./to_markdown.py sorted.csv > info.md
