from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock 
from random import randint
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color

#icon
Config.set('kivy','window_icon','icon.png')

#increase the speed of ball
game_level = 5

#SFX
bgm = SoundLoader.load('ball_hit.wav')
miss = SoundLoader.load('miss.wav')

#BgColor
Window.clearcolor = (52/255.0, 111/255.0, 207/255.0, 1)



class PongPaddle(Widget):
	score = NumericProperty(0)

	def bounce_ball(self, ball):

		 if self.collide_widget(ball):
		 	bgm.play()
		 	ball.velocity_x *= -1 #comment it to run lower code
# to increase the speed of ball on each collision with paddle uncomment lower line
			#ball.velocity_x *= -1.1


class PongBall(Widget):

	# velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball   
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos        


class PongGame(Widget): #moving the ball by calling the move() and other objects
	
	ball = ObjectProperty(None) 
	left_player = ObjectProperty(None)
	right_player = ObjectProperty(None)

	def serve_ball(self):
		self.ball.velocity = Vector(game_level, 0).rotate(randint(0, 360))

	def update(self, dt):
		self.ball.move()

		# bounce off at top/bottom
		if (self.ball.y < 0) or (self.ball.y > self.height - 15):
			self.ball.velocity_y *= -1

		# bounce off left
		if self.ball.x < 0:
			self.ball.velocity_x *= -1
			self.right_player.score += 1
			miss.play()

		# bounce off right
		if self.ball.x > self.width - 15:
			self.ball.velocity_x *= -1
			self.left_player.score += 1
			miss.play()

		#idk it works or not, but it's to prevent ball moving along y axis in a straight line loop
		#if self.ball.velocity == Vector(self.center_x, game_level):
		#	PongApp().run()

		# making ball bounce on paddle
		self.left_player.bounce_ball(self.ball)
		self.right_player.bounce_ball(self.ball)

# on_touch_move()-	When we drag our finger on the screen
	def on_touch_move(self, touch):

		if touch.x < self.width / 1/4:
			self.left_player.center_y = touch.y

		if touch.x > self.width * 3/4:
			self.right_player.center_y = touch.y
		
		else :
			pass


class PongApp(App):	# Building the kivy App
	def build(self):

		game = PongGame()

		game.serve_ball() 

		Clock.schedule_interval(game.update,1.0/60.0) #drawing 60 frames of ball per socond

		return game

PongApp().run()
