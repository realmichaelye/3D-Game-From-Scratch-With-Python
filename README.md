# 3D Game From Scratch

I was bored in my grade 10 compsci class, so instead of making a 2D game for my summative, I decided to learn Linear Algebra and 3D projection and made a 3D space shooter game with only numpy and pygame.

## The Process of Making this Game(Written Report Part of Summative):

### Introduction
I approached my 3D Game Shooter project knowing it will be an extremely difficult challenge and serious effort is required in 1. Learning the underlying math(linear algebra: matrices, dot products, cross products...) of 3D to 2D projection, 3D rotation, 3D movement, etc… and 2. Converting the underlying math into an efficient, runnable program using only 2 external libraries, pygame and numpy; all without copying pasting code from the internet. Although I had to spend tens of hours learning linear algebra from scratch and re-coding the entire program dozens of times to make it more efficient, it has elevated my understanding of computer science and mathematics in a profound way. Now I will go in depth about how I handled each stage of the Software Development Cycle.

### Planning
In the planning phase, I studied the feasibility of creating this program. At first, I cracked the code for 3D to 2D projection (after a thought experiment done thinking about how to project 4D onto a 3D space and then project that on a 2D plane), however that’s only the tip of the iceberg.
![alt text](https://miro.medium.com/max/1092/1*vfDeX9HH5TGwY2cgyBuuFA.png)

My program involves rotating and moving the player’s vision freely in 3D, that was completely out of my field of expertise until I discovered linear algebra. I spent tens of hours watching 3Blue1Brown and Khan Academy’s videos to gain an intuitive understanding of Linear Algebra. Once I’ve understood the math, it’s clear the program is feasible on a purely mathematical level. All I need to do left is translate and organize the formulas into python which is in my field of expertise. Therefore, the program is feasible and we can move onto the next stage.

### Analysis
In the analysis phase, I broke the program down to different parts and analyzed serious programming challenges. Here is the analysis for the programming challenges.
* 3D to 2D projection
* 3D Translation
* 3D Rotation
* 3D Sphere Scaling & Stretching
* 3D Bullet and Sphere Collision
* *3D Check if Object is behind a player

*Challenge: Since the coordinate system allows the player to freely move around and look around in 3D space, the math isn’t as simple as checking if(sphere.z<player.z) since when the player’s yaw and pitch is changed, to find whether an object is behind the player, you must check if it’s behind in respect to the plane at which is rotated according to pitch and yaw: This magnifies such a simple problem to an extremely difficult linear algebra problem.

### Design
In the design phase, I used the problems found in the analysis stage and figured out the most efficient solutions to those problems.
* 3D to 2D projection: Solved using similar triangles
* 3D Translation: Offset playerX, playerY, playerZ when key is pressed
* 3D Rotation: Take the dot product of a 3D rotation matrix and the position of all sphere objects. During this step, first offset the position by the player position, and after the rotation is completed, offset the position back. This is done so rotation is completed about the player position instead of the origin.
* 3D Sphere Scaling & Stretching: Solved using similar triangles
* 3D Bullet and Sphere Collision: Check if crosshair is on Sphere
* *3D Check if Object is behind a player: First rotate every point and player back to the original position(prior to applying the transformation of yaw, pitch, and roll). Then check if sphere.z < player.z. Finally, re-rotate every point and player back to the original state.

### Implementation
Every programmer knows your code doesn’t always go as planned, therefore in my implementation phase, I had to make serious modifications to the design of my program. Here are the major changes and modifications to the previous design.
#### Major Changes
* 3D Rotations no longer rotates the player, instead, it rotates the space around the player. (This is done since previously, to find if a point is behind the player, you must rotate everything in parallel to the z-axis, and then compare the z coordinate and player.z. This is extremely inefficient since you rotate all points 2 times. Therefore instead, keep the player’s vision always parallel to the z-axis. When you “rotate the player”, you just rotate all the points around the player the opposite way. )
* Created ScreenType enumeration class: Because using an enumeration for the screen is much more intuitive and easy to read than setting variables for if player lost. This way all you have to do is player.screenType = ScreenType.INTRO and it will display intro screen, if you set it to GAME it will display the game screen and so on.
* I realized my program does not sort the spheres, therefore when spheres are behind each other, sometimes they still render. That’s why I implemented a sortSpheres() function to sort the spheres according to their distance away from the player, so closer spheres render last, adding the feature of depth(uses bubble sort, I did not want to use more efficient algorithms because my goal is to never copy and paste code for this project, and only work with what I fully understand).
#### Minor Changes
* Created button class inside RenderUtils: Buttons are extremely annoying to create if done individually using rectangles and fonts. Especially this way you must recreate the click detection method for each button. Therefore, I created a generalized class for the button. To create a button, write: button = Button(parameters go here...), and to draw a button, write: button.draw().
* Created a CONSTANTS class: I realized there’s a need to share constants between the Main class and RenderUtils class. One way to do this is to put everything in the player class however it seems unintuitive to have constants such as the sound-files, and font-files in the player class, therefore I created a separate class called CONSTANTS.

## THE END
