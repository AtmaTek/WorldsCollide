Beta Branch for 1.1.0

Adds the following flags for new features:
1) -bmbs for Kielbasigo's "Shuffle/randomize bosses and statues together"
2) -rec6 for a 6th excluded command
3) -sch for "Steal Rate is improved and rare steals are more likely"
   or 
   -sca for "Steal will always succeed if enemy has an item"
4) -frw for "Removes only the worst flashes from animations. Ex: Learning Bum Rush, Bum Rush, Quadra Slam/Slice, Flash, etc."
   or 
   -frm for "Removes most flashes from animations. Includes Kefka Death."
5) -fc to Fix Capture Bugs (multi-steal not giving more than 1 item and weapon specials not proccing)

Other changes:
- Feature: Magitek is now a -com option (it's 29) and will show up in Random/Random Unique
- Bugfix: Fixes Zozo random clock hints
- Bugfix: Guarantee Enough Unique Dragons to complete objective conditions with random bosses
- Bugfix: Fix win an auction objective condition not completed if auction items not randomized
- QoL: Mt Kolts is peekable -- the shadowy figure will now represent the reward
- Bugfix: Fixed animation bugs with Reflecting Health
- QoL: Once you have 22 coral, every teleporter will take you to chest
- Bugfix: Stats added by objectives will max out at 128, to match Esper reward max and avoid bugs.

Associated PRs:
<https://github.com/AtmaTek/WorldsCollide/pull/10>
<https://github.com/AtmaTek/WorldsCollide/pull/13>
<https://github.com/AtmaTek/WorldsCollide/pull/8>
<https://github.com/AtmaTek/WorldsCollide/pull/3>
<https://github.com/AtmaTek/WorldsCollide/pull/16>
<https://github.com/AtmaTek/WorldsCollide/pull/15>
<https://github.com/AtmaTek/WorldsCollide/pull/17>
<https://github.com/AtmaTek/WorldsCollide/pull/19>
<https://github.com/AtmaTek/WorldsCollide/pull/18>