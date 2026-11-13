extends CharacterBody3D


const SPEED = 5.0
const JUMP_VELOCITY = 4.5

var coins = 0

var speed = 2
var t = 4
var log = ""

@onready var pickup = get_node("../pickup")

var is_slerping:bool = false

func _ready() -> void:
	var f1 = position.distance_to($"../pickup".position)
	
	speed = f1 / t

var target_quaternion:Quaternion
var start_quaternion:Quaternion

func _process(delta):
	
	if Input.is_action_just_pressed("shoot"):
		var to_target = pickup.global_position - global_position
		to_target = to_target.normalized()
		var axis = Vector3.FORWARD.cross(to_target)
		axis = axis.normalized()
		var theta = to_target.angle_to(Vector3.FORWARD) 
		target_quaternion = Quaternion(axis, theta)
		
		start_quaternion = global_basis.get_rotation_quaternion()
		is_slerping = true
		t = 0
		
	if is_slerping:
		var q = start_quaternion.slerp(target_quaternion, t)
		print(start_quaternion)
		print(target_quaternion)
		
		t += delta
		print(t)
		if t > 1.0:
			is_slerping = false
		global_basis = Basis(q)
	
	
	
	
	log = ""
	log_text("basis.z " + str(basis.z))
	log_text("basis.x " + str(basis.x))
	log_text("basis.y " + str(basis.y))
	log_text("position " + str(position))
	
	# distance 1
	
	#var q:Quaternion
	#var t = Vector3.FORWARD.angle_to(pickup.global_position - global_position)
	#q = Quaternion(Vector3.DOWN, t)
	#global_basis = Basis(q)
	#$"../log".text = log
	#
	
func log_text(s):
	log += s + "\n"

func add_coins():
	coins += 1
	$"../coins".text = "Coins: " + str(coins)


func _physics_process(delta: float) -> void:
	# Add the gravity.
	pass

func _on_pickup_body_entered(body: Node3D) -> void:
	print()
	pass # Replace with function body.
