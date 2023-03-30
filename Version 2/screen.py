def change_display(passport_id):
	# First define some constants to allow easy resizing of shapes.
	BORDER = 20
	FONTSIZE = 24

	# Configuration for CS and DC pins (these are PiTFT defaults):
	cs_pin = digitalio.DigitalInOut(board.CE0)
	dc_pin = digitalio.DigitalInOut(board.D21)
	reset_pin = digitalio.DigitalInOut(board.D20)

	# Config for display baudrate (default max is 24mhz):
	BAUDRATE = 24000000

	# Setup SPI bus using hardware SPI:
	spi = board.SPI()

	disp = st7735.ST7735R(spi, rotation=90, cs = cs_pin, dc = dc_pin, rst = reset_pin, baudrate = BAUDRATE)   # 1.8" ST7735R

	# Create blank image for drawing.
	# Make sure to create image with mode 'RGB' for full color.
	if disp.rotation % 180 == 90:
		height = disp.width  # we swap height/width to rotate it to landscape!
		width = disp.height
	else:
		width = disp.width  # we swap height/width to rotate it to landscape!
		height = disp.height

	image = Image.new("RGB", (width, height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	# Draw a green filled box as the background
	draw.rectangle((0, 0, width, height), fill=(0, 255, 0))
	disp.image(image)

	# Draw a smaller inner purple rectangle
	draw.rectangle(
		(BORDER, BORDER, width - BORDER - 1, height - BORDER - 1), fill=(170, 0, 136)
	)

	# Load a TTF Font
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

	# Draw Some Text
	(font_width, font_height) = font.getsize(passport_id)
	draw.text(
		(width // 2 - font_width // 2, height // 2 - font_height // 2),
		passport_id,
		font=font,
		fill=(255, 255, 0),
	)

	# Display image.
	disp.image(image)
