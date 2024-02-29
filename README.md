# Machine Learning Development

- [Virtual environment](#virtual-environment)
- [Install dependencies](#install-dependencies)
- [Start the Flask server](#start-the-flask-server)
  - [Send a `curl` command](#send-a-curl-command)
- [`docker-compose`](#docker-compose)
  - [Testing with Postman](#testing-with-postman)
- [Docker Hub](#docker-hub)
- [Remove Docker images and containers](#remove-docker-images-and-containers)
- [Pull the image from Docker Hub and run](#pull-the-image-from-docker-hub-and-run)

## Virtual environment <a name="virtual-environment"></a>

```bash
conda create -n your_env_name python=3.11 -y  # create a virtual environment
conda activate your_env_name  # activate your virtual environment
```

## Install dependencies <a name="install-dependencies"></as>

```bash
cd app/api  # head to where the requirements.txt is located
conda install --file requirements.txt -y   # install dependencies
```

## Start the Flask server <a name="start-the-flask-server"></a>

```bash
python app.py
```

### Send a `curl` command <a name="send-a-curl-command"></a>

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "May the Force be with you."}' 0.0.0.0:5000/predict

{
    "label": "Positive",
    "pred": 1,
    "text": "May the Force be with you."
}
```

## `docker-compose` <a name="docker-compose"></a>

Build the image then run the container based on that image.

```bash
docker compose up --build
```

### Testing with Postman <a name="testing-with-postman"></a>

1. Change the request method to `POST` and set the endpoint to `http://localhost:5000/predict` in Postman.

2. Under the `Headers` tab, type `Content-Type` for the key and `application/json` for the value.

3. Under the `Body` tab, select `raw` and enter the following:

   ```
   {
       "text": "May the Force be with you."
   }
   ```

4. Hit send and you will see the same output as above during production

## Docker Hub <a name="docker-hub"></a>

```bash
docker compose push
```

## Remove Docker images and containers <a name="remove-docker-images-and-containers"></a>

```bash
docker images  # view all images
docker rmi -f <IMAGE_ID>  # remove image
docker ps -a  # list all containers
docker rm -f <CONTAINER_ID>  # remove container
```

## Pull the image from Docker Hub and run <a name="pull-the-image-from-docker-hub-and-run"></a>

Now that your local is clean, let's confirm that we successfully pushed the Docker image into Docker Hub by running the following:

```bash
docker run -p5000:5000 your_username/your_app_name
```

You can follow the same steps above and test with Postman to confirm that it is working as expected.
