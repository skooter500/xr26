extends CharacterBody3D


const SPEED = 5.0
const JUMP_VELOCITY = 4.5

var coins = 0

var speed = 2

var log = ""

func _process(delta):
	log = ""
	log_text("basis.z " + str(basis.z))
	log_text("basis.x " + str(basis.x))
	log_text("basis.y " + str(basis.y))
	log_text("position " + str(position))
	
	# distance 1
	var d:Vector3 = ($"../pickup".position - position)
	var f = d.length()
	
	var f1 = position.distance_to($"../pickup".position)
	log_text("dist 1 " + str(f))
	log_text("f1 " + str(f1))
	
	var v1 = basis.z
	var v2 = $"../pickup".position - position
	
	var dot = v1.dot(v2)
	log_text("dot: " + str(dot))
	if dot < 0:
		log_text("behind")
	else:
		log_text("in front")
	var theta = acos(v1.dot(v2) / (v1.length() * v2.length()))
	
	var t1 = basis.z.angle_to(v2)
	log_text("angle to: " + str(rad_to_deg(t1)))
	
	var t2 = atan2(v2.y, v2.x)
	log_text("atan to: " + str(rad_to_deg(t2)))
	
	DebugDraw3D.draw_arrow(global_position, global_position + basis.z * 10, Color.WHEAT, 0.1)
	log_text("angle: " + str(rad_to_deg(theta)))
	$"../log".text = log
	
	
func log_text(s):
	log += s + "\n"

func add_coins():
	coins += 1
	$"../coins".text = "Coins: " + str(coins)

func _physics_process(delta: float) -> void:
	# Add the gravity.
	#velocity = basis.z * speed
	#move_and_slide()
	#position += basis.z * speed
	rotate_y(delta * 0.3)


func _on_pickup_body_entered(body: Node3D) -> void:
	print()
	pass # Replace with function body.
