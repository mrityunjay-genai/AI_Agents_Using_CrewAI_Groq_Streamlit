from markitdown import MarkItDown

md = MarkItDown()
# Converts the txt file and preserves structural elements
result = md.convert("dockerfile_explanation.txt")

# Save the markdown content
with open("output.md", "w") as f:
    f.write(result.markdown)
