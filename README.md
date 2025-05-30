# How to set up Development Environment as DataDev

Known as Data Tech-Stack for building OpenData platforms and applications.

Try to use this setup for your projects, doing custom configuration as your application requires.

## Changelog

- 2025-03-01: Change to use Vim for writing, coding; and tmux for splitting terminal.
![tmux-setup](assets/tmux-setup.png)

## Contents

- [General Settings](#general-settings)
- [Data Applications](#data-applications)
- [Data Platforms](#data-platforms)
- [Development](#development)
- [Project Structure](#project-structure)
- [DataPods-OSS](#data-pods-oss)

## Tutorial and Demo

Watch this video to get hands-on [https://youtu.be/2nKRHoWemDQ](https://youtu.be/2nKRHoWemDQ)

![MacbookM1](assets/MacbookM1Setup.png)

## General Settings

*As Developer, spending a lot of time to mimic from internet and custom your personalized*

![Development](assets/GitCli.png)

### MacOS Package Management `homebrew`

For Windows or Linux users, you will need to install the following package management as your OS distro: choco, pacman, apt,...

Normally, I remove all unusual application on Dock/Toolbar/Desktop. Make it lean.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```
Notes: Check `python3 --version` on your machine, if it doesn't have yet ?! Run `brew install python3`

### Python Package Management

Most of Data Dev are installed and built using Python. PLEASE USE `VENV` and `pip` (virtual environment for different projects) instead global settings.

This is an example of libs I mostly use in Data Project

```bash
python3 -m pip install --user venv
python3 -m venv --help

pip3 install -r requirements.txt
```

### Git

```bash
brew install git --cask
```

### Terminal

Using --Oh my zsh!!-- , build comfortable Terminal Settings because you might work a lot with CLI.

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Change theme settings by:
> echo "ZSH_THEME="agnoster"" >> ~/.zshrc

Or visit this to change whatever you want <https://github.com/ohmyzsh/ohmyzsh/wiki/Theme>

**Recommend to use iTerm2**

Easily install iTerm2 by this `brew install iTerm2`

#### Plugins

In order to make your CLI more faster, check these out:

1. Install plugins


```bash
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting

git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting

git clone --depth 1 -- https://github.com/marlonrichert/zsh-autocomplete.git $ZSH_CUSTOM/plugins/zsh-autocomplete
```

1. Change config

```bash
 plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  fast-syntax-highlighting
  zsh-autocomplete
 )
```

3. Run `source ~/.zshrc` to activate change

### Browser

Lightweight, Secure, Private with [Min Browser](https://minbrowser.org/)

### KeyCastr (Optional)

To display the keyboard on the screen

```bash
brew install keycastr --cask
```

### Container Setup for Development

Navigate to `./containers/` and run `docker-compose up`

![Container Setup for Data Engineering](/assets/ContainersSetup.png)

Please remember to utilize your resources, *Don't kill a machine*


### Devbox

- Update on 2025-01-19, change to use devboxfor developement. [devbox](https://github.com/jetify-com/devbox)

### Deployment

- Vercel
- Railway


## Data Applications

*When you're joining a project for building Data SaaS*

### 1. Core Backend

- Flask [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- Structured Data & Simplified Data warehouse [PostgreSQL](https://www.postgresql.org/)
- Data Programming [Python3.9.0](https://www.python.org)

### 2. Frontend

- [Node.js 16](https://nodejs.org/en/) or upper
- [JavaScript](https://www.typescriptlang.org/)
- Web Framework/Library: [React](https://reactjs.org/)
- Rapidly build modern websites [Tailwind CSS](https://tailwindcss.com/)

### 3. Additional Tools

- DataOps: [Dbt](https://www.getdbt.com/)
- CI/CD: [GitHub Actions](https://github.com/features/actions)
- Containerization: [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- K8s: [Kubenetes](https://kubernetes.io/)

## Data Platforms

*When you're joining a project for building Data PaaS*

### 1. Storage

- File object storage - Datalake (using for partition): [MinIO](https://min.io/)
- Non-Structured Data: [MongoDB](https://www.mongodb.com/)

### 2. Processing

- Streaming and Batching: [Flink](https://www.flink.apache.org)
- Big Data Processing: [Spark](https://spark.apache.org/) or [Arrow](https://arrow.apache.org/docs/index.html)

### 3. Warehousing

Free Register and do mockup, install CLI

- [Databricks](https://www.databricks.com/)
- [Snowflake](https://www.snowflake.com/)

### 4. Programming

- Programming OOP & Functions [Scala](https://scala-lang.org/)
- Backend & Infra [Go](https://go.dev/)
- Fundamentals Data Engineering and Software Development

### 5. Protocol

- Sync [Rest API](https://restfulapi.net/)
- ASync [Message Queue](https://kafka.apache.org/)

### 6. Semantic

- Modeling [Power BI](https://powerbi.microsoft.com/en-us/) or SuperSet

### 7. Cloud Providers

Any of cloud providers [AWS] , Azure, GCP

### 8. Infrastructure

- Infrastructure as Code [Terraform](https://www.terraform.io/)
- Monitoring [Grafana](https://grafana.com/)
- Logging [Prometheus](https://prometheus.io/docs/introduction/overview/) or [ELK](https://www.elastic.co/elastic-stack/) Stack

## Development

Supporting Development Tools

- VSCode [VSCode](https://code.visualstudio.com/)
- Dbeaver [Dbeaver](https://dbeaver.com/docs/dbeaver/)
- Postman [Postman](https://www.postman.com/)
- MongoDBCompass [MongDb](https://www.mongodb.com/products/tools/compass)
- CLI
- [OrbStack](https://orbstack.dev/) (Only for Mac users)
- Debugging, Breakpoints, logging
- Tree Viewer [$ brew install tree]

![Monitoring Platforms](/assets/MonitoringInfra.png)

## Project Structure

Create the folders as you need them

```bash
.
├── LICENSE
├── README.md : information about the project
├── app : contains data application
├── devops : contains cicd, infrastructure
├── docs : documentation
├── docusaurus : docs generator
├── run-stringx-platform.sh : master script to run the project
├── servers : contains data servers
└── venv-stringx : py virtual environment
```
If you want to get understanding what data engineering is and trying to achieve fundatmental knowledge about data engineering, check this Youtube Series:

[https://youtu.be/5DEFgEBAuTA?si=KymSgjY-foD8q5I3](https://youtu.be/5DEFgEBAuTA?si=KymSgjY-foD8q5I3)


## DataPods OSS

<sub>If you have been spent late night with data ingestion and data migration</sub>

- This project data project includes lightweight k8s yaml files for creating the development environment, testing environment, Proof of Concept, Proof of Service or even support for **Small Business**.

- With DataPods [DPs],  maximize the number of times to provision services for creating data transformations.

- Supported Scalability and Resiliency by features of Kubernetes.

- Check out [DataPods](https://datapods-oss.vercel.app/)

----------------------------------------------------------------
*I created this setting for my development setup, for contribution please create PR and update your preference*
