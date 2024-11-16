(define (problem ZTRAVEL-5-20)
(:domain zenotravel)
(:objects
	plane1 - aircraft
	plane2 - aircraft
	plane3 - aircraft
	plane4 - aircraft
	plane5 - aircraft
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
	person7 - person
	person8 - person
	person9 - person
	person10 - person
	person11 - person
	person12 - person
	person13 - person
	person14 - person
	person15 - person
	person16 - person
	person17 - person
	person18 - person
	person19 - person
	person20 - person
	city0 - city
	city1 - city
	city2 - city
	city3 - city
	city4 - city
	city5 - city
	city6 - city
	city7 - city
	city8 - city
	city9 - city
	city10 - city
	city11 - city
	city12 - city
	city13 - city
	city14 - city
	city15 - city
	)
(:init
	(located plane1 city14)
	(= (capacity plane1) 10969)
	(= (fuel plane1) 397)
	(= (slow-burn plane1) 5)
	(= (fast-burn plane1) 19)
	(= (onboard plane1) 0)
	(= (zoom-limit plane1) 4)
	(located plane2 city11)
	(= (capacity plane2) 5305)
	(= (fuel plane2) 343)
	(= (slow-burn plane2) 2)
	(= (fast-burn plane2) 4)
	(= (onboard plane2) 0)
	(= (zoom-limit plane2) 1)
	(located plane3 city4)
	(= (capacity plane3) 3033)
	(= (fuel plane3) 26)
	(= (slow-burn plane3) 1)
	(= (fast-burn plane3) 3)
	(= (onboard plane3) 0)
	(= (zoom-limit plane3) 4)
	(located plane4 city11)
	(= (capacity plane4) 14632)
	(= (fuel plane4) 4714)
	(= (slow-burn plane4) 5)
	(= (fast-burn plane4) 12)
	(= (onboard plane4) 0)
	(= (zoom-limit plane4) 4)
	(located plane5 city15)
	(= (capacity plane5) 8462)
	(= (fuel plane5) 646)
	(= (slow-burn plane5) 3)
	(= (fast-burn plane5) 7)
	(= (onboard plane5) 0)
	(= (zoom-limit plane5) 2)
	(located person1 city0)
	(located person2 city14)
	(located person3 city12)
	(located person4 city7)
	(located person5 city4)
	(located person6 city14)
	(located person7 city4)
	(located person8 city0)
	(located person9 city3)
	(located person10 city7)
	(located person11 city3)
	(located person12 city15)
	(located person13 city10)
	(located person14 city1)
	(located person15 city7)
	(located person16 city9)
	(located person17 city7)
	(located person18 city5)
	(located person19 city11)
	(located person20 city0)
	(= (distance city0 city0) 0)
	(= (distance city0 city1) 547)
	(= (distance city0 city2) 747)
	(= (distance city0 city3) 712)
	(= (distance city0 city4) 979)
	(= (distance city0 city5) 517)
	(= (distance city0 city6) 506)
	(= (distance city0 city7) 956)
	(= (distance city0 city8) 694)
	(= (distance city0 city9) 946)
	(= (distance city0 city10) 931)
	(= (distance city0 city11) 907)
	(= (distance city0 city12) 898)
	(= (distance city0 city13) 707)
	(= (distance city0 city14) 587)
	(= (distance city0 city15) 775)
	(= (distance city1 city0) 547)
	(= (distance city1 city1) 0)
	(= (distance city1 city2) 888)
	(= (distance city1 city3) 721)
	(= (distance city1 city4) 749)
	(= (distance city1 city5) 588)
	(= (distance city1 city6) 598)
	(= (distance city1 city7) 562)
	(= (distance city1 city8) 610)
	(= (distance city1 city9) 958)
	(= (distance city1 city10) 912)
	(= (distance city1 city11) 798)
	(= (distance city1 city12) 996)
	(= (distance city1 city13) 620)
	(= (distance city1 city14) 864)
	(= (distance city1 city15) 716)
	(= (distance city2 city0) 747)
	(= (distance city2 city1) 888)
	(= (distance city2 city2) 0)
	(= (distance city2 city3) 888)
	(= (distance city2 city4) 895)
	(= (distance city2 city5) 763)
	(= (distance city2 city6) 635)
	(= (distance city2 city7) 607)
	(= (distance city2 city8) 743)
	(= (distance city2 city9) 653)
	(= (distance city2 city10) 613)
	(= (distance city2 city11) 699)
	(= (distance city2 city12) 847)
	(= (distance city2 city13) 560)
	(= (distance city2 city14) 631)
	(= (distance city2 city15) 754)
	(= (distance city3 city0) 712)
	(= (distance city3 city1) 721)
	(= (distance city3 city2) 888)
	(= (distance city3 city3) 0)
	(= (distance city3 city4) 959)
	(= (distance city3 city5) 839)
	(= (distance city3 city6) 842)
	(= (distance city3 city7) 734)
	(= (distance city3 city8) 727)
	(= (distance city3 city9) 564)
	(= (distance city3 city10) 984)
	(= (distance city3 city11) 815)
	(= (distance city3 city12) 662)
	(= (distance city3 city13) 546)
	(= (distance city3 city14) 926)
	(= (distance city3 city15) 621)
	(= (distance city4 city0) 979)
	(= (distance city4 city1) 749)
	(= (distance city4 city2) 895)
	(= (distance city4 city3) 959)
	(= (distance city4 city4) 0)
	(= (distance city4 city5) 959)
	(= (distance city4 city6) 725)
	(= (distance city4 city7) 617)
	(= (distance city4 city8) 580)
	(= (distance city4 city9) 589)
	(= (distance city4 city10) 833)
	(= (distance city4 city11) 968)
	(= (distance city4 city12) 984)
	(= (distance city4 city13) 597)
	(= (distance city4 city14) 604)
	(= (distance city4 city15) 592)
	(= (distance city5 city0) 517)
	(= (distance city5 city1) 588)
	(= (distance city5 city2) 763)
	(= (distance city5 city3) 839)
	(= (distance city5 city4) 959)
	(= (distance city5 city5) 0)
	(= (distance city5 city6) 840)
	(= (distance city5 city7) 757)
	(= (distance city5 city8) 705)
	(= (distance city5 city9) 540)
	(= (distance city5 city10) 604)
	(= (distance city5 city11) 766)
	(= (distance city5 city12) 672)
	(= (distance city5 city13) 859)
	(= (distance city5 city14) 725)
	(= (distance city5 city15) 511)
	(= (distance city6 city0) 506)
	(= (distance city6 city1) 598)
	(= (distance city6 city2) 635)
	(= (distance city6 city3) 842)
	(= (distance city6 city4) 725)
	(= (distance city6 city5) 840)
	(= (distance city6 city6) 0)
	(= (distance city6 city7) 701)
	(= (distance city6 city8) 959)
	(= (distance city6 city9) 738)
	(= (distance city6 city10) 766)
	(= (distance city6 city11) 943)
	(= (distance city6 city12) 554)
	(= (distance city6 city13) 928)
	(= (distance city6 city14) 990)
	(= (distance city6 city15) 980)
	(= (distance city7 city0) 956)
	(= (distance city7 city1) 562)
	(= (distance city7 city2) 607)
	(= (distance city7 city3) 734)
	(= (distance city7 city4) 617)
	(= (distance city7 city5) 757)
	(= (distance city7 city6) 701)
	(= (distance city7 city7) 0)
	(= (distance city7 city8) 550)
	(= (distance city7 city9) 950)
	(= (distance city7 city10) 705)
	(= (distance city7 city11) 667)
	(= (distance city7 city12) 530)
	(= (distance city7 city13) 795)
	(= (distance city7 city14) 501)
	(= (distance city7 city15) 998)
	(= (distance city8 city0) 694)
	(= (distance city8 city1) 610)
	(= (distance city8 city2) 743)
	(= (distance city8 city3) 727)
	(= (distance city8 city4) 580)
	(= (distance city8 city5) 705)
	(= (distance city8 city6) 959)
	(= (distance city8 city7) 550)
	(= (distance city8 city8) 0)
	(= (distance city8 city9) 780)
	(= (distance city8 city10) 598)
	(= (distance city8 city11) 603)
	(= (distance city8 city12) 872)
	(= (distance city8 city13) 939)
	(= (distance city8 city14) 860)
	(= (distance city8 city15) 578)
	(= (distance city9 city0) 946)
	(= (distance city9 city1) 958)
	(= (distance city9 city2) 653)
	(= (distance city9 city3) 564)
	(= (distance city9 city4) 589)
	(= (distance city9 city5) 540)
	(= (distance city9 city6) 738)
	(= (distance city9 city7) 950)
	(= (distance city9 city8) 780)
	(= (distance city9 city9) 0)
	(= (distance city9 city10) 980)
	(= (distance city9 city11) 965)
	(= (distance city9 city12) 844)
	(= (distance city9 city13) 652)
	(= (distance city9 city14) 825)
	(= (distance city9 city15) 569)
	(= (distance city10 city0) 931)
	(= (distance city10 city1) 912)
	(= (distance city10 city2) 613)
	(= (distance city10 city3) 984)
	(= (distance city10 city4) 833)
	(= (distance city10 city5) 604)
	(= (distance city10 city6) 766)
	(= (distance city10 city7) 705)
	(= (distance city10 city8) 598)
	(= (distance city10 city9) 980)
	(= (distance city10 city10) 0)
	(= (distance city10 city11) 664)
	(= (distance city10 city12) 527)
	(= (distance city10 city13) 529)
	(= (distance city10 city14) 902)
	(= (distance city10 city15) 793)
	(= (distance city11 city0) 907)
	(= (distance city11 city1) 798)
	(= (distance city11 city2) 699)
	(= (distance city11 city3) 815)
	(= (distance city11 city4) 968)
	(= (distance city11 city5) 766)
	(= (distance city11 city6) 943)
	(= (distance city11 city7) 667)
	(= (distance city11 city8) 603)
	(= (distance city11 city9) 965)
	(= (distance city11 city10) 664)
	(= (distance city11 city11) 0)
	(= (distance city11 city12) 973)
	(= (distance city11 city13) 957)
	(= (distance city11 city14) 722)
	(= (distance city11 city15) 964)
	(= (distance city12 city0) 898)
	(= (distance city12 city1) 996)
	(= (distance city12 city2) 847)
	(= (distance city12 city3) 662)
	(= (distance city12 city4) 984)
	(= (distance city12 city5) 672)
	(= (distance city12 city6) 554)
	(= (distance city12 city7) 530)
	(= (distance city12 city8) 872)
	(= (distance city12 city9) 844)
	(= (distance city12 city10) 527)
	(= (distance city12 city11) 973)
	(= (distance city12 city12) 0)
	(= (distance city12 city13) 938)
	(= (distance city12 city14) 772)
	(= (distance city12 city15) 914)
	(= (distance city13 city0) 707)
	(= (distance city13 city1) 620)
	(= (distance city13 city2) 560)
	(= (distance city13 city3) 546)
	(= (distance city13 city4) 597)
	(= (distance city13 city5) 859)
	(= (distance city13 city6) 928)
	(= (distance city13 city7) 795)
	(= (distance city13 city8) 939)
	(= (distance city13 city9) 652)
	(= (distance city13 city10) 529)
	(= (distance city13 city11) 957)
	(= (distance city13 city12) 938)
	(= (distance city13 city13) 0)
	(= (distance city13 city14) 643)
	(= (distance city13 city15) 939)
	(= (distance city14 city0) 587)
	(= (distance city14 city1) 864)
	(= (distance city14 city2) 631)
	(= (distance city14 city3) 926)
	(= (distance city14 city4) 604)
	(= (distance city14 city5) 725)
	(= (distance city14 city6) 990)
	(= (distance city14 city7) 501)
	(= (distance city14 city8) 860)
	(= (distance city14 city9) 825)
	(= (distance city14 city10) 902)
	(= (distance city14 city11) 722)
	(= (distance city14 city12) 772)
	(= (distance city14 city13) 643)
	(= (distance city14 city14) 0)
	(= (distance city14 city15) 944)
	(= (distance city15 city0) 775)
	(= (distance city15 city1) 716)
	(= (distance city15 city2) 754)
	(= (distance city15 city3) 621)
	(= (distance city15 city4) 592)
	(= (distance city15 city5) 511)
	(= (distance city15 city6) 980)
	(= (distance city15 city7) 998)
	(= (distance city15 city8) 578)
	(= (distance city15 city9) 569)
	(= (distance city15 city10) 793)
	(= (distance city15 city11) 964)
	(= (distance city15 city12) 914)
	(= (distance city15 city13) 939)
	(= (distance city15 city14) 944)
	(= (distance city15 city15) 0)
	(= (total-fuel-used) 0)
)
(:goal (and
	(located plane1 city14)
	(located plane3 city7)
	(located plane5 city12)
	(located person1 city4)
	(located person2 city11)
	(located person3 city0)
	(located person4 city12)
	(located person5 city12)
	(located person6 city0)
	(located person7 city5)
	(located person8 city13)
	(located person9 city9)
	(located person10 city7)
	(located person11 city7)
	(located person12 city6)
	(located person13 city2)
	(located person14 city10)
	(located person15 city14)
	(located person16 city12)
	(located person17 city1)
	(located person18 city1)
	(located person19 city5)
	(located person20 city13)
	))

;(:metric minimize (+ (* 1 (total-time))  (* 3 (total-fuel-used))))
(:metric minimize (total-fuel-used))
)
