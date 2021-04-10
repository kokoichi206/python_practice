## shell
python3 -c "import this" > zen.txt
grep -i beautiful zen.txt 
grep -o Beautiful zen.txt
grep -i ^if zen.txt 
echo 123 hi 34 hello. | grep [[:digit:]]
echo two twoo not too. | grep -o two*
echo __hello__there | grep -o __.*__
echo I love $ | grep \\$

seq 100 | sed '0~3s/[0-9]*$/Fizz/' | sed '0~5s/[0-9]*$/Buzz/'
seq 1 100 | awk '$1 %3 == 0 && $1 %15 != 0 {print "Fizz"} $1 %5 == 0 && $1 %15 != 0 { print "Buzz"} $1 %15 == 0 {print "FizzBuzz"} $1 %3 != 0 && $1 %5 != 0 { print $1 }'
echo 1 2 3 | awk '$1 == 1 {print "oneone"}'


## memo
DRY: Don't Repeat Yourself
直行性: aはbに影響するべきではない


## TO READ
- [Pythonで学ぶアルゴリズム](http://libgen.li/item/index.php?md5=AE007A68C3C7FE1E5ABECBAD87D16703)
- [偉い人の自伝？](http://libgen.li/item/index.php?md5=3E1BB9301F6FB066416F5F5DC3501994)
- [JUST FOR FUN](http://libgen.gs/ads.php?md5=475a6d212223f377cb2c61aff925549a)


- [Hacker Ethic](http://libgen.gs/ads.php?md5=ea50230c67939095c6ca0dbde7ad4445)
- [Linusさんの修論](http://libgen.gs/ads.php?md5=5a9073ee2d3bb0d68f5895857e9cf9ca)
