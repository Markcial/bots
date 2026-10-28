# Brand book: <Brand name>

Status: `draft` | `approved <date>`   Version: 1   Updated: <date>
Machine copy: `brand/<slug>/brand.json` (the bot reads and checks this one). Memory note: `brand-book-<slug>`.

Only the owner's explicit OK changes anything below. Every change gets a line in the change log.

## 1. Idea in one line
What the brand is for, who it speaks to, and the one feeling a piece should leave. Source: the approved diagnosis `diagnosis-<project-slug>`.

## 2. Colour
| Token | Hex | Role |
| --- | --- | --- |
| primary | `#` | main brand colour |
| accent | `#` | secondary, never body text |
| background | `#` | default canvas |
| ink | `#` | text |
| surface | `#` | cards and panels |

Contrast pairs (ratio measured by `node scripts/brand-check.mjs`): ink on background (4.5 or more), primary on background (3 or more), ink on surface (4.5 or more), text on primary (4.5 or more).

## 3. Type
| Use | Family | Weight | Licence | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| Headings | | | SIL OFL or Apache-2.0 | | |
| Body | | | | | |

## 4. Logo and avatar
Master file, minimum size (px), clear space, allowed backgrounds, and the sizes exported. Original files only.

## 5. Voice and tone
Tone in one line, words to use, words to avoid, and spoken respellings (voice text only, never in captions).

## 6. Motion
Formats, frame rate, easing, pacing, caption rules, music and loudness.

## 7. Do and don't
Short lists. Each line is checkable.

## 8. References
What the owner likes and dislikes, with a link and a reason.

## 9. Change log
| Date | Change | Approved by |
| --- | --- | --- |
