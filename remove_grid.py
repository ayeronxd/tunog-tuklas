import re
import os

files = [
    r"c:\Users\User\OneDrive\Desktop\tunog-tuklas\core\templates\core\letrang_b.html",
    r"c:\Users\User\OneDrive\Desktop\tunog-tuklas\core\templates\core\letrang_i.html",
    r"c:\Users\User\OneDrive\Desktop\tunog-tuklas\core\templates\core\letrang_m.html",
    r"c:\Users\User\OneDrive\Desktop\tunog-tuklas\core\templates\core\letrang_o.html"
]

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Regex to remove .canvas-frame::before and its block
        new_content = re.sub(
            r"([ \t]*/\* Ruled lines drawn via CSS pseudo \+ repeating gradient \*/\s*\.canvas-frame::before \{.*?\})",
            "",
            content,
            flags=re.DOTALL
        )
        
        # If the comment is slightly different, let's just use .canvas-frame::before { ... }
        if new_content == content:
             new_content = re.sub(
                 r"([ \t]*\.canvas-frame::before\s*\{.*?\})",
                 "",
                 content,
                 flags=re.DOTALL
             )

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filepath}")
        else:
            print(f"No match found in {filepath}")
