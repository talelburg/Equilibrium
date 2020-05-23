from matplotlib import pyplot

from equilibrium.parsers.parsing_manager import ParsingManager


@ParsingManager.parses("depth_image")
def parse_depth_image(snapshot, data_dir_path):
    data = (data_dir_path / "depth_image.bin").read_bytes()
    height, width = snapshot.depth_image.height, snapshot.depth_image.width
    data = [[data[i * width + j] for j in range(width)] for i in range(height)]
    result_path = data_dir_path / "depth_image.jpg"
    pyplot.imshow(data).write_png(str(result_path))
    return result_path
