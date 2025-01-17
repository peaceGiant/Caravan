# Tasks
## Title Screen
- [ ] Add PvP mode. (Pece)
  - new state designed for player vs player game.
- [ ] opt. Add smarter player AI agent.
  - new state.
- [ ] opt. Add Tutorial mode. (Luka)
  - new state.
  - adds helper text what the player should do next.
  - adds clarifying text whenever the player attempts an impossible move.
- [ ] opt. Tooltip card animation.
  - on title screen - display card rotating animation along with text providing helpful tips.
  - after a certain time period, change to a different card.
- [ ] Improve graphics. (Luka)
  - change background.
  - improve title dancing animation.
  - improve buttons (or completely change them).
- [ ] opt. Settings button. (Luka)
  - disable audio.
  - OCD Mode.
  - maybe audio adjusting.
  - maybe tutorial mode can be toggled here.
## Running
- [ ] Bug fix: fix flicker after state transition to running. (Hallucinations)
- [ ] Improve graphics. (Luka)
  - change background.
  - have nice looking `go back` and `trash` buttons.
- [ ] Add total value above caravans. (Luka)
- [ ] Implement win/lose animations. (Pece)
  - implement a function which check when a player wins.
    - the winning conditions of caravan are as follows:
      1) all caravans are sold.
      2) winning player has at least 2 winning caravans.
      - a caravan is considered sold if:
        1) its value is greater than the opposing caravan.
        2) its value is in the range 21-26 (inclusive).
  - implement animations.
- [ ] (Fixed, needs testing) ~~Bug fix: player 2 sometimes has 4 instead of 5 playing cards.~~ (Pece)
- [ ] opt. Implement a logger. (Luka)
  - save the name of the state of the game.
  - log which player played which move.
  - ex. Running - Player 1 plays `ace spades` on `player 1 caravan A` - Player 2 plays `joker red` on `player 1 caravan C card 10 hearts`
- [ ] (Fixed, needs testing) ~~Handle cards `z-index` better.`~~
- [ ] Display number of cards left in drawing pile. (Luka)
- [ ] Distribute one standard deck into playing cards and drawing deck. (Pece)
  - the playing cards MUST contain at least 3 numerical cards.