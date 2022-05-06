Beta Branch for 1.1.x

Adds the following flags for new features:
1. `-stloc/-drloc <original | shuffle | mix>` for Kielbasigo's Status Boss Location, Dragon Boss Location shuffle or mix. Shuffle = shuffled amongst themselves, Mix = mixed boss pool
2. `-fc` to Fix Capture Bugs (multi-steal not giving more than 1 item and weapon specials not proccing)
3. `-np` flag for Sprites in peekable checks are left a mystery until reward
4. `-cc` flag for Controllable Coliseum
5. Kielbasiago's movement options: 
- `-noshoes` flag for "Removes Sprint Shoes from appearing in shops, chests, etc."
- `--move og | as | bd | ssbd` for Movement Speed (MS) changes:
        Original -- MS 2 by default, MS 3 with sprint shoes | 
        Auto Sprint (new default, equivalent to deprecated `-as` flag) -- MS 3 by default, MS 2 when holding B | 
        B Dash -- MS 3 by default, MS 4 when holding B | 
        Sprint Shoes B Dash -- MS 3 by default, MS 2 when holding B, MS 4 when holding B with sprint shoes
6. `-rls` flag for "Remove spells from learnable sources: Items, Espers, Natural Magic, and Objectives"
7. `-scis` flag for "Sketch & Control 100% accurate and use Sketcher/Controller's stats"
8. `-scia` flag for "Improves Sketch & Control abilities. Removes Battle from Sketch. Adds Rage as a Sketch/Control possibility for most monsters. Gives Sketch abilities to most bosses."
9. `-stesp <MIN> <MAX>` for "Give Player between MIN - MAX espers at the start of the seed
10. `-wmhc` for "World Minimap High Contrast -- makes minimap opaque and increases contrast of location indicator"

Other changes:
- QoL: Mt Kolts is peekable -- the shadowy figure will now represent the reward
- QoL: Once you have 22 coral, every teleporter will take you to chest
- Feature: The Top 4 Magitek default to disabled for all characters, and are now unlockable for an objective (result = 59, "Magitek Upgrade")
- Bugfix: Learn Spells reward can no longer give Life spells during permadeath seeds.
- Feature: Added Gau-Father Reunion as a Quest objective (objective string ends with `.12.10`). Hint: take Gau + Sabin to Gau's Father House in WoR.
- Bugfix: Fixing bug that prevented learning Bum Rush if the Blitzer was recruited at level >= 42

Associated PRs:
- <https://github.com/AtmaTek/WorldsCollide/pull/35>
- <https://github.com/AtmaTek/WorldsCollide/pull/16>
- <https://github.com/AtmaTek/WorldsCollide/pull/15>
- <https://github.com/AtmaTek/WorldsCollide/pull/18>
- <https://github.com/AtmaTek/WorldsCollide/pull/21>
- <https://github.com/AtmaTek/WorldsCollide/pull/25>
- <https://github.com/AtmaTek/WorldsCollide/pull/28>
- <https://github.com/AtmaTek/WorldsCollide/pull/30>
- <https://github.com/AtmaTek/WorldsCollide/pull/32>
- <https://github.com/AtmaTek/WorldsCollide/pull/34>
- <https://github.com/AtmaTek/WorldsCollide/pull/36>
- <https://github.com/AtmaTek/WorldsCollide/pull/37>


