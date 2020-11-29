from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock 
from random import randint

Hardness = 4

class PongPaddle(Widget):
	score = NumericProperty(0)

	def bounce_ball(self, ball):

		 if self.collide_widget(ball):
		 	ball.velocity_x *= -1




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
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def serve_ball(self):
		self.ball.velocity = Vector(Hardness, 0).rotate(randint(0, 360))
		

	def update(self, dt):

		self.ball.move()

		# bounce off at top/bottom

		if (self.ball.y < 0) or (self.ball.y > self.height - 15):
			self.ball.velocity_y *= -1

		# bounce off left
		if self.ball.x < 0:
			self.ball.velocity_x *= -1
			self.player2.score += 1

		# bounce off right
		if self.ball.x > self.width - 15:
			self.ball.velocity_x *= -1
			self.player1.score += 1


		#idk it works or not, but it's to prevent ball moving along y axis in a straight line loop

		#while self.ball.velocity == Vector(self.center_x, Hardness):
		#	PongApp().run()

		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)

# on_touch_down()- When our fingers/mouse touches the screen
# on_touch_up()-	When we lift off fingers from the screen after touching it
# on_touch_move()-	When we drag our finger on the screen

	def on_touch_move(self, touch):

		if touch.x < self.width / 1/4:
			self.player1.center_y = touch.y

		if touch.x > self.width * 3/4:
			self.player2.center_y = touch.y
		
		else :
			pass



class PongApp(App):
	def build(self):

		game = PongGame()

		game.serve_ball() 

		Clock.schedule_interval(game.update,1.0/60.0)

		return game

PongApp().run() 