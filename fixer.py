import glob

files = glob.glob('core/templates/core/letrang_*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's use regex to find the broken line and replace it exactly
    import re
    # Match any mctx.font assignment inside validateDrawing block that looks mangled
    fixed_line = "mctx.font = `${comp.fontWeight} ${comp.fontSize} ${comp.fontFamily}`;"
    
    # Let's replace the whole assignment
    new_content = re.sub(
        r'mctx\.font\s*=\s*[^\n]+;',
        fixed_line,
        content
    )
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Fixed {file}')
