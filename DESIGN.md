# Hualien Kitchen — Design Reference

## Brand Concept: "Taroko Entrance"
The visual identity draws from Hualien's landscape — deep forest green of the gorge,
warm cream like sunlit marble, gold like late-afternoon light on stone.

## Color Palette
| Token         | Value     | Usage                          |
|---------------|-----------|--------------------------------|
| `--green`     | `#2a5c45` | Primary brand, buttons, header |
| `--green-light`| `#3a7d60` | Hover states                   |
| `--green-pale`| `#eaf2ed` | Backgrounds, selected states   |
| `--gold`      | `#c8a057` | Accents, prices, labels        |
| `--bg`        | `#f7f5f0` | Page background (menu/admin)   |
| `--card`      | `#ffffff` | Card surfaces                  |
| `--text`      | `#1c1c1c` | Body text                      |
| `--muted`     | `#7a7a7a` | Secondary text                 |
| `--border`    | `#e8e3d8` | Dividers, input borders        |

**Landing page only** uses a dark variant: `#0c1f13` bg + `#f2e8d0` text.

## Typography
- **Display (landing)**: Cormorant Garamond — italic for the name, wide-spaced uppercase for the category word
- **UI (menu/admin)**: System sans-serif stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI'…`)

## Page Hierarchy
| Page        | Mood            | Background  | Font stack     |
|-------------|-----------------|-------------|----------------|
| Landing `/` | Atmospheric     | Dark green  | Cormorant + Montserrat |
| Menu `/menu`| Clean, bright   | `--bg` cream | System sans   |
| Admin       | Functional      | `--bg` cream | System sans   |

## Key Design Decisions
- **Landing ≠ Menu**: The entrance page uses a dark theme to create contrast and drama. Arriving at the menu (bright, airy) feels like "opening the door."
- **CSS class names are stable**: Never rename classes from the static prototype — Alpine.js depends on them.
- **Buttons**: Pill-shaped in the menu UI; rectangular with slide-fill hover on the landing page.
- **Chinese text**: Used as watermark on landing (`opacity ~0.02`) and as `item-name-sub` label in menu cards (`--gold` color).
