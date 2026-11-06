extends CharacterBody3D

@export var speed:float = -1
@export var rot_speed = 10.0

@export var bullet_scene:PackedScene
@export var bullet_spawn:Node3D

@export var fire_rate:int = 10

@onready var wall = $"../wall"

@onready  var timer = $Timer

func print_stuff():
	DebugDraw2D.set_text("position", position)
	DebugDraw2D.set_text("global_position", position)
	DebugDraw2D.set_text("rotation", rotation)
	DebugDraw2D.set_text("global_rotation", global_rotation)

	DebugDraw2D.set_text("basis.x", transform.basis.x)
	DebugDraw2D.set_text("basis.y", transform.basis.y)
	DebugDraw2D.set_text("basis.z", transform.basis.z)
	DebugDraw2D.set_text("global basis.x", global_transform.basis.x)
	DebugDraw2D.set_text("global basis.y", global_transform.basis.y)
	DebugDraw2D.set_text("global basis.z", global_transform.basis.z)
	#print(scale)
	#print(global_scale)
	

func _time_out():
	#print("fira again")
	can_fire = true

func _ready() -> void:
	timer.wait_time = 1.0 / fire_rate
	timer.connect("timeout", _time_out)
	pass 

var can_fire:bool = true

func _physics_process(delta: float) -> void:

	print_stuff()

	# Other ways of moving by manipulating the transform	
	# global_position.z += speed * delta
	
	var f = Input.get_axis("back", "forward")
	
	var v = Vector3()	
	v = global_transform.basis.z # My direction vector	
	# print(global_transform.basis.z)
	velocity = v * speed * f
	# position += speed * delta * global_transform.basis.z * f
	
	move_and_slide()
	
	var r = Input.get_axis("left", "right")
	
	rotate_y(- deg_to_rad(rot_speed) * r * delta)
	# rotate_y()
	# rotate_y(deg_to_rad(rot_speed) * delta)
	# rotate_x(deg_to_rad(rot_speed) * delta)
	
	
	if can_fire and Input.is_action_pressed("shoot"):
		var bullet = bullet_scene.instantiate()
		get_parent().add_child(bullet)
		#can_fire = fals
		#print("not can fire ")
	
		bullet.global_position = bullet_spawn.global_position
		bullet.global_rotation = global_rotation
		timer.start()
	pass
	
@export var enemy:Node3D
	
func _process(delta: float) -> void:
	var e = $"../enemy"

	var toEnemy:Vector3 = e.global_position - global_position

	toEnemy = toEnemy.normalized()
	var d:float = global_transform.basis.z.dot(toEnemy)
			
	var theta = acos(d)
	var fov = 45
	theta = rad_to_deg(theta)
	if theta < fov:
		DebugDraw2D.set_text("fov", "inside")
	else:
		DebugDraw2D.set_text("fov", "outside")
	
	DebugDraw2D.set_text("theta", theta)

	pass
