(define (problem ZTRAVEL-1-2)
(:domain zenotravel)
(:objects
	plane1 - aircraft
	plane2 - aircraft
	person1 - person
	city0 - city
	)
(:init
	(located plane1 city0)
	(located plane2 city0)
	(= (capacity plane1) 60000)
	(= (capacity plane2) 60000)
	(= (fuel plane1) 40000)
	(= (fuel plane2) 40000)
	(= (fast-burn plane1) 15)
	(= (fast-burn plane2) 15)
	(= (onboard plane1) 0)
	(= (onboard plane2) 0)
	(= (zoom-limit plane1) 8)
	(= (zoom-limit plane2) 8)
	(located person1 city0)
	(= (distance city0 city0) 0)
	(= (total-fuel-used) 0)

)
(:goal (and
	(located person1 city0)
	))
(:metric  minimize (total-fuel-used) )

)