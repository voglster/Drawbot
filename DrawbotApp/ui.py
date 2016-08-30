#ThorPy hello world tutorial : step 2
import thorpy

application = thorpy.Application(size=(300, 300), caption="Hello world")

my_button = thorpy.make_button("Hello world!") #just a useless button

#a button for leaving the application:
quit_button = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)

#a background which contains quit_button and useless_button
background = thorpy.Background.make(color=(200, 200, 255),
                                    elements=[my_button, quit_button])

#automatic storage of the elements
thorpy.store(background)

menu = thorpy.Menu(background) #create a menu on top of the background
menu.play() #launch the menu

application.quit()