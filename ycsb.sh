#! /bin/sh
mongodb_url="mongodb.url="$1
recordcount=$2
threads=$3
work=$4
insertproportion=$5
ycsb_dir=$6
prometheus_url=$7
result="y_"$recordcount"_"$threads
echo "执行recordcount为:$2"
echo "threads:$3"
if [ $insertproportion -ne 1 ]
then
   $ycsb_dir/bin/ycsb load mongodb -P $work -p $mongodb_url -p recordcount=$recordcount -threads $threads
fi
start_time=`date +'%Y-%m-%d %H:%M:%S'`
#start_time=`date -u -d"+8 hour" +'%Y-%m-%d %H:%M:%S'`
$ycsb_dir/bin/ycsb run mongodb -P $work -p $mongodb_url -threads $threads > result/$result
#done
end_time=`date +'%Y-%m-%d %H:%M:%S'`
#end_time=`date -u -d"+8 hour" +'%Y-%m-%d %H:%M:%S'`
echo "start_time,"$start_time >> result/$result
echo "end_time,"$end_time >> result/$result
echo "--------------------------------"
echo "处理数据中"
echo "start_time|end_start|result|Thread|recordcount|Throughput|READ_95|READ_99|UPDATE_95|UPDATE_99|INSERT_95|INSERT_99|cpu_user max|cpu_user min|cpu_user avg|cpu_sys max|cpu_sys min|cpu_sys avg|cpu_wait max|cpu_wait min|cpu_wait avg|mem_percent max|mem_percent min|mem_percent max">lujin.txt
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
    start_time=`cat $result|awk -F ',' '/start_time/{print $2}'`
    end_time=`cat $result|awk -F ',' '/end_time/{print $2}'`
    monitor=`python monitor.py "$start_time" "$end_time" $prometheus_url`
    monitor_l=`echo $monitor|sed 's/\[//g'|sed 's/\]//g'|awk -F ',' '{print $0"%"}'|sed 's/,/%|/g'|sed 's/ //g'`
    echo "$start_time|$end_time|$result|$Thread|$recordcount|$Throughput|$READ_95thPercentileLatency|$READ_99thPercentileLatency|$UPDATE_95thPercentileLatency|$UPDATE_99thPercentileLatency|$INSERT_95thPercentileLatency|$INSERT_99thPercentileLatency|$monitor_l">>lujin.txt
done
echo "数据处理完成"
#echo "请打开lujin.txt查看结果"