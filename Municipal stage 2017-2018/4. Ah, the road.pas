//
// Решение на 100 баллов
//

program PR;
var x0, y0, r, Xa, Ya, Xb, Yb, l, d , AB, AO, BO, s: real;
    lk: string;
    f,g: text;

begin
  assing(f, 'input.txt')
  reset(f);
  readln(f, x0, y0, r);
  readln(f, Xa, Ya, Xb, Yb);
  close(f);
  
  AB:= sqrt(sqr(Ya-Yb)+sqr(Xa-Xb));
  AO:= sqrt(sqr(Ya-YO)+sqr(Xa-XO));
  BO:= sqrt(sqr(YO-Yb)+sqr(XO-Xb));
  
  s:= (sqr(AO)-sqr(BO)+sqr(AB))/(2*AB);
  d:= sqrt(sqr(AO)-sqr(s));
  l:= 2*sqrt(sqr(r)-sqr(d));
  
  assign(g, 'output.txt');
  rewrite(g);
  writeln(g, l:0:3);
  close(g);
end.
