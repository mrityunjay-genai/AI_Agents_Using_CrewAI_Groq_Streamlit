from markitdown import MarkItDown

md = MarkItDown()
# Converts the txt file and preserves structural elements
result = md.convert("test.txt")

# Save the markdown content
with open("README.md", "w") as f:
    f.write(result.markdown)
