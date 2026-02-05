---
name: feature-darkmode
description: Use this prompt when you want the Designer Agent to implement a theme toggler (Dark Mode) that respects accessibility and brand guidelines.
---
# Feature Request: High Contrast Dark Mode

**Context:**
To improve accessibility and reduce eye strain for students studying late, we need a Dark Mode toggle.

**Task:**
Implement a theme toggler in the website header.

**Requirements:**
1.  **HTML (`src/static/index.html`):**
    * Add a toggle button inside the `<header>` element.
    * Use a simple emoji (🌙/☀️) or icon for the button content.
    * Ensure the button is accessible via keyboard navigation.

2.  **CSS (`src/static/styles.css`):**
    * Define a `.dark-mode` class for the `body`.
    * **Color Palette:**
        * Background: Dark gray (e.g., `#121212`) instead of `#f5f5f5`.
        * Text: White or off-white (`#e0e0e0`).
        * Header: Keep the branding, but maybe darken the blue `#1a237e` slightly or add a lighter border for contrast.
        * Activity Cards: Change background from `#f9f9f9` to a dark card color (e.g., `#1e1e1e`) with a subtle light border.
    * Ensure the blue links and buttons (`#1a237e`, `#0066cc`) are adjusted to a lighter shade (e.g., `#5c6bc0`) in dark mode to pass WCAG contrast ratios against the dark background.

3.  **JavaScript (`src/static/app.js`):**
    * Add logic to toggle the `.dark-mode` class on the `body` when the button is clicked.
    * (Optional) Save the user's preference in `localStorage`.

**Design Note:**
The transition between modes should be smooth. Verify that the "Participants" section inside cards remains readable in dark mode.