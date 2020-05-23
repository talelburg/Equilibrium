from PIL import Image

from equilibrium.parsers.parsing_manager import ParsingManager


@ParsingManager.parses("color_image")
def parse_color_image(snapshot, data_dir_path):
    color_image_data = (data_dir_path / "color_image.bin").read_bytes()
    height, width = snapshot.color_image.width, snapshot.color_image.height
    image = Image.new("RGB", (width, height))
    image.putdata([tuple(color_image_data[3 * i:3 * i + 3]) for i in range(len(color_image_data) // 3)])
    result_path = data_dir_path / "color_image.jpg"
    image.save(str(result_path))
    return {
        "height": height,
        "width": width,
        "data": str(result_path)
    }
