echo "algo,size,exemplaire,temps" > ./results.csv

for algo in "glouton" "progdyn" "approx"; do
    if [ $algo == "glouton" ] || [ $algo == "approx" ]; then
        for exemplaire in $(ls test_set/GA); do
            t=$(./tp.sh -a $algo -e test_set/GA/${exemplaire} -t)
            echo $algo,$exemplaire,$t
        done
    else
        for exemplaire in $(ls test_set/DP); do
            t=$(./tp.sh -a $algo -e test_set/DP/${exemplaire} -t)
            echo $algo,$exemplaire,$t
        done
    fi
done >> results.csv