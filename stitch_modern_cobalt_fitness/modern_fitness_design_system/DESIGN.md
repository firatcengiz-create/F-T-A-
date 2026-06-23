---
name: Modern Fitness Design System
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#434656'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#747688'
  outline-variant: '#c4c5d9'
  surface-tint: '#124af0'
  primary: '#0040e0'
  on-primary: '#ffffff'
  primary-container: '#2e5bff'
  on-primary-container: '#efefff'
  inverse-primary: '#b8c3ff'
  secondary: '#515f7a'
  on-secondary: '#ffffff'
  secondary-container: '#cfddfd'
  on-secondary-container: '#53617d'
  tertiary: '#0d569a'
  on-tertiary: '#ffffff'
  tertiary-container: '#346fb4'
  on-tertiary-container: '#ebf1ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c3ff'
  on-primary-fixed: '#001356'
  on-primary-fixed-variant: '#0035be'
  secondary-fixed: '#d7e2ff'
  secondary-fixed-dim: '#b9c7e6'
  on-secondary-fixed: '#0d1b33'
  on-secondary-fixed-variant: '#394761'
  tertiary-fixed: '#d4e3ff'
  tertiary-fixed-dim: '#a4c8ff'
  on-tertiary-fixed: '#001c39'
  on-tertiary-fixed-variant: '#004784'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Lexend
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Lexend
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Lexend
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.1px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.5px
  headline-lg-mobile:
    fontFamily: Lexend
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  margin-mobile: 20px
  margin-desktop: 64px
  gutter: 16px
---

## Brand & Style
The brand personality is **authoritative, high-performance, and revitalizing**. This design system bridges the gap between clinical fitness data and the energetic lifestyle of a tech-forward athlete. It avoids the aggressive, dark aesthetics of traditional "gym" apps, instead opting for a crisp, "breathable" interface that mirrors the clarity of a fresh start.

The design style is **Corporate Modern with a Tech-Startup edge**, heavily influenced by **Material Design 3**. It utilizes expansive white space to reduce cognitive load during intense workouts. The aesthetic is defined by its mathematical precision, soft tonal depth, and a "motivational airy" quality achieved through generous padding and vibrant accent pops.

## Colors
The palette is rooted in a monochromatic blue spectrum to maintain professional focus and trust.

- **Primary (Electric Cobalt):** Used for primary actions, active progress indicators, and key brand moments. It is high-vibrancy to ensure visibility and energy.
- **Secondary (Navy & Sky):** Navy is reserved for high-contrast typography and deep backgrounds; Sky Blue is used for "subtle" interactive states and secondary data visualizations.
- **Backgrounds:** The primary surface is a pure White (#FFFFFF). Surfaces requiring separation use a very soft Slate Gray (#F8FAFC) to maintain the airy feel.
- **Data Visualization:** Charts use a gradient ramp from Navy through Cobalt to Sky Blue to represent intensity or progress layers.

## Typography
This design system utilizes **Lexend** for headings to leverage its athletic, highly readable, and modern geometric character. **Inter** is used for all functional body text and UI labels due to its neutral, systematic clarity.

Headlines should use tighter letter spacing for a punchy, editorial feel. Data points (like weights or durations) should always use the `headline-md` or `display-lg` roles to ensure they are glanceable during physical activity.

## Layout & Spacing
The layout follows a **fluid grid** model optimized for high-speed interaction. On mobile, a 4-column grid with 20px margins is standard. On desktop, a 12-column grid is used with a maximum content container of 1280px.

A strict **8px spacing scale** ensures rhythmic consistency. Generous padding (minimum 24px) is applied within cards to maintain the "airy" brand promise. Vertical rhythm should prioritize large "breathing rooms" between distinct content sections to avoid visual clutter during high-intensity use.

## Elevation & Depth
Depth is communicated through **ambient shadows** and **tonal layering**, moving away from harsh borders.

- **Level 0 (Base):** Pure white background.
- **Level 1 (Cards):** Resting state cards use a very soft, diffused shadow (Blur: 15px, Y: 4px, Color: Navy @ 4% opacity) to appear slightly lifted.
- **Level 2 (Active/Interactive):** Elements that are being interacted with or require immediate attention (like a timer) use a more pronounced, "glow" shadow using a tinted Electric Cobalt at 10% opacity.
- **Backdrop blurs:** Used sparingly on navigation bars and overlays to maintain context while focusing the user on a specific task.

## Shapes
In alignment with Material Design 3 and a friendly "tech-startup" look, this design system uses an **aggressive corner radius**. 

- **Primary Containers (Cards):** Use `rounded-2xl` (1.5rem / 24px) to feel soft and approachable.
- **Interactive Elements (Buttons/Inputs):** Use `rounded-xl` (0.75rem / 12px) to provide a distinct but related aesthetic.
- **Circular Elements:** Progress rings and profile avatars are always fully circular (50% radius).

## Components
- **Buttons:** Primary buttons are solid Electric Cobalt with white text. Secondary buttons use a Sky Blue ghost style (transparent fill, subtle border).
- **Cards:** The foundation of the UI. They should have a White background and the defined Level 1 shadow. Group related data (e.g., Heart Rate + Steps) into single cards with internal dividers.
- **Circular Progress Rings:** Use a thick stroke (8px-12px) with a rounded cap. Background tracks should be a 10% opacity version of the progress color.
- **Charts:** Line charts must use smooth cubic interpolation (not jagged lines). Bar charts should have rounded tops. Use Navy for axes and Electric Cobalt for the primary data series.
- **Chips:** Small, pill-shaped indicators for workout categories (e.g., "HIIT", "Yoga"). Use Sky Blue backgrounds with Navy text.
- **Input Fields:** Minimalist design with a soft Slate Gray fill and a 2px Electric Cobalt bottom border on focus.