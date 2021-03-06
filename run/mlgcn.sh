source activate zykycy
python ../main.py \
    --do_train \
    --do_test \
    --paradigm classical classical classical \
    --meta_batch_size 1 \
    --data_path /user/zhangyk/ML-GCN/data/coco/data \
    --max_epoch 1 \
    --gpu 12,13,14,15 \
    --model_class ProtoNetPretrainClassifier \
    --distance l2 \
    --backbone_class MLGCN \
    --dataset MiniImageNet \
    --logger_filename /logs \
    --temperature 64 \
    --lr 0.0005 --lr_mul 10 --lr_scheduler step \
    --step_size 50 \
    --batch_size 128 \
    --gamma 0.7 \
    --val_interval 1 \
    --test_interval 0 \
    --loss_fn nn-cross_entropy \
    --epoch_verbose \
    --verbose