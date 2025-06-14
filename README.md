# 🧟 Zombie Shooter Game (Python + Pygame)

This is a simple **top-down 2D zombie shooter game** built using **Python and Pygame**. Control a rotating gun, shoot incoming zombies, and survive as long as you can!

---

## 🎮 Features

- 🧭 Rotate gun using LEFT and RIGHT arrow keys
- 🔫 Fire bullets in the rotated direction using SPACEBAR
- 💥 Real-time collision detection between bullets and zombies
- 🔊 Gunfire and zombie-blast sound effects
- 🧟 Zombies spawn randomly and move downward
- 🧠 Built entirely with Python and Pygame

---

## 🖥️ Requirements

- Python 3.7 or higher
- Pygame library

Install Pygame using pip:

```bash
pip install pygame

🗂️ Project Structure
ZombieShooter/
├── shooter.py            # Main game code
├── gun_imagee.jpg        # Player gun image
├── zombie.png            # Zombie image
├── gun_sound.mp3         # Gunfire sound
├── gun_blast.wav         # Zombie explosion sound
├── README.md             # This file

🚀 How to Run the Game
Clone or Download the Repo
git clone https://github.com/namansinghpatel/Python_Progs.git
cd Python_Progs
Run the Game

python shooter.py
🎮 Game Controls
Key	Action
LEFT ⬅️	Rotate gun counter-clockwise
RIGHT ➡️	Rotate gun clockwise
SPACE 🔫	Shoot bullet

🧠 How It Works
The gun rotates based on arrow keys.

When the player hits SPACE, a bullet is fired in the direction of the gun.

Zombies randomly spawn at the top of the screen and move downward.

If a bullet hits a zombie, the zombie disappears, and your score increases.

If any zombie reaches the bottom, it's Game Over.

📸 Screenshot
(You can add a screenshot here by saving an in-game image and naming it screenshot.png, then uncomment below)

<!-- ![Gameplay Screenshot](screenshot.png) -->
📜 License
This project is licensed under the MIT License.

👤 Author
Naman Singh Patel

🔗 GitHub: @namansinghpatel

🤝 Contributing