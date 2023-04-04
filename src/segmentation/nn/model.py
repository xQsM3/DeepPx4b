from PaddleSeg.predict import get_test_config
from PaddleSeg.paddleseg.utils import get_sys_env, logger, get_image_list
from PaddleSeg.paddleseg.cvlibs import manager, Config
from PaddleSeg.paddleseg.transforms import Compose
from PaddleSeg.paddleseg import utils
from PaddleSeg.paddleseg.utils import logger, progbar, visualize
from PaddleSeg.paddleseg.core import infer
import paddle

import numpy as np

from utils.visualize import addcolor
class DeviceUnavailabeError(Exception):
    "raised when device is not reachable"
    pass

class NN:
    def __init__(self,args):
        self.args = args
        self.check_machine()
        if not args.cfg:
            raise RuntimeError("no cfg specified for model")

        cfg = Config(args.cfg)
        self.model = cfg.model
        self.transforms = Compose(cfg.val_transforms)
        self.test_config = get_test_config(cfg, args)
        utils.load_entire_model(self.model,args.model_path)
        self.model.eval()
        self.color_map = visualize.get_color_map_list(256, custom_color=args.custom_color)


    def check_machine(self):
        env_info = get_sys_env()

        if self.args.device == 'gpu' and env_info[
            'Paddle compiled with cuda'] and env_info['GPUs used']:
            place = 'gpu'
        elif self.args.device == 'xpu' and paddle.is_compiled_with_xpu():
            place = 'xpu'
        elif self.args.device == 'npu' and paddle.is_compiled_with_npu():
            place = 'npu'
        else:
            place = 'cpu'

        paddle.set_device(place)
        print(f"set device: {place}")
        if place != self.args.device:
            raise DeviceUnavailabeError(f"device {self.args.device} not reachable")

    def __call__(self,im):
        with paddle.no_grad():
            ori_shape = im.shape[:2]
            im,_ = self.transforms(im)
            im = im[np.newaxis, ...]
            im = paddle.to_tensor(im)

            if self.args.aug_pred:
                pred, _ = infer.aug_inference(
                    self.model,
                    im,
                    ori_shape=ori_shape,
                    transforms=self.transforms.transforms,
                    scales=self.args.scales,
                    flip_horizontal=self.args.flip_horizontal,
                    flip_vertical=self.args.flip_vertical,
                    is_slide=self.args.is_slide,
                    stride=self.args.stride,
                    crop_size=self.args.crop_size)
            else:
                pred, _ = infer.inference(
                    self.model,
                    im,
                    ori_shape=ori_shape,
                    transforms=self.transforms.transforms,
                    is_slide=self.args.is_slide,
                    stride=self.args.stride,
                    crop_size=self.args.crop_size)
            pred = paddle.squeeze(pred)
            pred = pred.numpy().astype('uint8')

            #pred_mask = utils.visualize.get_pseudo_color_map(pred, self.color_map)
            #colored_pred = addcolor(pred,color_map=self.color_map)

            return pred#np.array(colored_pred)
