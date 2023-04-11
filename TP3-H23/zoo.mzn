% Use this editor as a MiniZinc scratch book
include "globals.mzn";

int: n;
int: m;
int: k;
array[1..m] of int: index_bonus;
array[1..n] of int: size_enclos;
array[1..n, 1..n] of int: edge_matrix;

int: maxSize = max(size_enclos);
int: zoo_size = ceil(sum(size_enclos)*1.2/2);

array[1..n, 1..maxSize] of var -1..zoo_size: zoo_x;
array[1..n, 1..maxSize] of var -1..zoo_size: zoo_y;

int: nCoordinate = n * maxSize;

array[1..nCoordinate] of var int: coordinate = [
    if zoo_x[i, j]=-1 then -i*zoo_size+j
    else zoo_x[i, j]*zoo_size + zoo_y[i, j] endif
    | i in 1..n, j in 1..maxSize
];

% make sure it has the right y output format               
constraint forall(i in 1..n) (
                  if size_enclos[i] != maxSize then
                  forall(j in (size_enclos[i]+1)..maxSize)
                  (zoo_y[i, j]=-1) else 1=1 endif
                  /\
                  forall(j in 1..size_enclos[i])
                  (zoo_y[i, j]!=-1)
                  /\
                  all_different([zoo_y[i, j]| j in 1..size_enclos[i]])      
               );
                  
% make sure it has the right x output format                        
constraint forall(i in 1..n) (
                  if size_enclos[i] != maxSize then
                  forall(j in (size_enclos[i]+1)..maxSize)
                  (zoo_x[i, j]=-1) else 1=1 endif
                  /\
                  forall(j in 1..size_enclos[i])
                  (zoo_x[i, j]!=-1)
               );
% make sure all coordinate are unique           
constraint all_different(coordinate);

function var int: manhattan(var int: x1, var int: y1,
                            var int: x2, var int: y2)
                          =abs(x1-x2) + abs(y1-y2);
                          
function var int: distance_enclos(var int:enclos1, var int:enclos2)
                                  = min([
                                      manhattan(zoo_x[enclos1, i], zoo_y[enclos1, i],
                                                zoo_x[enclos2, j], zoo_y[enclos2, j])
                                      | i,j in 1..maxSize where zoo_x[enclos1, i] != -1 /\ zoo_x[enclos2, j] != -1
                                  ]);
                                  
var int: toMinimize = sum([
        distance_enclos(i, j) * edge_matrix[i, j]
        | i,j in 1..n
]);


var int: distanceMaximalBonus = max([
    distance_enclos(i, j)
  | i, j in 1..m
]);

var int: V = if distanceMaximalBonus <= k then m*m else 0 endif;


%make sure a plot is all connected
constraint forall(i in 1..n) (
            forall(j in 1..(size_enclos[i]-1))
            ( manhattan(zoo_x[i, j], zoo_y[i, j],
                        zoo_x[i, j+1], zoo_y[i, j+1])=1
            )
);
                                 
solve maximize V - toMinimize;

output
  ["Zoo : \n"]  
  
  ++
  
  [
    show(zoo_x[i, j])
      ++ "," ++
    show(zoo_y[i, j])
      ++ "," ++ 
    if j=maxSize then "\n" else "" endif
    | i in 1..n, j in 1..maxSize
  ]