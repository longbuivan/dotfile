import os
import re
"""

This script consolidates all markdown files in a repository into a single markdown file.
It extracts headers from each file, adjusts their levels, and writes them into a new file.
This script consolidates all markdown files in a repository into a single markdown file.
Use the consolidated markdown file as input for LLM to generate the Knowledge Graph.

Usage: https://www.longdatadevlog.com/brain/knowledge-graph-brain/
"""
# Define the repository root and output file
repo_root = "./"  # Change this to your repo's root if running from elsewhere
output_file = "longddl_wiki.md"

def extract_headers(content):
    """Extract headers from markdown content and adjust levels"""
    lines = content.split("\n")
    updated_lines = []
    for line in lines:
        match = re.match(r"^(#{1,6})\s*(.*)", line)
        if match:
            level, text = match.groups()
            adjusted_level = "#" * (len(level) + 1)  # Shift headers by 1 level
            updated_lines.append(f"{adjusted_level} {text}")
        else:
            updated_lines.append(line)
    return "\n".join(updated_lines)

def consolidate_markdown(repo_root, output_file):
    with open(output_file, "w", encoding="utf-8") as out_file:
        for root, _, files in os.walk(repo_root):
            for file in sorted(files):
                if file.endswith(".md") and file != output_file:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as md_file:
                        content = md_file.read()

                    # Write file name as header
                    out_file.write(f"# {file}\n\n")
                    out_file.write(extract_headers(content))
                    out_file.write("\n\n---\n\n")  # Separator between files

if __name__ == "__main__":
    print("Processing to collecting file")
    consolidate_markdown(repo_root, output_file)
    print(f"Consolidated markdown saved to {output_file}")
