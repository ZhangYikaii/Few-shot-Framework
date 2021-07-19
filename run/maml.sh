python ../main.py \
    --gpu 15 \
    --max_epoch 50 \
    --episodes_per_train_epoch 400 \
    --episodes_per_val_epoch 40 \
    --model_class MAML \
    --dataset MiniImageNet \
    --train_way 5 --test_way 5 \
    --shot 1 --test_shot 1 \
    --query 5 --test_query 5 \
    --logger_filename /logs \
    --loss_fn F-cross_entropy \
    --lr 0.0001 --lr_mul 10 --lr_scheduler step \
    --step_size 20 \
    --gamma 0.5 \
    --val_interval 1 \
    --test_interval 2 \
    --meta \
    --order 1 \
    --meta_batch_size 4 \
    --inner_train_steps 5 \
    --inner_val_steps 10 \
    --inner_lr 0.01 \
    --verbose