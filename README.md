P2P betting site. I made it a few years ago with Django and HTMX.
The UI looks terrible and the code is ugly, but it works more or less. Payments are made with Bitcoin via a separate BTCPayServer that I set up.

Concept: A football game has three outcomes: Team 1 wins, Team 2 wins, or a draw. Users can create a bet and pick one or two outcomes and set a stake. If a game cannot end in a draw, then there is only one option to pick from two: either Team 1 wins or Team 2 wins.
Let's say I create a bet on Chelsea winning against Man City, or them playing to a draw, and I bet 20 Taler (the site's in-house currency). Now, you wait for another user to accept the bet. Both users stake 20 Taler. So, if Chelsea wins or they play to a draw, I get my 20 Taler back, plus the 20 Taler from the opponent. If Man City wins, the other user gets my 20 Taler, plus their 20 Taler.

![ezgif-888e8ba74d76f961](https://github.com/user-attachments/assets/39e37603-a7d1-4d0e-a4e4-61bf05360c13)

<img width="959" height="477" alt="screenshot1" src="https://github.com/user-attachments/assets/5533f7d5-2bbd-48db-b123-fa31a2875ac7" />

<img width="959" height="481" alt="screenshot2" src="https://github.com/user-attachments/assets/49ed5585-d434-4116-9909-166372bb6430" />
