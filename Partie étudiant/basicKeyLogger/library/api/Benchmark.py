""" benchmark of CPU """


import sys

import os

import random

import math

import time

from api.Utilities import *



class Benchmark :

    """ benchmark of CPU """



    # counts of clocks used to measure granularity

    countClock = None
    
    # results

    durationArgumentS = None

    durationCallS = None

    durationClockS = None

    durationFloatS = None

    durationIntegerS = None

    durationLoopS = None

    granularityClockS = None

    lagClockS = None

    stdevClockS = None

    # list of consecutive clocks

    clockList = None

    # list of consecutive deltas

    deltaList = None
    
    # total duration of test

    durationS = None

    # tick method: time.clock or time.time according to OS

    tick = None



    def dummy (

        self,
        a0 = None,
        a1 = None,
        a2 = None,
        a3 = None,
        a4 = None,
        a5 = None,
        a6 = None,
        a7 = None,
        ) :

        """ dummy function used to test calls duration """

        None
        



    def reset ( self ) :

        """ resets results """

        self.countClockS = 0.

        self.durationS = 10.

        self.durationArgumentS = 0.

        self.durationCallS = 0.

        self.durationClockS = 0.

        self.durationFloatS = 0.

        self.durationIntegerS = 0.

        self.durationLoopS = 0.

        self.granularityClockS = 0.

        self.lagClockS = 0.

        self.stdevClockS = 0.

        self.clockList = 20000 * [ 0. ]

        self.deltaList = 20000 * [ 0. ]

        # tick method : according to OS time.time or time.clock (that has different semantics in linux: consumed CPU time)

        if sys.platform == "linux2" : self.tick = time.time

        else : self.tick = time.clock
        

         

    def test (
        
        self,
        duration = None
        ) :

        """ tests the cpu and returns a string. duration is defined as argument (default = 10s) """

        self.reset()

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )

        self.durationS = duration
            
        text = "benchmark" 
        
        text1 = self.testLoop( duration / 10. ) 

        text2 = self.testClock( duration / 10. )

        text3 = self.testGranularity( duration / 10. )

        text4 = self.testInteger( duration / 10. )

        text5 = self.testFloat( duration / 10. )

        text6 = self.testCall( duration / 10. )

        text7 = self.testArguments( duration / 10. )

        text = text + "\n" + \
               "  " + text1 + "\n" + \
               "  " + text2 + "\n" + \
               "  " + text3 + "\n" + \
               "  " + text4 + "\n" + \
               "  " + text5 + "\n" + \
               "  " + text6 + "\n" + \
               "  " + text7               
        
        return text



    def testArguments (
        
        
        self,
        duration = None
        ) :

        """ tests the time of calls as a function of the number of arguments

            duration is defined as argument (default = 10s)

            returns a string.

            """

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )
            
        text = "function_argument"

        # loop with 2 calls
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count1 = 0

        while self.tick() < t2 :

            self.dummy(
                a0 = count1
                )

            count1 = count1 + 1

        
        # loop with 4 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count2 = 0

        while self.tick() < t2 :

            self.dummy(
                a0 = count2,
                a1 = count2,
                a2 = count2,
                a3 = count2
                )
            
            count2 = count2 + 1

        
        # loop with 8 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count3 = 0

        while self.tick() < t2 :

            self.dummy(
                a0 = count3,
                a1 = count3,
                a2 = count3,
                a3 = count3,
                a4 = count3,
                a5 = count3,
                a6 = count3,
                a7 = count3,
                )
            
            count3 = count3 + 1


        # approximates cost of passing argument  as follows
        # t = duration / 3.
        # t ~ ( tloop + tclock * 1 ) * count1               (e1)
        # t ~ ( tloop + tclock * 4 ) * count2           (e2)
        # t ~ ( tloop + tclock * 8 ) * count3           (e3) 
        #
        # sistem (e1, e2) : tclock ~ ( count1-count2 ) * t /  ( 3. * count1 * count2 )
        # sistem (e2, e3) : tclock ~ ( count2-count3 ) * t /  ( 4. * count2 * count3 )
        # sistem (e1, e3) : tclock ~ ( count1-count3 ) * t /  ( 7. * count2 * count3 )

        t = duration / 3.

        t1 = float( count1 - count2 ) * t / 3. / float( count1 ) / float( count2 )
        
        t2 = float( count2 - count3 ) * t / 4. / float( count2 ) / float( count3 )       
                    
        t3 = float( count1 - count3 ) * t / 7. / float( count1 ) / float( count3 )

        # average
        
        t123 = ( t1 + t2 + t3 ) / 3.

        self.callArgumentS = t123

        # average in microseconds, precision = 10-8

        t123 = int( t123 * 100000000. )

        t123 = float( t123 ) / 100.
        
        text = text + " " + str( t123 ) + " mus"

##        text = text + " " + \
##               str( t1 ) + " " + \
##               str( t2 ) + " " + \
##               str( t3 ) + " " + \
##               str( t123 ) + " mus"

        return text


    def testCall (
        
        
        self,
        duration = None
        ) :

        """ tests the cpu and returns a string. duration is defined as argument (default = 10s) """

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )
            
        text = "function_call"

        # loop with 2 calls
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count1 = 0

        while self.tick() < t2 :

            self.dummy( count1 )

            self.dummy( count1 )

            count1 = count1 + 1

        
        # loop with 4 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count2 = 0

        while self.tick() < t2 :

            self.dummy( count2 )

            self.dummy( count2 )
            
            self.dummy( count2 )

            self.dummy( count2 )
            
            count2 = count2 + 1

        
        # loop with 8 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count3 = 0

        while self.tick() < t2 :

            self.dummy( count3 )

            self.dummy( count3 )
            
            self.dummy( count3 )

            self.dummy( count3 )
            
            self.dummy( count3 )

            self.dummy( count3 )
            
            self.dummy( count3 )

            self.dummy( count3 )
            
            count3 = count3 + 1


        # approximates cost of calling self.tick() as follows
        # t = duration / 3.
        # t ~ ( tloop + tclock * 2 ) * count1               (e1)
        # t ~ ( tloop + tclock * 4 ) * count2           (e2)
        # t ~ ( tloop + tclock * 8 ) * count3           (e3) 
        #
        # sistem (e1, e2) : tclock ~ ( count1-count2 ) * t /  ( 2. * count1 * count2 )
        # sistem (e2, e3) : tclock ~ ( count2-count3 ) * t /  ( 4. * count2 * count3 )
        # sistem (e1, e3) : tclock ~ ( count1-count3 ) * t /  ( 6. * count2 * count3 )

        t = duration / 3.

        t1 = float( count1 - count2 ) * t / 2. / float( count1 ) / float( count2 )
        
        t2 = float( count2 - count3 ) * t / 4. / float( count2 ) / float( count3 )       
                    
        t3 = float( count1 - count3 ) * t / 6. / float( count1 ) / float( count3 )

        # average
        
        t123 = ( t1 + t2 + t3 ) / 3.

        self.callDurationS = t123

        # average in microseconds, precision = 10-8

        t123 = int( t123 * 100000000. )

        t123 = float( t123 ) / 100.
        
        text = text + " " + str( t123 ) + " mus"

##        text = text + " " + \
##               str( t1 ) + " " + \
##               str( t2 ) + " " + \
##               str( t3 ) + " " + \
##               str( t123 ) + " mus"

        return text

    
        



    def testClock (
        
        
        self,
        duration = None
        ) :

        """ tests the cpu and returns a string.

            duration is defined as argument (default = 10s)

            """

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )
            
        text = "clock_call"
        

        # loop with clock call and increment
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count1 = 0

        while self.tick() < t2 :

            count1 = count1 + 1

            
        # loop with 4 clock calls and increment
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count2 = 0

        while self.tick() < t2 :

            self.tick()

            self.tick()

            self.tick()

            count2 = count2 + 1
            
            
        # loop with 8 clock calls and increment
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count3 = 0

        while self.tick() < t2 :

            self.tick()

            self.tick()

            self.tick()

            self.tick()

            self.tick()

            self.tick()

            self.tick()

            count3 = count3 + 1

        # approximates cost of calling self.tick() as follows
        # t = duration / 3.
        # t ~ ( tloop + tclock ) * count1               (e1)
        # t ~ ( tloop + tclock * 4 ) * count2           (e2)
        # t ~ ( tloop + tclock * 8 ) * count3           (e3) 
        #
        # sistem (e1, e2) : tclock ~ ( count1-count2 ) * t /  ( 3. * count1 * count2 )
        # sistem (e2, e3) : tclock ~ ( count2-count3 ) * t /  ( 4. * count2 * count3 )
        # sistem (e1, e3) : tclock ~ ( count1-count3 ) * t /  ( 7. * count2 * count3 )

        t = duration / 3.

        t1 = float( count1 - count2 ) * t / 3. / float( count1 ) / float( count2 )
        
        t2 = float( count2 - count3 ) * t / 4. / float( count2 ) / float( count3 )       
                    
        t3 = float( count1 - count3 ) * t / 7. / float( count1 ) / float( count3 )

        # average
        
        t123 = ( t1 + t2 + t3 ) / 3.

        self.clockDurationS = t123

        # average in microseconds, precision = 10-8

        t123 = int( t123 * 100000000. )

        t123 = float( t123 ) / 100.

        
        text = text + " " + str( t123 ) + " mus"

##               str( t1 ) + " " + \
##               str( t2 ) + " " + \
##               str( t3 ) + " " + \
##               str( t123 ) + " mus"

        return text
        





    def testFloat (
        
        self,
        duration = None
        ) :

        """ tests the cpu and returns a string.

            duration is defined as argument (default = 10s)

            """

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )
            
        text = "float_mul_div"

        # loop with 2 multiplications /divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        i = 1.

        count1 = 0

        while self.tick() < t2 :

            i = i * i

            i = i / i

            i = i + 1.

            count1 = count1 + 1

        
        # loop with 4 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count2 = 0

        i = 1.

        while self.tick() < t2 :

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i + 1.
            
            count2 = count2 + 1

        
        # loop with 8 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count3 = 0

        i = 1.

        while self.tick() < t2 :

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i + 1.
            
            count3 = count3 + 1


        # approximates cost of calling self.tick() as follows
        # t = duration / 3.
        # t ~ ( tloop + tclock * 2 ) * count1               (e1)
        # t ~ ( tloop + tclock * 4 ) * count2           (e2)
        # t ~ ( tloop + tclock * 8 ) * count3           (e3) 
        #
        # sistem (e1, e2) : tclock ~ ( count1-count2 ) * t /  ( 2. * count1 * count2 )
        # sistem (e2, e3) : tclock ~ ( count2-count3 ) * t /  ( 4. * count2 * count3 )
        # sistem (e1, e3) : tclock ~ ( count1-count3 ) * t /  ( 6. * count2 * count3 )

        t = duration / 3.

        t1 = float( count1 - count2 ) * t / 2. / float( count1 ) / float( count2 )
        
        t2 = float( count2 - count3 ) * t / 4. / float( count2 ) / float( count3 )       
                    
        t3 = float( count1 - count3 ) * t / 6. / float( count1 ) / float( count3 )

        # average
        
        t123 = ( t1 + t2 + t3 ) / 3.

        self.integerDurationS = t123

        # average in microseconds, precision = 10-8

        t123 = int( t123 * 100000000. )

        t123 = float( t123 ) / 100.
        
        text = text + " " + str( t123 ) + " mus"

##        text = text + " " + \
##               str( t1 ) + " " + \
##               str( t2 ) + " " + \
##               str( t3 ) + " " + \
##               str( t123 ) + " mus"

        return text




    def testGranularity (

        
        self,
        duration = None
        ) :

        """ tests the cpu and returns a string.

            duration is defined as argument (default = 10s)

            """

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )
            
        text = "granularity"

        size = len( self.clockList )

        rangeClock = range( 1, size )

        count = 0

        sumt = 0.

        sumt2 = 0.

        maxt = 0.

        t1 = self.tick() + duration

        while self.tick() < t1 :

            # fills array with consecutive time clocks

            self.clockList[ 0 ] = self.tick()

            i = 0

            while i + 1 < size :

                t = self.tick()

                # change of time

                if t > self.clockList[ i ] :

                    i = i + 1

                    self.clockList[ i ] = t

            # creates an array of deltas and updates statistics
            
            for i in rangeClock :

                delta = self.clockList[ i ] - self.clockList[ i - 1 ]

                self.deltaList[ i ] = delta

                count = count + 1

                sumt = sumt + delta

                sumt2 = sumt2 + delta * delta

                maxt = max( maxt, delta )
                
        
        # error case
        
        if count <= 0 : return text

        count = float( count )
        
        average = sumt / count

        variance = sumt2 / count - average * average

        if variance < 0. : variance = 0.

        stdev = math.sqrt( variance )

        maximum = maxt

        self.countClockS = count

        self.granularityClockS = average

        self.stdevClockS = stdev

        self.lagClockS = maximum

        # in microseconds, resolution 10-8

        average = int( average * 100000000. )

        average = float( average ) / 100.

        stdev = int( stdev * 100000000. )

        stdev = float( stdev ) / 100.
        
        maximum = int( maximum * 100000000. )

        maximum = float( maximum ) / 100.
        
        text = text + " " + \
               str( average ) + " mus " + \
               "cnt " + str( int( count ) ) + " " + \
               "stdev " + str( stdev ) + " " + \
               "max " + str( maximum )

        return text
    


    def testInteger (
        
        self,
        duration = None
        ) :

        """ tests the cpu and returns a string.

            duration is defined as argument (default = 10s)

            """

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )
            
        text = "integer_mul_div"
        
        # loop with 2 multiplications /divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        i = 1

        count1 = 0

        while self.tick() < t2 :

            i = i * i

            i = i / i

            i = i + 1

            count1 = count1 + 1

        
        # loop with 4 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count2 = 0

        i = 1

        while self.tick() < t2 :

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i + 1
            
            count2 = count2 + 1

        
        # loop with 8 multiplications / divisions
        
        t1 = self.tick()

        t2 = t1 + duration / 3.

        count3 = 0

        i = 1

        while self.tick() < t2 :

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i * i

            i = i / i

            i = i + 1
            
            count3 = count3 + 1


        # approximates cost of calling self.tick() as follows
        # t = duration / 3.
        # t ~ ( tloop + tclock * 2 ) * count1               (e1)
        # t ~ ( tloop + tclock * 4 ) * count2           (e2)
        # t ~ ( tloop + tclock * 8 ) * count3           (e3) 
        #
        # sistem (e1, e2) : tclock ~ ( count1-count2 ) * t /  ( 2. * count1 * count2 )
        # sistem (e2, e3) : tclock ~ ( count2-count3 ) * t /  ( 4. * count2 * count3 )
        # sistem (e1, e3) : tclock ~ ( count1-count3 ) * t /  ( 6. * count2 * count3 )

        t = duration / 3.

        t1 = float( count1 - count2 ) * t / 2. / float( count1 ) / float( count2 )
        
        t2 = float( count2 - count3 ) * t / 4. / float( count2 ) / float( count3 )       
                    
        t3 = float( count1 - count3 ) * t / 6. / float( count1 ) / float( count3 )

        # average
        
        t123 = ( t1 + t2 + t3 ) / 3.

        self.integerDurationS = t123

        # average in microseconds, precision = 10-8

        t123 = int( t123 * 100000000. )

        t123 = float( t123 ) / 100.
        
        text = text + " " + str( t123 ) + " mus"

##        text = text + " " + \
##               str( t1 ) + " " + \
##               str( t2 ) + " " + \
##               str( t3 ) + " " + \
##               str( t123 ) + " mus"


        return text
    




    def testLoop (
        
        self,
        duration = None
        ) :

        """ tests the time of a while loop (the slowest) and returns a string.

            duration is defined as argument (default = 10s)

            """

        if not type( duration ) == float : duration = utilities.float( duration, default = 10. )
            
        text = "loop"

        # loop with clock calls for first estimate
        
        t1 = self.tick()

        t2 = t1 + duration / 2.

        count1 = 0

        while True :

            if self.tick() >= t2 : break

            count1 = count1 + 1

        # loop without clock calls

        count2 = 0

        count3 = 10 * count1

        t1 = self.tick()

        while count2 < count3 :

            count2 = count2 + 1

        t2 = self.tick()

        # approximates cost of loop as follows
        # t = t2 - t1
        # t ~ tloop * count3 / 10.                      (e1)

        t = ( t2 - t1 ) / count3

        self.loopDurationS = t

        # average in microseconds, precision = 10-8
        
        t = int( t * 100000000. )

        t = float( t ) / 100.

        text = text + " " + str( t ) + " mus"

        return text
    


    
# creates singleton

if not "benchmark" in globals() : benchmark = Benchmark()
    
