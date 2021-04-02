# QIX Game

Note:
    - Instead of North, West, East, South: Up, Left, Right, Down
    - The Map object will only be rendering the graphics.
    - The logic aspect of things should be implemented in other objects.
    - Qix and Sparx should not collide with each other.

1. Class Enemy
    1. _Sparx_: 
        - Randomly initialized in a coordinate where it is a division of 5. Otherwise, it will go out of the border
        - The initial Orientation will either be **Vertical** or **Horizontal**.
        - For each Orientation the movement will differ.
    2. _Qix:
        - Randomly initialized in a coordinate where it is a division of 5. Otherwise, it will go out of the border