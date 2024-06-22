# Kandinsky API tools
This is a quite simple script based on [the official Kandinsky API example](https://fusionbrain.ai/docs/doc/api-dokumentaciya/) that
allows you to create a set number of images and save them.

<img src="images/README.jpg" width="60%" align="center">  

## Get API keys
Get your secret keys from [here](https://fusionbrain.ai/docs/doc/poshagovaya-instrukciya-po-upravleniu-api-kluchami/) by following the instructions


## How to install


```bash
cd /home
git clone https://github.com/Vadimmmz/Sber-Kandinsky-API.git
python -m venv env

# Activate virtual environment for Windows
source env/Scripts/activate

# Activate virtual environment fo for Linux
source env/bin/activate

# install all the libraries that are needed to work
pip install -r requirements.txt

deactivate

# Add .env file
echo 'API_KEY="YOUR_API_KEY"' > .env \
&& echo 'SECRET_KEY="YOU_SECRET_KEY"' >> .env \

```

## Quick start

```python
generate_image(prompt='Кот сидит на столе и смотрит в окно', filename='cat', image_num=3, folder='folder with cat')
```

## Used packages

- requests==2.31.0
- python-dotenv==1.0.1

## License

MIT License
