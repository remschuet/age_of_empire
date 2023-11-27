# age_of_empire
Age Of Empire using QT, network, python

# Start the game
- Start main_serveur
- Start 1 at 2 main_age
- main_chat is juste to have a chat

# Package
## Backup
- Sauvegarde de certains projets / idées

## Entity
- Represents all kinds of entity possible in the 2d game
- All entity inherit from Entity class

## GameEngine
- Represents all the game pattern,
- Gameplay
- GameScene
- GameListener
- GameNumpy

## GUI
- Represents all my:
- q_assets
- image for the games
- Contains folder images

## Serveur
- Contains my client and server part

## Utils
- Contains:
- Math algorythmes
- A_Star algorythme


# Entity part
## Where to found all data for entity creation
- gameplay  (Slot for creation)
- gameplay  (emit to send creation)
- main_age  (received from serveur, send to gameplay)
- NameClass (for all datas for the entity)
- const_image_name  (for the name of the image)
- const_action      (for the id of the action)

