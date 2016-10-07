Wikomega
======

#choose top query
perl included.pl <(cat query_sample.txt | awk -F "\|" '{if(NR<100000)print $2}') wikisqldb-stream-header.txt 

