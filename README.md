# QIX Game

Note:

- The Map object will only be rendering the graphics.
- The logic aspect of things should be implemented in other objects.
- Qix and Sparx should not collide with each other.
- When player moves toward certain direction, they will not be able to move in the opposite direction.
- Qixes will not hit the player on the borders, Sparxes will.

1. Class Enemy
    1. _Sparx_: 
        - Randomly initialized in a coordinate where it is a division of 5. Otherwise, it will go out of the border
        - The initial Orientation will either be **Vertical** or **Horizontal**.
        - For each Orientation the movement will differ.
    2. _Qix:
        - Randomly initialized in a coordinate where it is a division of 5. Otherwise, it will go out of the border
2. Map:
    - Will give other objects ability to communicate with each other within the object.
    - Checks for collisions and handle the lifetime of the player.

link to the [game](https://playclassic.games/games/action-dos-games-online/play-qix-online/)

To implement:

- Dynamic bordering:
    - The player will first enter the area using the space bar.
    - When the space bar is not hit, the player will only move horizontally or vertically (run the code).
    - After entering the area, the player will not be able to make opposite moves (cannot do a left after a right or an up after a down).
    - An incursion area will be achieved when the start point and end point is on a border. (Note: The start is obviously on a border)
    - Task: Dynamicly change the borderings so all the new claimed areas are included.
- Drawing the claimed parts / Percentage (Ahnaf)
- Check for the space bar being pressed (first time) (Angelo)
- Writting tests (Damoon)
- Modify User stories (Angelo)
- Test Diagrams (Damoon, Angelo)