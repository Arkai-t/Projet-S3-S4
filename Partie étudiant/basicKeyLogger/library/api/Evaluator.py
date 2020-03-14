
""" Class that evaluates expressions
 
   
    """


from api.Utilities import *


class Evaluator :


    """ Class that evaluates expressions
  
        """


    # comparison operators

    comparisonList = [
        "==",
        "=",
        "<>",
        "!=",
        ">=",
        ">",
        "<=",
        "<",
        "startswith",
        "endswith",
        "contains"
        ]


    # list of logical connectors and sintactic keywords

    connectorList = [
        "not",
        "!",
        "and",
        "&&",
        "or",
        "||",
        ]

    # error message

    error = None
    
    # current expression

    expression = None

    # list of possible states or conditions for widgets

    functionList = [
        "alpha",        # the value of widget is alphabetical 
        "alphanum",     # the value is alphanumerical
        "defined",      # value is defined (non empty)
        "digit",        # the value is a sequence of digits
        "empty",        # the value is empty or undefined
        "float",        # value is a float
        "integer",      # value is an integer
        "present",      # path is present
        ]

    # index in current expression

    iEval = None

    # list of arithmetic operators

    operationList = [
        "+",
        "-",
        "/",
        "*",
        "and",
        "or",
        "not",
        "==",
        "<",
        "<=",
        ">",
        ">=",
        "max",
        "min"
        ]

    # optimizes the variable references

    optimize = True

    # level of parenthesis for expressions

    parenthesisLevel = None


    # list of keywords of expressions

    reservedList = [
        "(",
        ")",
        "?",
        ":"
        "then",
        "else"
        ]
    


    def __init__ (

        self,
        ) :

        """ Constructor """

        None
        



    def errorExpression (

        self,
        text = None
        ) :

        """ Registers an error in expression evaluation """


        expression = utilities.listToText( self.expression )

        self.error = " Expression - " + \
                     expression + \
                     " - " + \
                     utilities.string( text, default = "error" ).strip()



    def evalAction ( 

        self,
        expression = None,
        index = None,
        parenthesis = None,
        execute = None,
       

        ) :

        """ Evaluates an action and executes it if "execute" is True
        
            expression is a sequence of words or a string . Defaut expression is self.expression
            index is the position in the expression. Default is self.iEval

            Normalizes the elements of the terms at first pass.
            context variables are replaced to indexes in the list of context variables
            etc.

            """

        # default = global expression, default index = 0

        if not expression is None : self.expression = expression

        if not index is None : self.iEval = index

        # converts from string to list of words ( removes extreme spaces & delimiters before split )
        
        if type( self.expression ) == str : self.expression = utilities.textToWords( self.expression, leaveEmpty = False )

        # empty list of words

        if utilities.isEmpty( self.expression ) : return False

        # out of range

        if not utilities.isIndex( self.iEval, self.expression ) : return False

        word = self.expression[ self.iEval ]

        self.iEval = self.iEval + 1



        # no context ? no variables

        if utilities.context is None :

            return False

        # the index of a context variable

        elif ( ( type( word ) == int ) and ( word >= 0 ) ) :

            try :

                variable = self.variableList[ word ]

            except Exception, exception :

                return False
            
        # looks in list of patterns of context variables. replaced by the index of variable for next evaluation

        elif word in self.patternList :

            index = self.patternList.index( word )

            variable = self.variableList[ index ]

            # normalizes for next evaluation
            
            self.substituteConstant( index )
            
        # looks in list of context variables. replaced by the index of variable for next evaluation

        elif word in self.variableList :

            index = self.variableList.index( word )

            variable = word

            # normalizes for next evaluation
            
            self.substituteConstant( index )
            
        # left term is not a variable

        else :

            return False

        # operator or function

        if not utilities.isIndex( self.iEval, self.expression ) : return False

        value = self.expression[ self.iEval ]

        self.iEval = self.iEval + 1

        if value == "=" :

            if not utilities.isIndex( self.iEval, self.expression ) : return False

            value = self.expression[ self.iEval ]

            self.iEval = self.iEval + 1

        # assigns

        if ( ( value.lower() == "none" ) or ( value == "()" ) or ( value == "(none)" ) ) : value = ""

        else : value = utilities.instantiate( value )

        if bool( execute ) : self.setVariable( variable, value )

        return True
    




    def evalComparison (

        self,
        leftValue = None,
        comparison = None,
        rightValue = None
        
        ) :

        """ evaluates a comparison between 2 terms

            returns a 4 uple result ( T F None ), left, operation, right in case they were modified
            
            """

        
        if ( ( leftValue is None ) or ( rightValue is None ) or ( comparison is None ) ) : return None


        result = None
                

        # string operators

        if comparison == "startswith"  : result = leftValue.startswith( rightValue )

        if comparison == "endswith" : result = leftValue.endswith( rightValue )

        if comparison == "contains" : result = ( rightValue in leftValue )

    
        if not result is None : return result, leftValue, comparison, rightValue

        
        # tries to convert the values to compare into integers ( both terms )

        i1 = utilities.integer( leftValue )

        i2 = utilities.integer( rightValue )

        if ( ( not i1 is None ) and ( not i2 is None ) ) :

            leftValue = i1

            rightValue = i2

        # tries to convert to floats

        else :

            f1 = utilities.float( leftValue )

            f2 = utilities.float( rightValue )

            if ( ( not f1 is None ) and ( not f2 is None ) ) :

                leftValue = f1

                rightValue = f2

        

        # checks the comparison

        if ( ( comparison == "=" ) or ( comparison == "==" ) ) : result = ( leftValue == rightValue )

        elif ( ( comparison == "!=" ) or ( comparison == "<>" ) ) : result = ( not leftValue == rightValue )

        elif comparison == "<"  :  result = ( leftValue < rightValue )

        elif comparison == "<="  : result = ( leftValue <= rightValue )

        elif comparison == ">"  : result = ( leftValue > rightValue )

        elif comparison == ">="  : result = ( leftValue >= rightValue )


        return result, leftValue, comparison, rightValue


    
    def evalConstant (

        self,
        word = None
        
        ) :

        """ evaluates a constant term and

            returns a pair result( True False or None), argument , in case it was modified """

        result = None

        # a reference that was unsolved at previous evaluation

        if word is None : result = False
        
        # true or 1 -> continue ( the expression is true )
        
        elif ( ( word == "true" ) or ( word == "TRUE" ) or ( word == "1" ) ) :

            # normalizes for next evaluation

            self.substituteConstant( "true" )

            result = True

        # false or zero, the expression is false

        elif ( ( word == "false" ) or ( word == "FALSE" ) or ( word == "0" ) ) :

            # normalizes for next evaluation

            self.substituteConstant( "false" )

            result =  False

        return result, word

        
        
        
    def evalExpression (

        self,
        expression = None,
        index = None,
        parenthesis = None,
        ) :

        """ evaluates a condition ( list of words ) and returns True / False

            Empty conditions return the default value True

            """

        # sets the lists of variables and patterns

        self.setVariableList()
        
        # default = global expression, default index = 0

        if not expression is None : self.expression = expression

        if not index is None : self.iEval = index

        else : self.iEval = 0

        # converts from string to list of words ( removes extreme spaces & delimiters before split )
        
        if type( self.expression ) == str : self.expression = utilities.textToWords( self.expression, leaveEmpty = False )

        # empty list of words

        if utilities.isEmpty( self.expression ) : return True

        # default index = 0

        if not utilities.isIndex( self.iEval, self.expression ) : self.iEval = 0

        size = len( self.expression )

        # default parenthesis level

        if not parenthesis is None : self.parenthesisLevel = parenthesis

        else : self.parenthesisLevel = 0


        # reads and evaluates the expression from left to right accepts flat logical operators,
        # only one level not x , x or y, x and y. No parentheses.
        # scope of not is next expression, scope of and and of or = expression before (from beginning to AND), 1 after


        # global result is True, default logical operator = conjunction (AND), does not expect any term

        result = True

        connector = ""

        expected = False

        negation = False

        action = None

        while True :

            # breaks at the end ( no intermediate break, coz of the flat syntax of OR AND )

            if self.iEval >= size :

                # ends in the middle of a logical expression

                if expected :

                    self.errorExpression( "truncated expression" )

                    result = False

                    break

                # lack or excess of parenthesis

                if not self.parenthesisLevel == 0 :

                    self.errorExpression( "parenthesis do not match [" + utilities.string( self.parenthesisLevel ) + "]" )

                    result = False

                    break

                break


            # current word
            
            word = self.expression[ self.iEval ]

            # closing parenthesis

            if word == ")" :

                self.iEval = self.iEval + 1

                self.parenthesisLevel = self.parenthesisLevel - 1

                if self.parenthesisLevel == 0 : break

                continue

            # ? means that the following is a sequence of actions to execute if result is true

            if ( ( word == "?" ) or ( word == "then" ) ) :

                action = True

                self.iEval = self.iEval + 1

                continue


            # : means that the following is a sequence of actions to execute if result is false

            if ( ( word == ":" ) or ( word == "else" ) ) :

                action = False

                self.iEval = self.iEval + 1

                continue


            # we are in a block of actions TRUE

            if action == True :

                self.evalAction( execute = result )

                continue
            
            # we are in a block of actions FALSE
            
            if action == False :

                self.evalAction( execute = not result )

                continue

                
            # we are in a NOT x y .. ( multiple NOTs not allowed )

            if ( ( word == "not" ) or ( word == "!" ) ) :

                self.iEval = self.iEval + 1

                # embbedded expressions are forbidden
                
                if negation :

                    self.errorExpression( "NOT : multiple NOTs not allowed" )

                    result = False

                    break
                
                negation = True

                expected = True

                continue


            elif ( ( word == "or" ) or ( word == "||" ) ):

                self.iEval = self.iEval + 1

                # OR is not allowed after a  NOT, OR AND
                
                if expected :
                    
                    self.errorExpression( "OR : embedded connectors not allowed" )

                    result = False

                    break

                connector = "or"

                expected = True

##                # beginning of expression was true: no need to evaluate the remainder
##
##                if result : break

                continue

            elif ( ( word == "and" ) or ( word == "&&" ) ) :

                self.iEval = self.iEval + 1

                # AND is not allowed after NOT OR AND
                               
                if expected :

                    self.errorExpression( "AND : embedded connectors not allowed" )

                    result = False

                    break

                connector = "and"

                expected = True

##                # beginning of expression was false : no need to evaluate the remainder
##
##                if not result : break

                continue

            # other cases : nothing is expected after current term
            
            else :

                expected = False


            # parenthesis : increments level and skips

            if word == "(" :

                self.iEval = self.iEval + 1

                self.parenthesisLevel = self.parenthesisLevel + 1

                term = self.evalExpression(
                    index = self.iEval,
                    parenthesis = self.parenthesisLevel
                    )

                

            # evaluates current term, increases self.iEval

            else :

                term = self.evalTerm()

            # it was a negation

            if negation :

                term = not term

                negation = False

            # propagates previous result

            if connector == "or" : result = result or term

            else : result = result and term

        return result
    





    def evalFunction (

        self,
        word = None,
        operation = None
        ) :

        """ evaluates general operations on the word

            returns a 3-uple result( True False or None), argument and operation (in case they were modified) """


        # default result is None

        result = None
        
        if operation == "alpha" :

            if not utilities.isEmpty( word ) : result = word.isalpha()

            else : result = False

        if operation == "alphanum" :

            if not utilities.isEmpty( word ) : result = word.isalnum()

            else : result = False

        if operation == "defined" :

            result = not utilities.isEmpty( word )


        if operation == "digit" :

            if not utilities.isEmpty( word ) : result = word.isdigit()

            else : result = False

        if operation == "float" :

            if utilities.isEmpty( word ) : result = False

            try :

                value = float( word )

                result = True

            except Exception, exception :

                result = False


        if operation == "integer" :

            if utilities.isEmpty( word ) : result = False

            try :

                value = int( word )

                result = True

            except Exception, exception :

                result = False


        if operation == "present" :

            if utilities.isEmpty( word ) : result = False

            else : result = utilities.pathPresent( word )


        if operation == "empty" :

            if utilities.isEmpty( word ) : result = True

            else : result = utilities.pathSize( word ) <= 0


        return result, word, operation


        


    def evalFunctionExternal (

        self,
        word = None,
        operation = None
        ) :

        """ evaluates a unary term, external hook. Default procedure resolves left argument

            note. iEval is already placed after the unary term ARG FCT

            returns a 3-uple result (True False None) , the argument and the operation in case they were modified
            
            """

        # the index of a context variable

        if ( ( type( word ) == int ) and ( word >= 0 ) ) :

            word = self.getVariable( self.variableList[ word ] )
            
        # looks in list of patterns of context variables. replaced by the index of variable for next evaluation

        elif word in self.patternList :

            index = self.patternList.index( word )

            # normalizes for next evaluation
            
            evaluator.substituteArgument( index )

            word = self.getVariable( self.variableList[ index ] )
        
        # replaces variable by its value

        else :

            word = utilities.string( word, default = "" )

        word = utilities.instantiate( word, default = "" )

        return None, word, operation


    def evalNumeric(

        self,
        expression = None,
        index = None,
        parenthesis = None,
        ) :

        """ evaluates a numerical expression( list of words ) and returns a float

            Empty conditions return the default value 0.

            """

        # sets the lists of variables and patterns

        self.setVariableList()
        
        # default = global expression, default index = 0

        if not expression is None : self.expression = expression

        if not index is None : self.iEval = index

        else : self.iEval = 0

        # converts from string to list of words ( removes extreme spaces & delimiters before split )
        
        if type( self.expression ) == str : self.expression = utilities.textToWords( self.expression, leaveEmpty = False )

##        print "evalNumeric expression[", self.iEval, ":] = ", self.expression[ self.iEval : ]

        # empty list of words

        if utilities.isEmpty( self.expression ) : return 0.


        # default index = 0

        if not utilities.isIndex( self.iEval, self.expression ) : self.iEval = 0

        size = len( self.expression )

        # default parenthesis level

        if not parenthesis is None : self.parenthesisLevel = parenthesis

        else : self.parenthesisLevel = 0


        # reads and evaluates the expression from left to right accepts flat logical operators,
        # only one level not x , x or y, x and y. No parentheses.
        # scope of not is next expression, scope of and and of or = expression before (from beginning to AND), 1 after


        # global result is True, default logical operator = conjunction (AND), does not expect any term

        result = None

        operation = ""

        expected = False

        while True :

            # breaks at the end ( no intermediate break, coz of the flat syntax of OR AND )

            if self.iEval >= size :

                # ends in the middle of a logical expression

                if expected :

                    self.errorExpression( "truncated expression" )

                    return 0.

                # lack or excess of parenthesis

                if not self.parenthesisLevel == 0 :

                    self.errorExpression( "parenthesis do not match [" + utilities.string( self.parenthesisLevel ) + "]" )

                    return 0.

                break


            # current word & value
            
            word = self.expression[ self.iEval ]

##            print "  ", self.iEval, word, "previous result", result, " operation ", operation

            # closing parenthesis . weird

            if word == ")" :

                self.iEval = self.iEval + 1

                self.parenthesisLevel = self.parenthesisLevel - 1

                if self.parenthesisLevel == 0 : break

                continue


            if word in self.operationList :

                self.iEval = self.iEval + 1

                # compound operations
                
                if operation == "-" :

                    if word == "-"  : operation = ""

                    elif word == "+" : operation = "-"

                    else : word = None

                elif operation == "+" :

                    if word == "-"  : operation = "-"

                    elif word == "+" : operation = "+"

                    else : word = None

                if word is None :
                    
                    self.errorExpression( operation + " : consecutive operations" )

                    return 0.

                operation = word

                expected = True

                continue

            # not an operation : expects nothing
            
            expected = False


            # parenthesis : increments level and skips

            if word == "(" :

                self.iEval = self.iEval + 1

                self.parenthesisLevel = self.parenthesisLevel + 1

                term = self.evalNumeric(
                    index = self.iEval,
                    parenthesis = self.parenthesisLevel
                    )

            # a float, normally
            
            else :
                

                # evaluates current term, increases self.iEval


                term = utilities.float( word )

                if term is None : term = utilities.float( self.getVariable( word ) )

                self.iEval = self.iEval + 1


            # error in evaluation
            
            if term is None :

                self.errorExpression( word + " : invalid number" )

                return 0.

            # propagates previous result

            if operation == "" : result = term

            elif operation == "max" :

                if result is None : result = term

                else : result = max( result, term )

            elif operation == "min" :

                if result is None : result = term

                else : result = min( result, term )

            elif operation == "and" :

                if result is None : result = utilities.boolean( term )

                else : result = utilities.boolean( result ) and utilities.boolean( term )

            elif operation == "or" :

                if result is None : result = utilities.boolean( term )

                else : result = utilities.boolean( result ) or utilities.boolean( term )

            elif operation == "not" :

                result = not utilities.boolean( term )

            elif operation == "==" :

                if result is None : result = utilities.boolean( term )

                else : result = ( result == term )


            elif operation == "<" :

                if result is None : result = utilities.boolean( term )

                else : result = ( result < term )


            elif operation == ">" :

                if result is None : result = utilities.boolean( term )

                else : result = ( result > term )


            elif operation == "<=" :

                if result is None : result = utilities.boolean( term )

                else : result = ( result <= term )


            elif operation == ">=" :

                if result is None : result = utilities.boolean( term )

                else : result = ( result >= term )
                
            elif operation == "+" :

                if result is None : result = term

                else : result = result + term

            elif operation == "-" :

                if result is None : result = - term

                else : result = result - term
                
            elif operation == "*" :

                if result is None : result = term

                else : result = result * term

            elif operation == "/" :

                if result is None : result = term

                elif term == 0. : result = 0.

                else : result = result / term

            operation = ""

        return float( result )
    

        

    def evalTerm ( 

        self,
        expression = None,
        index = None,
        parenthesis = None

        ) :

        """ Evaluates a term of a logical condition.
        
            expression is a sequence of words or a string . Defaut expression is self.expression
            index is the position in the expression. Default is self.iEval

            Normalizes the elements of the terms at first pass
            widgets are replaced by pointer to actual widget
            context variables are replaced to indexes in the list of context variables
            etc.

            """

        # default = global expression, default index = 0

        if not expression is None : self.expression = expression

        if not index is None : self.iEval = index

        # converts from string to list of words ( removes extreme spaces & delimiters before split )
        
        if type( self.expression ) == str : self.expression = utilities.textToWords( self.expression, leaveEmpty = False )

        # empty list of words

        if utilities.isEmpty( self.expression ) : return False

        # out of range

        if not utilities.isIndex( self.iEval, self.expression ) : return False

        word = self.expression[ self.iEval ]

        self.iEval = self.iEval + 1

        result, word = self.evalConstant( word )

        if not result is None : return result

        # operator or function is missing

        if not utilities.isIndex( self.iEval, self.expression ) : return False

        left = word

        operation = self.expression[ self.iEval ]

        self.iEval = self.iEval + 1

        # evaluates unary term on word, operator and returns a word ( modified ) and a result, or None None

        result, left, operation = self.evalFunctionExternal( left, operation )

        if not result is None : return result

        result, left, operation = self.evalFunction( left, operation )

        if not result is None : return result

        # here, we have a comparison, identifier comp value or identifier value

        if operation in self.comparisonList :

            comparison = operation

            if not utilities.isIndex( self.iEval, self.expression ) : return False

            right = utilities.instantiate( self.expression[ self.iEval ] )

            self.iEval = self.iEval + 1

        else :

            comparison = "="

            right = utilities.instantiate( operation )

        result, left, operation, right = self.evalComparison( left, comparison, right )

        return result



    def getVariable (

        self,
        variable = None,
        default = ""
        ) :

        """ returns the value of a variable. this method can be overwritten """

        return utilities.getVariable( variable, default )

    

    def set (
        
        self,
        externalFunction = None
        ) :

        """ sets the method to evaluate external functions """

        if callable( externalFunction ) : self.evalFunctionExternal = externalFunction



        
    def setVariableList ( self ) :

        """ initializes the lists of variables. this method can be overwritten """

        self.variableList = utilities.context.variableList

        self.patternList = utilities.context.patternList

        

    def setVariable (

        self,
        variable = None,
        value = None
        ) :

        """ sets the value of a variable. this method can be overwritten """

        return utilities.setVariable( variable, value )

    
        

    def substituteArgument (

        self,
        value = None
        ) :

        """ substitutes the argument of an expression by the value ( for on the flight compilation ) """

        if not bool( self.optimize ) : return

        if value is None : return

        if not utilities.isIndex( self.iEval - 2, self.expression ) : return

        self.expression[ self.iEval - 2 ] = value




    def substituteConstant (

        self,
        value = None
        ) :

        """ substitutes a constant by the value ( for on the flight compilation ) """

        if not bool( self.optimize ) : return

        if value is None : return

        if not utilities.isIndex( self.iEval - 1, self.expression ) : return

        self.expression[ self.iEval - 1 ] = value




    def substituteFunction (

        self,
        value = None
        ) :

        """ substitutes the function of an expression by the value ( for on the flight compilation ) """

        if not bool( self.optimize ) : return

        if value is None : return

        if not utilities.isIndex( self.iEval - 1, self.expression ) : return

        self.expression[ self.iEval - 1 ] = value



        
    def substituteLeft (

        self,
        value = None
        ) :

        """ substitutes the left argument of an expression by the value ( for on the flight compilation ) """

        if not bool( self.optimize ) : return

        if value is None : return

        if not utilities.isIndex( self.iEval - 3, self.expression ) : return

        self.expression[ self.iEval - 3 ] = value



        

    def substituteOperation (

        self,
        value = None
        ) :

        """ substitutes the operator of an infixedexpression by the value ( for on the flight compilation ) """

        if not bool( self.optimize ) : return

        if value is None : return

        if not utilities.isIndex( self.iEval - 2, self.expression ) : return

        self.expression[ self.iEval - 2 ] = value



    def substituteRight (

        self,
        value = None
        ) :

        """ substitutes the right argument of an expression by the value ( for on the flight compilation ) """

        if not bool( self.optimize ) : return

        if value is None : return

        if not utilities.isIndex( self.iEval - 1, self.expression ) : return

        self.expression[ self.iEval - 1 ] = value

        


        
# -----------------------------------
# creates the global singleton object if not already here
#

if not "evaluator" in globals() : evaluator = Evaluator()
         
        
