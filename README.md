# How to set up Development Environment as DataDev

Known as Data Tech-Stack for building OpenData platforms and applications.

Try to use this setup for your projects, doing custom configuration as your application requires.

## Contents
- [General Settings](#general-settings)
- [Data Applications](#data-applications)
- [Data Platforms](#data-platforms)
- [Development](#development)
- [Project Structure](#project-structure)

## General Settings

-As Developer, spending budge of time to mimic from internet and custom your personalized-

- MacOS Package Management `homebrew` 

For Windows or Linux users, you will need to install the following package management as your OS distro: choco, pacman, apt,...

```bash
export HOMEBREW_BREW_GIT_REMOTE="..."  # put your Git mirror of Homebrew/brew here
export HOMEBREW_CORE_GIT_REMOTE="..."  # put your Git mirror of Homebrew/homebrew-core here
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

- Python Package Management

Most of Data Dev are installed and built using Python. PLEASE USE `VENV` and `pip` (virtual environment for different projects) instead global settings.

```bash
python -m pip install --user venv
python -m venv --help

# cd to working directory, and install requirements.txt
cat requirements.txt # Show list of libraries
# Flask
# pymongo
# flask_cors
# kafka-python
# pandas
# pyarrow
# boto3
# snowflake-connector-python

pip install -r requirements.txt
```

- Terminal

Using Oh my zsh!! , build comfortable Terminal Settings because you might work a lot with CLI.

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Change theme settings by:
> echo "ZSH_THEME="agnoster"" >> ~/.zshrc

Or, visit https://github.com/ohmyzsh/ohmyzsh/wiki/Theme

**Recommend to use iTerm2**

Easily intsall Iterm2 by this `brew install iterm2`

Plugins:

1. Install plugins


```bash
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions


git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting

git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting

git clone --depth 1 -- https://github.com/marlonrichert/zsh-autocomplete.git $ZSH_CUSTOM/plugins/zsh-autocomplete
```
2. Change config

```bash
 plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  fast-syntax-highlighting
  zsh-autocomplete
 )
```
3. `source ~/.zshrc`


- Browser

Lightweight, Secure, Private with [Min Browser](https://minbrowser.org/)

- Container Setup for Development

Navigate to `./containers/` and run `docker-compose up`

## Data Applications

-When you're joining a project for building Data SaaS-

### 1. Core Backend

- Flask: [Flask]
- Structured Data: [PostgreSQL]

-[Python3.9.0]

### 2. Frontend

- [Node.js 16]
- [JavaScript]
- [React]

### 3. Additional Tools

- DataOps: [Dbt]
- CI/CD: [GitHub Actions]
- Containerization: [Docker, K8s]
- [Docker Compose]

## Data Platforms

-When you're joining a project for building Data PaaS-

### 1. Storage

- File object storage [MinIO]
- Non-Structured Data: [MongoDB]

### 2. Processing

- Streaming and Batching: [Flink]
- Big Data Processing: [Spark]or [Arrow]

### 3. Warehousing

Free Regiter and do mockup, install CLI

- [Databricks]
- [Snowflake]

### 4. Programming

- Programming OOP & Functions [Scala]
- Backend & Infra [Go]
- Fundamentals Data Engineering and Software Development

### 5. Protocol

- Sync [Rest API]
- ASync [Message Queue]

### 6. Semantic

- Modeling [Power BI] or SuperSet

### 7. Cloud Providers

Any of cloud providers [AWS] , Azure, GCP

### 8. Infrastructure

- Infrastructure as Code [Terraform]
- Monitoring [Grafana]
- Logging [Prometheus] or ELK Stack

## Development

Supporting Development Tools

- VSCode [VSCode]
- Dbeaver [Dbeaver]
- Postman [Postman]
- MongoDB Compass [MongoDb]
- CLI
- OrbStack (Only for Mac users)
- Debugging
- Tree Viewer [$ brew install tree]

## Project Structure

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