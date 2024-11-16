(define (problem roverprob1234) (:domain Rover)
(:objects
	general - Lander
	colour - Mode
	rover0 rover1 - Rover
	rover0store - Store
	waypoint0 waypoint1 - Waypoint
	camera0 - Camera
	objective0 - Objective
	)
(:init
	(visible waypoint1 waypoint0)
	(visible waypoint0 waypoint1)
	(at_soil_sample waypoint0)
	(at_rock_sample waypoint1)
	(at_lander general waypoint0)
	(channel_free general)
	(available rover0)
	(store_of rover0store rover0)
	(empty rover0store)
	(equipped_for_soil_analysis rover0)
	(equipped_for_rock_analysis rover0)
	(equipped_for_imaging rover0)
	(on_board camera0 rover0)
	(supports camera0 colour)
	(visible_from objective0 waypoint0)
	(visible_from objective0 waypoint1)
)

(:goal (and
(communicated_image_data objective0 colour)
	)
)
)
