import yaml
import os
import rospkg
def relative_to_abs_path(path):
    if not os.path.isabs(path):
        rospack = rospkg.RosPack()
        pkg_dir = rospack.get_path("segmentation")
        path = os.path.join(pkg_dir,path)
    return path

class ConfigArgs:
    def __init__(self,path: str):
        path = relative_to_abs_path(path)
        if not path:
            raise ValueError("please specify the config path of the segmentation service model")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Config {path} does not exist")

        if path.endswith("yml") or path.endswith("yaml"):
            self._dic = self._parse_from_yaml(path)
        else:
            raise RuntimeError("incorrect config format, should be: yml / yaml")

    def _parse_from_yaml(self,path):
        with open(path, "r") as y:
            dic = yaml.load(y,Loader=yaml.FullLoader)
            return dic

    @property
    def cfg(self) -> str:
        return relative_to_abs_path(self._dic.get('_base_') )

    @property
    def model_path(self) -> str:
        return relative_to_abs_path(self._dic.get('weights') )

    @property
    def aug_pred(self) -> bool:
        return self._dic.get('augment')["aug_pred"]

    @property
    def scales(self) -> bool:
        return self._dic.get('augment')["scales"]

    @property
    def flip_horizontal(self) -> bool:
        return self._dic.get('augment')["flip_horizontal"]

    @property
    def flip_vertical(self) -> bool:
        return self._dic.get('augment')["flip_vertical"]

    @property
    def is_slide(self) -> bool:
        return self._dic.get('slide')["is_slide"]

    @property
    def crop_size(self):
        return self._dic.get('slide')["crop_size"]

    @property
    def stride(self):
        return self._dic.get('slide')["stride"]

    @property
    def custom_color(self) -> list:
        return self._dic.get('custom_color')