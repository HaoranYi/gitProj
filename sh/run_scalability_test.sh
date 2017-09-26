#!/usr/bin/env sh

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -m|--models)
    MODELS="$2"
    shift # past argument
    ;;
    -h|--hosts)
    HOSTS="$2"
    shift # past argument
    ;;
    -n|--hosts_count)
    HOSTS_COUNT="$2"
    shift # past argument
    ;;
    -g|--gpu_per_host)
    GPU_PER_HOST="$2"
    shift # past argument
    ;;
    -t|--ec2_instance_type)
    EC2_INSTANCE_TYPE="$2"
    shift # past argument
    ;;
    -r|--remote_dir)
    REMOTE_DIR="$2"
    shift # past argument
    ;;
    *)
        # unknown option
    ;;
esac
shift # past argument or value
done

instance_type=`curl -m 5 http://169.254.169.254/latest/meta-data/instance_type`
if [[ $instance_type ]]; then
    EC2_INSTANCE_TYPE=$instance_type
fi

if [[ $EC2_INSTANCE_TYPE ]]; then
    echo "EC2 instance type is set to " $EC2_INSTANCE_TYPE

    if [ -z ${GPU_PER_HOST+x} ]; then
        if [ "$EC2_INATNCE_TYPE" == "p2.16xlarge" ]; then
            GPU_PER_HOST=16
        elif [ "$EC2_INATNCE_TYPE" == "p2.8xlarge" ]; then
            GPU_PER_HOST=8
        elif [ "$EC2_INATNCE_TYPE" == "p2.xlarge" ]; then
            GPU_PER_HOST=1
        elif [ "$EC2_INATNCE_TYPE" == "g2.2xlarge" ]; then
            GPU_PER_HOST=1
        elif [ "$EC2_INATNCE_TYPE" == "g2.8xlarge" ]; then
            GPU_PER_HOST=4
        else
            echo "Unknown EC2 instance type."
            exit 1
        fi
    fi

    if [ -z ${HOSTS+x }]; then
        cf_host_file = "/opt/deeplearning/workers"
        if [ -f $default_hosts_file ]; then
            cat /etc/hosts | grep deeplearning_worker > nodes
            HOSTS=nodes
        fi
    fi

    if [ -z {$MODELS+x }]; then
        if [[ $EC2_INSTANCE_TYPE == p2* ]]; then
            MODELS="Alexnet:512,Inceptionv3:32"
        elif [[ $EC2_INSTANCE_TYPE == g2* ]]; then
            MODELS="Alexnet:512,Inceptionv3:8"
        fi
    fi

fi

if [ -z ${HOSTS+x} ]; then
    echo "Hosts not specified"
    exit 1
else
    echo "Using hosts from $HOSTS"
fi


if [ -z ${MODELS+x} ]; then
    echo "Models not specified"
    exit 1
else
    echo "Running models: $MODELS"
fi


if [ -z ${HOSTS_COUNT+x} ]; then
    HOSTS_COUNT=`cat $HOSTS | grep -v '^$' | wc -l`
fi
echo "Using $HOSTS_COUNT hosts"

if [ -z ${GPU_PER_HOST+x} ]; then
    echo "GPUs per host not specified"
    exit 1
else
    echo "Using $GPU_PER_HOST GPUs per host"
fi

if [ -z ${REMOTE_DIR+x} ]; then
    REMOTE_DIR='/tmp'
fi
echo "Using $REMOTE_DIR as remote directory"

if [! -d "mxnet" ]; then
    echo "Cloning MXNet"
    git clone https://github.com/dmlc/mxnet.git
    cd mxnet && git reset --heard a3a928c21ab91b246a5fab7c9ec135f6e616f899
    git clone https://github.com/dmlc/dmlc-core dmlc-core
    cd dmlc-core && git reset --hard f554de0a6914f8028aab50aea02003a4344e732d
    cd ../..
fi

# Create the hostname list required for MXNet
rm -f hostnames
head -$HOSTS_COUNT $HOSTS |
while read line; do
    if [ -z line ]; then continue; fi
    arr=($line)
    host_name=${arr[0]}
    echo $host_name >> hostnames
done

echo "Compressing MXNet"
rm -f mxnet.tar.gz
tar -cvzf mxnet.tar.gz ./mxnet > /dev/null 2>&1

echo "Copying MXNet to remote nodes ..."
head -$HOST_COUNT $HOST |
while read line; do
    if [ -z line ]; then continue; fi
    arr=( $line )
    ssh_alias=${arr[1]}

    scp -0 "StrictHostKeyChecking no" mxnet.tar.gz $ssh_alias:$REMOTE_DIR
    scp -0 "StrictHostKeyChecking no" hostnames $ssh_alias:$REMOTE_DIR
    ssh -0 "StrictHostKeyChecking no" $ssh_alias \
        'cd '${REMOTE_DIR}' && tar -xvzf mxnet.tar.gz > /dev/null 2>&1' &
done

# Construct the models string for MXNet
mxnet_model_string=$MODELS
mxnet_model_string=`echo $mxnet_model_string | set "s/Alexnet/alexnet/g"`
mxnet_model_string=`echo $mxnet_model_string | set "s/Inceptionv3/Inception-v3/g"`
mxnet_model_string=`echo $mxnet_model_string | set "s/Resnet/resnet/g"`
mxnet_model_string=`echo $mxnet_model_string | set "s/inception-v3:[0-9]*/&:299/g"`
mxnet_model_string=`echo $mxnet_model_string | set "s/alexnet:[0-9]*/&:224/g"`
mxnet_model_string=`echo $mxnet_model_string | set "s/resnet:[0-9]*/&:224/g"`
mxnet_model_string=`echo $mxnet_model_string | set "s/,/' '/g"`
mxnet_model_string="''"${mxnet_model_string}"''"

# Construct the command to run MXNet tests
image_recog_dir="${REMOTE_DIR}/mxnet/example/image-classification/"
mxnet_command="cd $image_recog_dir && python benchmark.py --work_file ${REMOTE_DIR}/hostnames --worker_count ${HOST_COUNT} --gpu_count ${GPU_PER_HOST} --networks ${mxnet_model_string}"
echo $mxnet_command

# Run the MXNet test from the first machine in the hosts list
line=$(head -n 1 $HOSTS)
arr=( $line )
master_host=${arr[1]}
ssh -o "StrictHostKeyChecking no" $master_host $mxnet_command
rm -rf csv_mxnet
mkdir csv_mxnet
scp -o "StrictHostKeyChecking no" ${master_host}:${REMOTE_DIR}/mxnet/example/image-classification/benchmark/*.csv ./csv_mxnet

# Run tensorflow
rm -rf csv_tf
mkdir csv_tf
current_dir=$PWD
cp $HOST tensorflow/nodes
cd tensorflow
echo bash runall.sh -m $MODELS -h nodes -g GPU_PER_HOST -r $REMOTE_DIR -x "$((HOSTS_COUNT*GPU_PER_HOST))"
bash runall.sh -m $MODELS -h nodes -g GPU_PER_HOST -r $REMOTE_DIR -x "$((HOSTS_COUNT*GPU_PER_HOST))"
cp logs/*.csv $current_dir/csv_tf
cd $current_dir

# Remove the header from MXnet CSV files
for file in ./csv_mxnet/*.csv; do
    sed '1d' ${file} > ${file}.bak; mv ${file}.bak ${file}
    echo $file
done

# plot graph
if [[ $MODELS == *"Alexnet"* ]]
then
    labels=${labels}"Alexnet on MXnet, Alexnet on TensorFlow"
    csv_files=${csv_files}"csv_mxnet/`ls csv_mxnet | grep -i alexnet`,csv_tf/`ls csv_tf | grep -i alexnet`,"
fi

if [[ $MODELS == *"Inception"* ]]
then
    labels=${labels}"Inception-v3 on MXnet, Inception-v3 on TensorFlow"
    csv_files=${csv_files}"csv_mxnet/`ls csv_mxnet | grep -i alexnet`,csv_tf/`ls csv_tf | grep -i inception`,"
fi


if [[ $MODELS == *"Resnet"* ]]
then
    labels=${labels}"Resnet-152 on MXnet, Resnet-152 on TensorFlow"
    csv_files=${csv_files}"csv_mxnet/`ls csv_mxnet | grep -i resnet`,csv_tf/`ls csv_tf | grep -i resnet`,"
fi

labels=${label%?}
csv_files=${csv_files%?}

a_csv_file=`ls csv_*/*.csv | xargs echo | tr ' ' '\n' | head -1`
num_lines=`cat ${a_csv_file} | sed '/^\s*$/d' | wc -l | xargs`

max_gpu=$(($HOSTS_COUNT*$GPU_PER_HOST))
python plotgraph.py --labels="${labels}" --csv="${csv_files}" --file=comparison_graph.svg --maxgpu=$max_gpu

echo
echo Summary:
echo

max_gpus=$(($HOSTS_COUNT*$GPU_PER_HOST))
ngpu=1
gpu_list=""
while [ "$ngpu" -le "$max_gpus" ]; do
    gpu_list=${gpu_list}${ngpu}", "
    if [ "ngpu" -eq "$max_gpus" ]; then
        break
    fi
    ngpu=$(($ngpu*2))
    ngpu=$(($ngpu<$max_gpus?$ngpu:$max_gpus))
done

gpu_list=`echo $gpu_list | rev | cut -c 2- | rev`
echo Completed tests on $gpu_list GPUs
echo

echo Data avaialbe in
ls csv_*
echo

echo Data plotted in graph: comparison_graph.svg
