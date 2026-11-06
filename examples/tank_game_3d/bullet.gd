extends Area3D

@export var speed:float=20

@export var explosion_scene:PackedScene

func _physics_process(delta: float) -> void:	
	var v = global_transform.basis.z
	global_position = global_position + v * speed * delta
	look_at(global_position - global_transform.basis.z)
	# global_translate(v * speed * delta)


func _on_timer_timeout() -> void:
	self.queue_free()
	pass # Replace with function body.


func _on_body_entered(b: Node3D) -> void:
		var explosion:GPUParticles3D = explosion_scene.instantiate()
		get_parent().add_child(explosion)		
		explosion.global_position = global_position
		explosion.emitting = true
		
		var color = b.get_node("MeshInstance3D").get_surface_override_material(0).albedo_color
		var m = StandardMaterial3D.new()		
		m.albedo_color = color
		explosion.material_override = m
		self.queue_free()		
		b.queue_free()		
		pass


func _on_area_entered(area: Area3D) -> void:
	print("area entered!!!")
	pass # Replace with function body.
