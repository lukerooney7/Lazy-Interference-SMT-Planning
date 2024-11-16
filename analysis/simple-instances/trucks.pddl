(define (problem truck-1)
(:domain Trucks)
(:objects
	truck1 - truck
	package1 - package
	l1 - location
	l2 - location
	t0 - time
	a1 - truckarea
	a2 - truckarea)

(:init
	(at truck1 l1)
	(free a1 truck1)
	(free a2 truck1)
	(closer a1 a2)
	(at package1 l1)

	(time-now t0))

(:goal (and
	(delivered package1 l1 t0)))
)
