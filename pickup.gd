extends Area3D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	var v = Input.get_axis("left", "right") * 5
	translate(Vector3.RIGHT * delta * v)
	var v1 = Input.get_axis("backward", "forward") * 5
	translate(Vector3.FORWARD * delta * v1)
	var v2 = Input.get_axis("up", "down") * 5
	translate(Vector3.UP * delta * v2)
	
	pass


func _on_body_entered(body: Node3D) -> void:
	# body.add_coins() #duck typing
	pass # Replace with function body.
