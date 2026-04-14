import re
import sys

file_path = "c:/Users/User/OneDrive/Desktop/tunog-tuklas/core/templates/core/letrang_o.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update UNIT_NAMES array
old_names = "const UNIT_NAMES = ['Kilalanin Natin', 'Gawain 1', 'Gawain 2', 'Pagsulat', 'Pagsasanay', 'Sagutin Natin'];"
new_names = "const UNIT_NAMES = ['Kilalanin Natin', 'Pagsulat', 'Gawain 2', 'Gawain 1', 'Pagsasanay', 'Sagutin Natin'];"
content = content.replace(old_names, new_names)

# 2. Extract Unit 1 (Gawain 1)
u1_start = content.find("<!-- ═══════════════════════════════════\n             UNIT 2: Gawain 1 – Starting /m/\n        ═══════════════════════════════════ -->")
u2_start = content.find("<!-- ═══════════════════════════════════\n             UNIT 3: Gawain 2 – Ending /m/\n        ═══════════════════════════════════ -->")

u3_start = content.find("<!-- ═══════════════════════════════════\n             UNIT 4: Pagsasanay 1 – Ending Sounds\n        ═══════════════════════════════════ -->")
u4_start = content.find("<!-- ═══════════════════════════════════════════\n             UNIT 5: Pagsasanay 1 at Sagutin Natin\n        ═══════════════════════════════════════════ -->")

if u1_start == -1 or u2_start == -1 or u3_start == -1 or u4_start == -1:
    print("Could not find unit markers. Exiting.")
    sys.exit(1)

unit1_text = content[u1_start:u2_start]
unit3_text = content[u3_start:u4_start]

# 3. Swap text blocks in the content
# We will do index based replacements.
# To be safe, we reconstruct the string
part1 = content[:u1_start]
part_u2 = content[u2_start:u3_start]
part_after_u4 = content[u4_start:]

# Put Unit 3 text where Unit 1 was, and Unit 1 where Unit 3 was.
new_content = part1 + unit3_text + part_u2 + unit1_text + part_after_u4

# 4. Fix IDs inside the swapped text blocks
# Inside unit3_text (which is now Pagsulat, placed at unit-1 position):
# It originally had id="unit-3" and UNIT 4 header.
# Inside unit1_text (which is now Gawain 1, placed at unit-3 position):
# It originally had id="unit-1" and UNIT 2 header.

new_content = new_content.replace('<div class="unit-slide" id="unit-1">', '{{TEMP_U1}}')
new_content = new_content.replace('<div class="unit-slide" id="unit-3">', '<div class="unit-slide" id="unit-1">')
new_content = new_content.replace('{{TEMP_U1}}', '<div class="unit-slide" id="unit-3">')

# 5. Fix Javascript Data-Activity and Check calls for Gawain 1 (now at index 3 -> state 3)
# The new Gawain 1 block has data-activity="1" and checkActivity(1) and feedback-icon-1
new_content = new_content.replace('data-activity="1"', 'data-activity="3"')
new_content = new_content.replace('checkActivity(1)', 'checkActivity(3)')
new_content = new_content.replace('feedback-act1', 'feedback-act3')
new_content = new_content.replace('feedback-icon-1', 'feedback-icon-3')
new_content = new_content.replace('feedback-text-1', 'feedback-text-3')
new_content = new_content.replace('check-act1', 'check-act3')

# 6. Fix Javascript markDone for Pagsulat (now at index 1 -> state 1)
# It used to say: if (... && !state[4].checked) { state[4].checked = true; state[4].score = 1;
# Even though it was buggy, we now map it to state 1
new_content = new_content.replace('!state[4].checked) {\n                    state[4].checked = true;\n                    state[4].score = 1;', '!state[1].checked) {\n                    state[1].checked = true;\n                    state[1].score = 1;')

# Save and write
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Swap operation completed visually. Let's double check.")
