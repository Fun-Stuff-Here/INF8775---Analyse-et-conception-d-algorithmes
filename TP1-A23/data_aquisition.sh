echo "algo,size,exemplaire,temps" > ./results.csv

for algo in "conv" "strassen" "strassenSeuil"; do
    for testset_folder_size in $(ls testset); do
        for exemplaire in $(ls testset/${testset_folder_size}); do
            t=$(./tp.sh -a $algo -e1 testset/${testset_folder_size}/${exemplaire} -e2 testset/${testset_folder_size}/${exemplaire} -t)
            echo $algo,$testset_folder_size,$exemplaire,$t
        done
    done
done >> results.csv