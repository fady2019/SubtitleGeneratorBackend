# CS50x Subtitle Generator (Backend)

## Video Demo

## Description

This is the backend of CS50x Subtitle Generator. It's my final project for CS50x course, offered by Harvard University. CS50x Subtitle Generator is a web application that facilitates the process of generating subtitles with support for multiple languages.

## Subtitle Generation Step-By-Step

![SubtitleGeneratorStepByStep](https://github.com/user-attachments/assets/e1c2bb13-444c-44b3-b8fb-3970e4733494)

## Database Schema

![SubtitleGeneratorERD](https://github.com/user-attachments/assets/1e949937-1154-4a38-8eb8-d0d949948a3d)

## Installation

1. **Setup WSL** (if you don't use linux already)
    - [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
    - [Install Ubuntu Terminal](https://www.microsoft.com/store/productId/9PDXGNCFSCZV?ocid=pdpshare)
2. **Setup Python** (v3.12)
    - `sudo apt update && sudo apt upgrade -y`
    - `sudo add-apt-repository ppa:deadsnakes/ppa` _(provides the newer versions of python)_
    - `sudo apt update` _(update package lists after adding a new repo ("deadsnakes"))_
    - `sudo apt install python3.12` _(install python3.12)_
    - `python3.12 --version` _(ensure that python3.12 installed)_
3. **Setup Virtual Environment**
    - open the project in ubuntu terminal
    - `python3.12 -m venv .venv` _(create a virtual environment)_
    - `. .venv/bin/activate` _(activate the virtual environment)_
4. **Setup Packages**
    - `sudo apt install ffmpeg`
    - `pip3.12 install -r requirements.txt` _(install the project dependencies)_

## Usage

1. **Start Server**
    - `python3.12 app.py`
2. **Start Celery**
    - `celery -A app.celery worker -l info` _(start celery worker, it's essential for the subtitle generation task and other async tasks)_
    - `celery -A app.celery beat -l info` _(start celery beat, it's essential for the periodic tasks such as cleaning the expired temporary token from db)_

## Technologies & Packages

<section>
  <kbd title="HTML5">
    <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> 
      <img src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-icon.svg" alt="html5" width="40" height="40"/>
    </a>
  </kbd>
  <kbd title="CSS3">
    <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> 
      <img src="https://www.vectorlogo.zone/logos/w3_css/w3_css-icon.svg" alt="css3" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="Python">
    <a href="https://www.python.org/" target="_blank" rel="noreferrer"> 
      <img src="https://www.vectorlogo.zone/logos/python/python-icon.svg" alt="python" width="40" height="40"/>
    </a>  
  </kbd>
  <kbd title="Flask">
    <a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/devicons/devicon/blob/master/icons/flask/flask-original.svg" alt="flask" width="40" height="40"/>
    </a>  
  </kbd>
  <kbd title="SQLAlchemy">
    <a href="https://www.sqlalchemy.org/" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/devicons/devicon/blob/master/icons/sqlalchemy/sqlalchemy-original.svg" alt="sqlalchemy" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="PostgreSQL">
    <a href="https://www.postgresql.org/" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original.svg" alt="postgresql" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="OpenAI Whisper">
    <a href="https://openai.com/index/whisper/" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/gilbarbara/logos/blob/main/logos/openai-icon.svg" alt="openai-whisper" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="Celery">
    <a href="https://docs.celeryq.dev/" target="_blank" rel="noreferrer"> 
      <img src="https://docs.celeryq.dev/en/stable/_static/celery_512.png" alt="celery" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="Redis">
    <a href="https://redis.io" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/devicons/devicon/blob/master/icons/redis/redis-original.svg" alt="redis" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="PyJWT">
    <a href="https://pyjwt.readthedocs.io/" target="_blank" rel="noreferrer"> 
      <img src="https://jwt.io/img/pic_logo.svg" alt="pyjwt" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="FFmpeg Python">
    <a href="https://python-ffmpeg.readthedocs.io/" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/get-icon/geticon/blob/master/icons/ffmpeg-icon.svg" alt="ffmpeg-python" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="Demucs">
    <a href="https://github.com/facebookresearch/demucs" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/gilbarbara/logos/blob/main/logos/meta-icon.svg" alt="demucs" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="Flasgger">
    <a href="https://github.com/flasgger/flasgger" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/devicons/devicon/blob/master/icons/swagger/swagger-original.svg" alt="swagger" width="40" height="40"/> 
    </a>
  </kbd>
</section>

##### Extra Packages

1. [Voluptuous](https://github.com/alecthomas/voluptuous)
2. [Pydub](https://pydub.com)
3. [Polyglot](https://github.com/aboSamoor/polyglot)

## Tools

<section>
  <kbd title="WSL">
    <a href="https://learn.microsoft.com/en-us/windows/wsl/" target="_blank" rel="noreferrer"> 
      <img src="https://upload.wikimedia.org/wikipedia/commons/4/49/Windows_Subsystem_for_Linux_logo.png" alt="wsl" width="40" height="40"/> 
    </a>
  </kbd>
  <kbd title="Visual Studio Code">
    <a href="https://code.visualstudio.com/" target="_blank" rel="noreferrer"> 
      <img src="https://www.vectorlogo.zone/logos/visualstudio_code/visualstudio_code-icon.svg" alt="vscode" width="40" height="40"/> 
    </a>
  </kbd>
</section>

## Project Folders

<details open>

```
.
├── README.md
├── app.py
├── app_factory.py
├── celery_tasks
│   ├── emails.py
│   ├── subtitle_media_file.py
│   ├── subtitles.py
│   └── temporary_tokens.py
├── db
│   ├── db_config.py
│   ├── entities
│   │   ├── segment.py
│   │   ├── subtitle.py
│   │   ├── temporary_token.py
│   │   └── user.py
│   ├── entity_dicts
│   │   ├── entity_dict.py
│   │   ├── segment_entity_dict.py
│   │   ├── subtitle_entity_dict.py
│   │   ├── temporary_token_entity_dict.py
│   │   └── user_entity_dict.py
│   ├── repositories
│   │   ├── repository
│   │   │   ├── create_repository.py
│   │   │   ├── crud_repository.py
│   │   │   ├── delete_repository.py
│   │   │   ├── find_repository.py
│   │   │   ├── repository.py
│   │   │   ├── repository_typing.py
│   │   │   └── update_repository.py
│   │   ├── segment.py
│   │   ├── subtitle.py
│   │   ├── temporary_token.py
│   │   └── user.py
│   └── utils
│       └── entity_to_dict.py
├── decorators
│   ├── errors
│   │   └── app_error_handler.py
│   ├── input_validator
│   │   ├── __init__.py
│   │   └── input_source.py
│   ├── restrictions
│   │   └── rate_limit.py
│   └── security
│       ├── auth_token.py
│       └── user_subtitle.py
├── dtos
│   ├── dto.py
│   ├── segment.py
│   ├── subtitle.py
│   └── user.py
├── dtos_mappers
│   ├── mapper.py
│   ├── segment.py
│   ├── subtitle.py
│   └── user.py
├── helpers
│   ├── __init__.py
│   ├── audio.py
│   ├── celery.py
│   ├── cookies.py
│   ├── date.py
│   ├── file.py
│   └── jwt.py
├── requirements.txt
├── response
│   ├── response.py
│   └── response_messages.py
├── routes
│   ├── api.py
│   ├── auth.py
│   └── subtitles
│       ├── segments
│       │   ├── segment.py
│       │   └── segments.py
│       ├── subtitle.py
│       └── subtitles.py
├── services
│   ├── auth.py
│   ├── segments.py
│   ├── subtitle_file
│   │   ├── __init__.py
│   │   └── subtitle_file_creator.py
│   └── subtitles.py
├── swagger
│   ├── __init__.py
│   ├── docs
│   │   ├── auth
│   │   │   ├── auto_login.yml
│   │   │   ├── change_password.yml
│   │   │   ├── login.yml
│   │   │   ├── logout.yml
│   │   │   ├── request_email_verification.yml
│   │   │   ├── request_password_reset.yml
│   │   │   ├── reset_password.yml
│   │   │   ├── signup.yml
│   │   │   └── verify_email.yml
│   │   └── subtitles
│   │       ├── begin_generation.yml
│   │       ├── cancel_generation.yml
│   │       ├── delete_subtitle.yml
│   │       ├── edit_subtitle.yml
│   │       ├── fetch_subtitle.yml
│   │       ├── fetch_subtitles.yml
│   │       ├── rebegin_generation.yml
│   │       └── segments
│   │           ├── as_file.yml
│   │           ├── edit_segment.yml
│   │           └── fetch_segments.yml
│   └── template.yml
├── templates
│   └── emails
│       ├── base.html
│       ├── reset_password.html
│       ├── subtitle_generation_completed.html
│       ├── subtitle_generation_failed.html
│       └── verify_email.html
└── validation
    ├── auth.py
    ├── pagination.py
    ├── shared.py
    ├── subtitles.py
    ├── transformers.py
    └── validators.py
```

</details>

## Environment Variables

<details open>

```.env
# SERVER
SERVER_HOST="127.0.0.1"
SERVER_PORT=5000
SERVER_DEBUG=true

# CORS
API_ALLOWED_ORIGINS="http://localhost:5173"
    # separated by ,

# COOKIE
COOKIE_HTTP_ONLY="true"
COOKIE_SAME_SITE="none"
COOKIE_SECURE="true"
# COOKIE_DOMAIN=""

# DATABASE
DATABASE_LOGIN="<db_username>"
DATABASE_PASSWORD="<db_password>"
DATABASE_HOST="<db_host>"
DATABASE_PORT=<db_port>
DATABASE_NAME="<db_name>"

# JWT
JWT_AUTH_TOKEN_EXP_IN_HOURS=24
JWT_AUTH_TOKEN_PUBLIC_KEY="..."
JWT_AUTH_TOKEN_PRIVATE_KEY="..."
JWT_AUTH_TOKEN_TOKEN_COOKIE_NAME="token"

# MAIL
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=465
MAIL_USERNAME="<email>"
MAIL_PASSWORD="<app_password>"
MAIL_SENDER="<email>"
MAIL_USE_TLS="false"
MAIL_USE_SSL="true"

# CLIENT
CLIENT_HOST_URL="http://localhost:5173"

# TEMPORARY TOKEN
TEMP_TOKEN_LENGTH=32
TEMP_TOKEN_EXP_IN_HOURS=1
TEMP_TOKEN_CLEANING_CRONJOB_HOUR="*/6"
    # 1 -> 23

# TEMPORARY FILE PATHS
MEDIA_FILES_TMP_STORAGE_PATH = "tmp/media_files"
MEDIA_FILE_NAME = "media_file"
AUDIO_FILE_NAME = "audio"
TRIMMED_AUDIO_FILE_NAME = "trimmed"
OPTIMIZED_AUDIO_FILE_NAME = "optimized"

# CELERY & REDIS
REDIS_URL="redis://127.0.0.1:6379/0"
CELERY_BROKER_URL="redis://127.0.0.1:6379/0"
CELERY_BACKEND="redis://127.0.0.1:6379/0"

# WHISPER
WHISPER_MODAL="small"
    # see (https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages) for alternatives

# SUBTITLE
MAX_NUMBER_OF_SUBTITLES_PER_USER=5

# DEMUCS
DEMUCS_OUT_DIR_NAME="source_separation"
DEMUCS_CHUNKS_OUT_DIR_NAME="chunks"
DEMUCS_VOCALS_FILE_NAME="vocals"
DEMUCS_MODAL_NAME="htdemucs_ft"
DEMUCS_STEM_NAME="vocals"
```

</details>

## Contact

<section>
  <kbd title="Fady's LinkedIn">
    <a href="https://www.linkedin.com/in/fadygoher/" target="_blank" rel="noreferrer"> 
      <img src="https://github.com/devicons/devicon/blob/master/icons/linkedin/linkedin-original.svg" alt="Fady's LinkedIn" width="40" height="40"/>
    </a>  
  </kbd>
</section>
