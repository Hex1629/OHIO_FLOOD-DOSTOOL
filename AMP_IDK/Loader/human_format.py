from typing import List, Union

class HumanBytes:
    METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB","RB","QB"]
    BINARY_LABELS: List[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    PRECISION_OFFSETS: List[float] = [0.5, 0.05, 0.005, 0.0005, 0.00005]
    PRECISION_FORMATS: List[str] = ["{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}", "{}{:.4f} {}", "{}{:.5f} {}"]
    @staticmethod
    def format(num: Union[int, float], metric: bool=False, precision: int=1) -> str:
        assert isinstance(num, (int, float))
        assert isinstance(metric, bool)
        assert isinstance(precision, int) and precision >= 0 and precision <= 3
        unit_labels = HumanBytes.METRIC_LABELS if metric else HumanBytes.BINARY_LABELS
        last_label = unit_labels[-1]
        unit_step = 1000 if metric else 1024
        unit_step_thresh = unit_step - HumanBytes.PRECISION_OFFSETS[precision]
        is_negative = num < 0
        if is_negative:
            num = abs(num)
        for unit in unit_labels:
            if num < unit_step_thresh:
                break
            if unit != last_label:
                num /= unit_step
        return HumanBytes.PRECISION_FORMATS[precision].format("-" if is_negative else "", num, unit)