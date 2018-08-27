# bin/sh
echo "执行recordcount为:$2"
echo "threads:$3"
work="workloads/workloada"
mongodb_url="mongodb.url="$1
recordcount=$2
#for i in 1 10 20 50
#do 
threads=$3
result="y_"$recordcount"_"$threads
#    ./bin/ycsb load mongodb -P $work -p $mongodb_url -p recordcount=$recordcount -threads $threads > result/$result
./bin/ycsb run mongodb -P $work -p $mongodb_url -p recordcount=$recordcount -threads $threads > result/$result
#done
echo "--------------------------------"
echo "处理数据中"
echo "result|Thread|recordcount|Throughput|READ_95|READ_99|UPDATE_95|UPDATE_99|INSERT_95|INSERT_99">lujin.txt
for result in $(ls result/y_*)
do
    Thread=`echo $result|awk -F '_' '{print $3}'`
    recordcount=`echo $result|awk -F '_' '{print $2}'`
    Throughput=`cat $result|awk '/Throughput/{print $3}'`
    READ_95thPercentileLatency=`cat $result|awk '/95thPercentileLatency/&&/READ/{print $3}'`
    READ_99thPercentileLatency=`cat $result|awk '/99thPercentileLatency/&&/READ/{print $3}'`
    UPDATE_95thPercentileLatency=`cat $result|awk '/95thPercentileLatency/&&/UPDATE/{print $3}'`
    UPDATE_99thPercentileLatency=`cat $result|awk '/99thPercentileLatency/&&/UPDATE/{print $3}'`
    INSERT_95thPercentileLatency=`cat $result|awk '/95thPercentileLatency/&&/INSERT/{print $3}'`
    INSERT_99thPercentileLatency=`cat $result|awk '/99thPercentileLatency/&&/INSERT/{print $3}'`
    echo "$result|$Thread|$recordcount|$Throughput|$READ_95thPercentileLatency|$READ_99thPercentileLatency|$UPDATE_95thPercentileLatency|$UPDATE_99thPercentileLatency|$INSERT_95thPercentileLatency|$INSERT_99thPercentileLatency">>lujin.txt
done
echo "请打开lujin.txt查看结果"
