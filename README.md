# 📖 LangChain Chainlit Docker Deployment App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://langchain-chainlit-lab.herokuapp.com/)

![Logo](./assets/genocs-library-logo.png?raw=true)

## 🔧 Features

- Basic Skeleton App configured with `openai` API
- A ChatBot using LangChain and Chainlit
- Integration with langchain csv_agent
- poetry integration for python dependency handler
- Docker Support with Optimisation Cache etc
- Deployment on Google Cloud App Engine
- Deployment on Google Cloud using `Cloud Run`

> Reference repository: https://github.com/Genocs/langchain-streamlit-docker-template

This repo contains an `main.py` file which has a template for a chatbot implementation.

## Adding your chain

To add your chain, you need to change the `load_chain` function in `main.py`.
Depending on the type of your chain, you may also need to change the inputs/outputs that occur later on.

## 💻 Running Locally

1. Clone the repository📂

```bash
git clone https://github.com/Genocs/langchain-chainlit-lab
```

2. Install dependencies with [Poetry](https://python-poetry.org/) and activate virtual environment🔨

If you don't have poetry installed, you can install it with `pip install poetry`.
Add `poetry` to your path.

```bash
# To check if poetry is installed
poetry --version

# To reevaluate the dependencies run
poetry lock

# To install the dependencies
poetry install

# To activate the virtual environment
poetry shell
```

3. Run the Chainlit server🚀

```bash
chainlit run src/main.py
```

Run App using Docker

--------------------

This project includes `dockerfile` to run the app in Docker container. In order to optimise the Docker Image
size and building time with cache techniques, I have follow tricks in below [Article on Medium](
https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0)

Build the docker container

```bash
docker build -t langchain-chainlit-chat-app:latest .
```

To generate Image with `DOCKER_BUILDKIT`, follow below command

```bash
DOCKER_BUILDKIT=1 docker build -t langchain-chainlit-chat-app:latest --target=runtime .
```

1. Run the docker container directly

```bash
docker run -d --name langchain-chainlit-chat-app -p 8000:8000 langchain-chainlit-chat-app 
```

2. Run the docker container using docker-compose (Recommended)

```bash
docker-compose up
```

Deploy App on Google App Engine

--------------------

This app can be deployed on Google App Engine following below steps.

## Prerequisites

Follow below guide on basic Instructions.
[How to deploy Streamlit apps to Google App Engine](https://dev.to/whitphx/how-to-deploy-streamlit-apps-to-google-app-engine-407o)

Below the configurations files:

1. `app.yaml`: A Configuration file for `gcloud`
2. `.gcloudignore` : Configure the file to ignore file / folders to be uploaded

I have adopted `dockerfile` to deploy the app on GCP APP Engine.

```bash
# 1. Initialise & Configure the App
gcloud app create --project=[YOUR_PROJECT_ID]

# 2. Deploy the App using
gcloud app deploy

```

3. Access the App using

https://langchain-chat-app-ex6cbrefpq-ts.a.run.app/

Deploy App on Google Cloud using Cloud Run (RECOMMENDED)

--------------------

This app can be deployed on Google Cloud using Cloud Run following below steps.

## Prerequisites

Follow below guide on basic Instructions.

[How to deploy Streamlit apps to Google App Engine](https://dev.to/whitphx/how-to-deploy-streamlit-apps-to-google-app-engine-407o)

We added below tow configurations files 

1. `cloudbuild.yaml`: A Configuration file for `gcloud`
2. `.gcloudignore` : Configure the file to ignore file / folders to be uploaded

we are going to use `dockerfile` to deploy the app using Google Cloud Run.

1. Initialise & Configure the Google Project using Command Prompt

```bash
gcloud app create --project=[YOUR_PROJECT_ID]
```

2. Enable Services for the Project

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

3. Create Service Account

```bash
gcloud iam service-accounts create langchain-app-cr \
    --display-name="langchain-app-cr"

gcloud projects add-iam-policy-binding langchain-chat \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding langchain-chat \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding langchain-chat \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/run.admin"
```

4. Generate the Docker

```bash
DOCKER_BUILDKIT=1 docker build --target=runtime . -t australia-southeast1-docker.pkg.dev/langchain-chat/clapp/langchain-chainlit-chat-app:latest
```

5. Push Image to Google Artifact's Registry

Create the repository with name `clapp`

```bash
gcloud artifacts repositories create clapp \
    --repository-format=docker \
    --location=australia-southeast1 \
    --description="A Langachain Chainlit App" \
    --async
```

Configure-docker

```bash
gcloud auth configure-docker australia-southeast1-docker.pkg.dev
```

In order to push the `docker-image` to Artifact registry, first create app in the region of choice. 

Check the artifacts locations

```bash
gcloud artifacts locations list
```

Once ready, let us push the image to location

```bash
docker push australia-southeast1-docker.pkg.dev/langchain-chat/clapp/langchain-chainlit-chat-app:latest
```

6. Deploy using Cloud Run

Once image is pushed to Google Cloud Artifacts Registry. Let us deploy the image.

```bash
gcloud run deploy langchain-chat-app --image=australia-southeast1-docker.pkg.dev/langchain-chat/clapp/langchain-chainlit-chat-app:latest \
    --region=australia-southeast1 \
    --service-account=langchain-app-cr@langchain-chat.iam.gserviceaccount.com \
    --port=8000
```

7. Test the App Yourself

You can try the app using below link

https://langchain-chat-app-ex6cbrefpq-ts.a.run.app/

## Report Feedbacks

As `langchain-chainlit-lab` is a template project with minimal example. Report issues if you face any.

## DISCLAIMER

This is a template App, when using with openai_api key, you will be charged a nominal fee depending
on number of prompts etc.

## License

This project is licensed with the [MIT license](LICENSE).

## Changelogs

View Complete [Changelog](https://github.com/Genocs/langchain-chainlit-lab/blob/main/CHANGELOG.md).

## Community

- Discord [@genocs](https://discord.com/invite/fWwArnkV)
- Facebook Page [@genocs](https://facebook.com/Genocs)
- Youtube Channel [@genocs](https://youtube.com/c/genocs)

## Support

Has this Project helped you learn something New? or Helped you at work?
Here are a few ways by which you can support.

- ⭐ Leave a star!
- 🥇 Recommend this project to your colleagues.
- 🦸 Do consider endorsing me on LinkedIn for ASP.NET Core - [Connect via LinkedIn](https://www.linkedin.com/in/giovanni-emanuele-nocco-b31a5169/)
- ☕ If you want to support this project in the long run, [consider buying me a coffee](https://www.buymeacoffee.com/genocs)!

[![buy-me-a-coffee](https://raw.githubusercontent.com/Genocs/langchain-chainlit-lab/main/assets/buy-me-a-coffee.png "buy me a coffee")](https://www.buymeacoffee.com/genocs)

## Code Contributors

This project exists thanks to all the people who contribute. [Submit your PR and join the team!](CONTRIBUTING.md)

[![genocs contributors](https://contrib.rocks/image?repo=Genocs/langchain-chainlit-lab "genocs contributors")](https://github.com/Genocs/langchain-chainlit-lab/graphs/contributors)

## Financial Contributors

Become a financial contributor and help me sustain the project.

**Support the Project** on [Opencollective](https://opencollective.com/genocs)
