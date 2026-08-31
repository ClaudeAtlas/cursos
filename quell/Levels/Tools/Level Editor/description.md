# Level |Editor

With this program you can edit your own Quell levels.
Before running the program, you must edit the Gobstones board, in order for it to have enough 
room for your level (plus 1 row for the top bar).

During edition, you may use the arrow keys to move around the Quell board zone, and add Quell 
elements to individual cells.
Some QElements require additional information to be completed. Movement can only occur when 
the edition of the current QElement is completed (or aborted).

When you think you have finishing editing your level, you need to verify it, to be sure that everything
will work fine. After validation, you save the Gobstones board using the menu on the left, and use the
board in your own level. The keys that draw QElements only can draw them if the current cell is Empty 
(with a few exceptions).

The keys to edit are the following:
  * arrow keys - move around Quell board (if current QElement is completed)
  * `ESC` - abort an incomplete edition of a QElement
  * `DEL` - clear the current cell, restoring the Empty QEelement
  * `ENTER` (or `V`) - verify the current level
  * `1` - Draw a Portal A  
  * `2` - Draw a Portal B
  * `B` - Draw a QBall
  * `D` - Edit TopSpikesDir (needs completion with arrow keys)
  * `G` - Draw an open Gate
  * `J` - Draw a Jewel (can work on Walls as well)
  * `K` - Edit a Spike (needs completiong with arrow keys)
  * `L` - Draw a boundary (after verification, they become straight Limits, Angles or Corners, accordingly to their positions)
  * `M` - Draw a Multispike
  * `P` - Draw a Pearl
  * `R` - Draw a RotableSpike (its direction is the last inserted TopSpikesDir, or North by default)
  * `S` - Draw a Switch (its direction is the last inserted TopSpikesDir, or North by default)
  * `W` - Draw a Wall (can work on a Jewel as well)
  * `X` - Edit a Box (needs completion with `F` or `M` keys)

Validation of the level verifies several conditions:
  - there can be exactly one Ball
  - there can be at most one Jewel
  - boundaries must delimit one or more areas, surrounding them in continuous "lines" of cells
  - all QElements must be inside one delimited area
After a successful validation, boundaries are transformed into Limits, Angles, or Corners, accordingly to their positions, 
and all cells not inside an area delimited by those is transformed into Out.

Once you have your level validated, you must save the Gobstones board, and later use that board to generate an activity 
with the level using the template.

