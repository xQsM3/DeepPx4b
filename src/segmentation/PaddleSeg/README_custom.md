train:

python train.py --config /home/linx123-rtx/PaddleSeg/configs/pp_liteseg/pp_liteseg_stdc1_hannasscapes_small_1024x512_scale0.5_160k.yml --do_eval --use_vdl --save_interval 500 --save_dir output/pp_liteset_hannascapes

predict:

python predict.py --config /home/linx123-rtx/PaddleSeg/configs/pp_liteseg/pp_liteseg_stdc1_hannasscapes_small_1024x512_scale0.5_160k.yml --model_path /home/linx123-rtx/PaddleSeg/output/pp_liteset_hannascapes/best_model/model.pdparams --image_path /home/linx123-rtx/PaddleSeg/docs/images/GAZEBOTEST_5 --save_dir /home/linx123-rtx/PaddleSeg/output/result/GAZEBOTEST5
