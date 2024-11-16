(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	thermograph0 - mode
	Star0 - direction
	GroundStation1 - direction
	Phenomenon4 - direction
	Star5 - direction
	Phenomenon6 - direction
)
(:init
	(supports instrument0 thermograph0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon6)
	(= (data_capacity satellite0) 1000)
	(= (fuel satellite0) 112)
	(= (data Phenomenon4 thermograph0) 134)
	(= (data Star5 thermograph0) 273)
	(= (data Phenomenon6 thermograph0) 219)
	(= (slew_time GroundStation1 Star0) 18.17)
	(= (slew_time Star0 GroundStation1) 18.17)
	(= (slew_time Phenomenon4 Star0) 35.01)
	(= (slew_time Star0 Phenomenon4) 35.01)
	(= (slew_time Phenomenon4 GroundStation1) 31.79)
	(= (slew_time GroundStation1 Phenomenon4) 31.79)
	(= (slew_time Star5 Star0) 36.56)
	(= (slew_time Star0 Star5) 36.56)
	(= (slew_time Star5 GroundStation1) 8.59)
	(= (slew_time GroundStation1 Star5) 8.59)
	(= (slew_time Star5 Phenomenon4) 64.5)
	(= (slew_time Phenomenon4 Star5) 64.5)
	(= (slew_time Phenomenon6 Star0) 77.07)
	(= (slew_time Star0 Phenomenon6) 77.07)
	(= (slew_time Phenomenon6 GroundStation1) 17.63)
	(= (slew_time GroundStation1 Phenomenon6) 17.63)
	(= (slew_time Phenomenon6 Phenomenon4) 2.098)
	(= (slew_time Phenomenon4 Phenomenon6) 2.098)
	(= (slew_time Phenomenon6 Star5) 29.32)
	(= (slew_time Star5 Phenomenon6) 29.32)
	(= (data-stored) 0)
	(= (fuel-used) 0)
)
(:goal (and
	(have_image Phenomenon4 thermograph0)
	(have_image Star5 thermograph0)
	(have_image Phenomenon6 thermograph0)
))
(:metric minimize (fuel-used))

)
