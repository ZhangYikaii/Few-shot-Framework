import os, shutil
import os.path as osp
import torch
import numpy as np
from torch.utils.data import DataLoader

def set_seeds(torch_seed, cuda_seed, np_seed):
    torch.manual_seed(torch_seed)
    torch.cuda.manual_seed_all(cuda_seed)
    np.random.seed(np_seed)

def mkdir(dirs):
    """Create a directory, ignoring exceptions

    # Arguments:
        dir: Path of directory to create
    """
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def rmdir(dirs):
    """Recursively remove a directory and contents, ignoring exceptions

   # Arguments:
       dir: Path of directory to recursively remove
   """
    if os.path.exists(dirs):
        shutil.rmtree(dirs)

def get_command_line_parser():
    """解析命令行参数.

    命令行参数说明:
        TODO

    # Arguments
        None
    # Return
        argparse.ArgumentParser(), 还需要 .parse_args() 转.
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='MiniImageNet',
                        choices=['MiniImageNet', 'TieredImageNet', 'CUB', 'OmniglotDataset'])
    parser.add_argument('--distance', default='l2')
    parser.add_argument('--way', type=int, default=5)
    parser.add_argument('--val_way', type=int, default=5)
    parser.add_argument('--test_way', type=int, default=5)
    parser.add_argument('--shot', type=int, default=1)
    parser.add_argument('--test_shot', type=int, default=1)
    parser.add_argument('--query', type=int, default=15)
    parser.add_argument('--test_query', type=int, default=15)
    parser.add_argument('--backbone_class', type=str, default='ConvNet',
                        choices=['ConvNet', 'Res12', 'Res18', 'WRN', 'Linear'])
    
    parser.add_argument('--max_epoch', type=int, default=200)
    parser.add_argument('--num_tasks', type=int, default=4)
    parser.add_argument('--episodes_per_train_epoch', type=int, default=200)
    parser.add_argument('--episodes_per_val_epoch', type=int, default=200)
    parser.add_argument('--episodes_per_test_epoch', type=int, default=5000)
    parser.add_argument('--drop_lr_every', type=int, default=40)
    parser.add_argument('--model_class', type=str, default='ProtoNet', 
                        choices=['MAML', 'MatchNet', 'ProtoNet', 'BILSTM', 'DeepSet', 'GCN', 'FEAT', 'FEATSTAR', 'SemiFEAT', 'SemiProtoFEAT']) # None for MatchNet or ProtoNet
    parser.add_argument('--logger_filename', type=str, default='/logs/process')

    parser.add_argument('--balance', type=float, default=0)
    parser.add_argument('--temperature', type=float, default=1)
    parser.add_argument('--temperature2', type=float, default=1)  # the temperature in the  

    parser.add_argument('--loss_fn', type=str, default='F-cross_entropy',
                        choices=['F-cross_entropy', 'nn-cross_entropy'])

    # optimization parameters
    parser.add_argument('--orig_imsize', type=int, default=-1) # -1 for no cache, and -2 for no resize, only for MiniImageNet and CUB
    parser.add_argument('--lr', type=float, default=0.0001)
    parser.add_argument('--lr_mul', type=float, default=10)
    parser.add_argument('--lr_scheduler', type=str, default='step', choices=['multistep', 'step', 'cosine'])
    parser.add_argument('--step_size', type=str, default='20')
    parser.add_argument('--gamma', type=float, default=0.2)    
    parser.add_argument('--fix_BN', action='store_true', default=False)     # means we do not update the running mean/var in BN, not to freeze BN
    parser.add_argument('--augment', action='store_true', default=False)
    parser.add_argument('--multi_gpu', action='store_true', default=False)
    parser.add_argument('--gpu', default='0')
    parser.add_argument('--init_weights', type=str, default=None)

    # usually untouched parameters
    parser.add_argument('--mom', type=float, default=0.9)
    parser.add_argument('--weight_decay', type=float, default=0.0005) # we find this weight decay value works the best
    parser.add_argument('--num_workers', type=int, default=4)
    parser.add_argument('--log_interval', type=int, default=50)
    parser.add_argument('--val_interval', type=int, default=1)
    parser.add_argument('--test_interval', type=int, default=10)
    parser.add_argument('--save_dir', type=str, default='./checkpoints')

    parser.add_argument('--model_save_dir', type=str, default='/mnt/data3/lus/zhangyk/models')
    parser.add_argument('--test_model_filepath', type=str, default=None)
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--epoch_verbose', action='store_true', default=False)

    parser.add_argument('--torch_seed', type=int, default=929)
    parser.add_argument('--cuda_seed', type=int, default=929)
    parser.add_argument('--np_seed', type=int, default=929)

    # MAML:
    parser.add_argument('--meta', action='store_true', default=False)
    parser.add_argument('--inner_train_steps', type=int, default=1)
    parser.add_argument('--inner_val_steps', type=int, default=3)
    parser.add_argument('--inner_lr', type=float, default=0.4)
    parser.add_argument('--meta_lr', type=float, default=0.001)
    parser.add_argument('--meta_batch_size', type=int, default=1)
    parser.add_argument('--order', type=int, default=1)

    return parser

import pprint
_utils_pp = pprint.PrettyPrinter()
def pprint(x):
    _utils_pp.pprint(x)

def set_logger(filename, logger_name):
    import logging
    logging.basicConfig(
        filename=filename,
        filemode='a',
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S %p'
    )
    return logging.getLogger(logger_name)

def set_gpu(x):
    os.environ['CUDA_VISIBLE_DEVICES'] = x
    assert torch.cuda.is_available()
    torch.backends.cudnn.benchmark = True

    return torch.device('cuda')

def preprocess_args(args):
    """根据命令行参数附加处理.

    添加参数:
        TODO

    # Argument
        args: parser.parse_args()
    # Return
        处理后的args
    """
    # TODO: setup_dirs 应该在这里根据传入参数建.

    set_gpu(args.gpu)
    set_seeds(torch_seed=args.torch_seed, cuda_seed=args.cuda_seed, np_seed=args.np_seed)

    # 添加由数据集决定的参数:
    if args.dataset == 'OmniglotDataset':
        args.num_input_channels = 1
    elif args.dataset == 'MiniImageNet':
        args.num_input_channels = 3

    from datetime import datetime
    args.time_str = datetime.utcnow().strftime('%m%d %H-%M-%S-%f')[:-3]

    # args.params_str = f'{args.model_class}_{args.dataset}_{args.backbone_class}-backbone_{args.distance}' \
    #         f'_{args.way}-way_{args.shot}-shot__{args.test_way}-test-way_{args.test_shot}-test-shot__' \
    #         f'{args.query}-query_{args.test_query}-test-query_{time_str}'
    args.params_str = f'{args.time_str} {args.model_class} {args.dataset} {args.backbone_class}-backbone {args.distance} ' \
            f'{args.way}-way {args.val_way}-val-way {args.shot}-shot {args.query}-query ' \
            f'{args.test_way}-test-way {args.test_shot}-test-shot {args.test_query}-test-query'

    args.train_mode = True if args.test_model_filepath is None else False
    args.model_filepath = f'{args.model_save_dir}/{args.model_class}/{args.params_str}.pth' \
        if args.test_model_filepath is None else args.test_model_filepath
    # 在此之后 test_model_filepath 没有用了, 因为已经传递给model_filepath的.
    args.model_filepath_test_best = f'{args.model_save_dir}/{args.model_class}/test_best/{args.params_str}.pth'

    return args

def create_kshot_task_label(way: int, query: int) -> torch.Tensor:
    """Creates an shot-shot task label.

    Label has the structure:
        [0]*query + [1]*query + ... + [way-1]*query

    # Arguments
        way: Number of classes in the shot-shot classification task
        query: Number of query samples for each class in the shot-shot classification task

    # Returns
        y: Label vector for shot-shot task of shape [query * way, ]
    """

    y = torch.arange(0, way, 1 / query).long() # 很精妙, 注意强转成long了.
    # 返回从 0 ~ way - 1 (label), 每个元素有 query 个(query samples).
    return y