---
name: feature-searchbar
description: Use this prompt when you want the Designer Agent to implement a real-time filtering mechanism for the activities list on the frontend.
---
# Feature Request: Real-time Activity Search Bar

**Context:**
We need to improve the user experience by allowing students to quickly find activities without scrolling through the entire list.

**Task:**
Implement a real-time search filter for the activities list.

**Requirements:**
1.  **HTML (`src/static/index.html`):**
    * Add a search input field immediately above the `#activities-list` container.
    * Use an accessible label or `aria-label="Search activities"`.
    * Add a placeholder text: "Search for clubs, sports..."

2.  **CSS (`src/static/styles.css`):**
    * Style the input to match the "Mergington High" brand identity. Use the same border-radius (4px) and padding as existing inputs.
    * Ensure the input has a focus state using the primary school color (`#1a237e`) for the border.

3.  **JavaScript (`src/static/app.js`):**
    * Add an event listener to the search input.
    * Filter the `.activity-card` elements in real-time based on their title (`h4`) or description (`p`).
    * If no matches are found, display a user-friendly message "No activities found" in the list container.

**Design Note:**
Ensure the new search bar looks integrated with the existing design and works well on mobile devices.