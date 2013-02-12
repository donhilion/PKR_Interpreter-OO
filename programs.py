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

prim = '''
    {
        var number = 23;
        var isprim = function(x) {
            if x % 2 == 0 {
                return false;
            };
            var isprim = true;
            var i = 3;
            while i <= x/2 && isprim == true {
                if x % i == 0 {
                    isprim := false;
                };
                i := i + 1;
            };
            return isprim;
        };
        var erg = isprim(number);
        print erg;
    }'''

iftest = '''
    {
        if 1 == 1 || 2 == 1 {
            print "Ja";
        } else {
            print "Nein";
        }
    }'''
