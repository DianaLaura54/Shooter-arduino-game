This project is a simple arcade-style game inspired by Space Invaders, where the player dodges and shoots falling objects. It uses the Processing IDE for graphics and a micro:bit as the game controller via serial communication.

Gameplay:
Player controls: Tilt the micro:bit to move (left = "W", right = "E"), press Button A to shoot ("F"), and Button B to restart after game over ("R").
Lives: Player starts with 3 lives and gains temporary immunity after being hit.
Shooting: Limited to one shot every 20 frames.
Enemies: 10 falling objects loop from top to bottom with increasing speed as difficulty ramps up.
Scoring: Score increases over time based on survival.

Features:
micro:bit LED display shows direction arrows based on tilt.
Collision detection between player/obstacles and bullets/obstacles.
Game restarts only when lives reach 0 and "R" is received.
Reuses objects for efficiency.

Technologies Used:
Processing (Java): Game logic, rendering, and serial communication.
micro:bit: Accelerometer input and button controls.
