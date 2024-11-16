(define (problem marketcount2)
(:domain Trader)
(:objects
            StPetersburg Amsterdam - market
        camel0 - camel
        Food ExpensiveRugs Coffee Cattle Water Cars GummyBears Computers LaminateFloor Copper Footballs Kittens Minerals Gold Platinum DVDs TuringMachines - goods)
(:init

        (= (price Food StPetersburg)    5.2)
        (= (on-sale Food StPetersburg)  12)
        (= (price ExpensiveRugs StPetersburg)    6.8)
        (= (on-sale ExpensiveRugs StPetersburg)  13)
        (= (price Coffee StPetersburg)    22.3)
        (= (on-sale Coffee StPetersburg)  11)
        (= (price Cattle StPetersburg)    10.0)
        (= (on-sale Cattle StPetersburg)  0)
        (= (price Water StPetersburg)    27.2)
        (= (on-sale Water StPetersburg)  10)
        (= (price Cars StPetersburg)    88.0)
        (= (on-sale Cars StPetersburg)  30)
        (= (price GummyBears StPetersburg)    26.3)
        (= (on-sale GummyBears StPetersburg)  0)
        (= (price Computers StPetersburg)    78.3)
        (= (on-sale Computers StPetersburg)  14)
        (= (price LaminateFloor StPetersburg)    54.0)
        (= (on-sale LaminateFloor StPetersburg)  22)
        (= (price Copper StPetersburg)    32.3)
        (= (on-sale Copper StPetersburg)  14)
        (= (price Footballs StPetersburg)    65.2)
        (= (on-sale Footballs StPetersburg)  0)
        (= (price Kittens StPetersburg)    59.6)
        (= (on-sale Kittens StPetersburg)  0)
        (= (price Minerals StPetersburg)    11.6)
        (= (on-sale Minerals StPetersburg)  56)
        (= (price Gold StPetersburg)    37.6)
        (= (on-sale Gold StPetersburg)  5)
        (= (price Platinum StPetersburg)    66.0)
        (= (on-sale Platinum StPetersburg)  61)
        (= (price DVDs StPetersburg)    16.8)
        (= (on-sale DVDs StPetersburg)  0)
        (= (price TuringMachines StPetersburg)    39.2)
        (= (on-sale TuringMachines StPetersburg)  0)

        (= (price Food Amsterdam)    2.8)
        (= (on-sale Food Amsterdam)  18)
        (= (price ExpensiveRugs Amsterdam)    5.6)
        (= (on-sale ExpensiveRugs Amsterdam)  16)
        (= (price Coffee Amsterdam)    18.8)
        (= (on-sale Coffee Amsterdam)  20)
        (= (price Cattle Amsterdam)    4.0)
        (= (on-sale Cattle Amsterdam)  0)
        (= (price Water Amsterdam)    21.2)
        (= (on-sale Water Amsterdam)  25)
        (= (price Cars Amsterdam)    97.6)
        (= (on-sale Cars Amsterdam)  6)
        (= (price GummyBears Amsterdam)    61.2)
        (= (on-sale GummyBears Amsterdam)  26)
        (= (price Computers Amsterdam)    95.2)
        (= (on-sale Computers Amsterdam)  0)
        (= (price LaminateFloor Amsterdam)    61.2)
        (= (on-sale LaminateFloor Amsterdam)  4)
        (= (price Copper Amsterdam)    33.6)
        (= (on-sale Copper Amsterdam)  11)
        (= (price Footballs Amsterdam)    80.8)
        (= (on-sale Footballs Amsterdam)  0)
        (= (price Kittens Amsterdam)    48.8)
        (= (on-sale Kittens Amsterdam)  18)
        (= (price Minerals Amsterdam)    10.3)
        (= (on-sale Minerals Amsterdam)  59)
        (= (price Gold Amsterdam)    36.3)
        (= (on-sale Gold Amsterdam)  8)
        (= (price Platinum Amsterdam)    63.6)
        (= (on-sale Platinum Amsterdam)  3)
        (= (price DVDs Amsterdam)    15.6)
        (= (on-sale DVDs Amsterdam)  0)
        (= (price TuringMachines Amsterdam)    57.2)
        (= (on-sale TuringMachines Amsterdam)  0)
        (= (bought Food ) 0)
        (= (bought ExpensiveRugs ) 0)
        (= (bought Coffee) 0)
        (= (bought Cattle ) 0)
        (= (bought Water ) 0)
        (= (bought Cars ) 0)
        (= (bought GummyBears ) 0)
        (= (bought Computers ) 0)
        (= (bought LaminateFloor ) 0)
        (= (bought Copper ) 0)
        (= (bought Footballs ) 0)
        (= (bought Kittens ) 0)
        (= (bought Minerals ) 0)
        (= (bought Gold ) 0)
        (= (bought Platinum ) 0)
        (= (bought DVDs ) 0)
        (= (bought TuringMachines ) 0)
        (= (drive-cost StPetersburg Amsterdam ) 6.3)
        (= (drive-cost Amsterdam StPetersburg ) 6.3)
        (can-drive StPetersburg Amsterdam)
        (can-drive Amsterdam StPetersburg)
        (at camel0       Amsterdam)
        (= (cash) 100)
        (= (capacity) 20)
        (= (fuel-used) 0)
	(= (fuel) 7.0)
)
(:goal (and
        (>= (cash) 1000)
))
;(:metric minimize (fuel-used)) 
)
