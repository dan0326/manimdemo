# Repository Instructions

## Manim scene style

- Write scene construction in a chronological, notebook-like order.
- Add a short comment before each visual section explaining what that section does.
- Initialize and configure an object close to the `self.add(...)` or `self.play(...)` call that first puts it on screen or animates it.
- Avoid collecting most object definitions at the top of `construct()` when they are not used until much later.
- Keep related setup, animation, and brief waits together so the file reads in the same order as the rendered scene.
- When reorganizing an existing scene for style, preserve its objects, calculations, animation order, timing, and rendered behavior unless the user explicitly requests functional changes.
- Use the user-authored files in `geometry/` as style references, especially their simple section comments and sequential flow.
