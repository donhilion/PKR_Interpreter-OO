__author__ = 'Donhilion'

diverses = '''
    {
        var x = 5;
        var f =
            function(a,b) {
                print a;
                print b;
                return 42;
                print 23
            };
        print x;
        var z = f(2,x);
        print z;

        var o = object {
            field1 = 15;
            field2 = 23;
            fun = function(x) {
                return x+this.field1;
            };
            test = function() {
                return o.field1;
            };
            ob = object {
                inner = 42;
            };
        };
        print o.field1;
        print o.fun(4);
        print o.ob.inner;
        print o.test();
    }'''

heap_and_string = '''
    {
        var m = alloc();
        *m := 42;
        print m;
        print *m;
        var string = "Test";
        print string;
    }'''

fibonacci = '''
    {
        var fib = function(x) {
            var i = 0;
            var erg = 1;
            var last = 0;
            var temp = 0;
            while i < x {
                temp := erg;
                erg := erg + last;
                last := temp;
                i := i + 1;
            };
            return erg;
        };
        print fib(5);
    }
    '''

read_line = '''
    {
        print "Geben Sie etwas ein";
        var input = readline();
        var output = "Hallo " + input;
        print output;
    }'''
