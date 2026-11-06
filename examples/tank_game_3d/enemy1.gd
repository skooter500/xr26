extends Marker3D

@onready var player = $"../tank"
@export var range = 6

var fov = 45

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# $"../tank/StaticBody3D" # get_node("../tank/StaticBody3D")
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	
	var d = global_position.distance_to(player.global_position)
	if d < range:
		#print("Inside")
		pass
	else:
		#print("outside")
		pass
	
	var to_player:Vector3 = player.global_position - global_position
	var angle = to_player.angle_to(global_basis.z)
	#print("angle: " + str(angle))
	DebugDraw3D.draw_arrow(global_position, global_position + (global_basis.z * 5), Color.BLUE, 0.1)
	
	#if rad_to_deg(angle) < 45:
		#print("Inside FOV")
	#else:
		#print("Outside FOV")
	#pass
	
	to_player = to_player.normalized()
	var dot = to_player.dot(global_basis.z)
	#print(dot)
	var ad = acos(dot)
	#print("ad" + str(ad))
