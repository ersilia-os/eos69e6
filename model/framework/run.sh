if [ -f /usr/bin/conda/envs/eos69e6 ]; then
    export LD_LIBRARY_PATH=/usr/bin/conda/envs/eos69e6/lib:$LD_LIBRARY_PATH
else
    export LD_LIBRARY_PATH=/eos69e6/lib:$LD_LIBRARY_PATH
fi
num_samples=10
cwd=$(realpath "$1")
input_file=$(realpath "$2")
cd $1/code/PGMG/
python generate_pharmacophores.py $input_file $num_samples
file_count=$(find "$cwd/tmp/" -type f | wc -l)
echo "$file_count"
for ((i = 0; i < file_count; i++))
do
    python generate.py "../../tmp/pharm_$i.edgep" "../../tmp/result_$i" weights/chembl_fold0_epoch32.pth weights/tokenizer.pkl --filter --device cpu --n_mol 1000
done
cd $cwd
python $1/code/assemble_results.py $2 $num_samples $3
rm -r $1/tmp