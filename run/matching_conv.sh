source activate zykycy
python ../main.py \
    --meta_batch_size 1 \
    --data_path /mnt/data3/lus/zhangyk/data/ye \
    --max_epoch 200 \
    --gpu 14 \
    --model_class MatchingNet \
    --distance cosine \
    --backbone_class Conv4 \
    --dataset MiniImageNet \
    --train_way 5 --val_way 5 --test_way 5 \
    --train_shot 1 --val_shot 1 --test_shot 1 \
    --train_query 15 --val_query 15 --test_query 15 \
    --logger_filename /logs \
    --temperature 64 \
    --lr 0.001 --lr_mul 10 --lr_scheduler step \
    --step_size 10 \
    --gamma 0.3 \
    --val_interval 1 \
    --test_interval 0 \
    --loss_fn nn-cross_entropy \
    --metrics categorical_accuracy \
    --verbose \