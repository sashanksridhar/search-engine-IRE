#!/bin/bash
#SBATCH -A research
#SBATCH -n 16
#SBATCH --mem-per-cpu=2048
#SBATCH --mincpus=32
#SBATCH --time=72:00:00
#SBATCH --mail-user=sashank.sridhar@research.iiit.ac.in
#SBATCH --mail-type=ALL

echo "Activating virtualenv"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate TripletLoss
mkdir /ssd_scratch/cvit/sashank.sridhar
echo "Generating dataset"
scp -r sashank.sridhar@ada:/share3/sashank.sridhar/IRE/phase2/enwiki-20220820-pages-articles-multistream.xml.bz2 /ssd_scratch/cvit/sashank.sridhar
cd /ssd_scratch/cvit/sashank.sridhar
echo "Extracting"
bzip2 -d enwiki-20220820-pages-articles-multistream.xml.bz2
echo "Get code"
scp -r sashank.sridhar@ada:/share3/sashank.sridhar/IRE/phase2/search-engine-IRE /ssd_scratch/cvit/sashank.sridhar
cd search-engine-IRE
echo "Run code"
python -u indexer.py /ssd_scratch/cvit/sashank.sridhar/enwiki-20220820-pages-articles-multistream.xml /ssd_scratch/cvit/sashank.sridhar/full_index_path /ssd_scratch/cvit/sashank.sridhar/full_index_path/invertedindex_stat.txt
scp -r /ssd_scratch/cvit/sashank.sridhar/full_index_path sashank.sridhar@ada:/share3/sashank.sridhar/IRE/
echo "Done"