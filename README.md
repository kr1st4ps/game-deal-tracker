# Game deal tracker

This code will take a list of games you want (PS and Oculus store games for now), and check the current price in the respective store. Depending on the price and price history, an email will be sent to you if the current discount on the game is good.

To be able to properly use this:

-   Modify config.ini with your data where it is asked

-   Check requirements.txt, to make sure you have all necessary python libraries installed

-   When adding the name of your wanted game, please use exact full name from PS store 

-   For ease of use find a way to schedule the execution of this code (eg. using cron jobs)

# TO DOs

-   Add support for steam store

-   Make it so there is no need to have the exact name of the game

-   Add support for Amazon (various regions) for PS games

-   Improve email design