# CS50x Subtitle Generator (Backend)

## Video Demo

## Description

This is the backend of CS50x Subtitle Generator. It's my final project for the CS50x course, offered by Harvard University. CS50x Subtitle Generator is a web application that facilitates the process of generating subtitles with support for multiple languages. The process is fully asynchronous, allowing users to upload media files without waiting for subtitles to be generated. Once the process is complete, they will receive an email notification.

You can find the frontend [**here**](https://github.com/fady2019/SubtitleGeneratorFrontend).

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
3. **Setup Database** (PostgreSQL)
   - **On Cloud** <br/>
     You can use database services such as [Supabase](https://supabase.com/) 
   - **Locally** <br/>
     To setup PostgreSQL on your local machine (with WSL), watch this [video](https://youtu.be/uq-QtZ5OdRM?si=2pLnHRdZN-C7Hg7o). Here are the commands used in the mentioned video:
     ```
     1. sudo apt update
     2. sudo apt install postgresql postgresql-contrib
     3. sudo -u postgres psql -c 'SHOW config_file'
     4. sudo vim <PATH_FROM_PREV_COMMAND_OUTPUT>
     5. sudo systemctl restart postgresql
     ```
     > ⚠️**Warning**
     > 
     > In the video, it's mentioned that the default password when connecting to the server in pgAdmin is 'postgres'. This is no longer true. You have to create a password. To do so, run the following commands:
     > ```
     > 1. sudo -i -u postgres
     > 2. psql
     > 3. \password postgres
     > 4. <PASSWORD>
     > 5. \q
     > 6. exit
     > ```
5. **Clone the Repository**
    - `git clone https://github.com/fady2019/SubtitleGeneratorBackend.git`
6. **Setup Virtual Environment**
    - open the project in ubuntu terminal
    - `sudo apt install python3.12-venv`
    - `python3.12 -m venv .venv` _(create a virtual environment)_
    - `. .venv/bin/activate` _(activate the virtual environment)_
7. **Setup Packages & System tools**
    - System tools _(here are the tools I needed, you might need additional or different ones)_
      - `sudo apt update`
      - `sudo apt install pkg-config libicu-dev python3-dev build-essential g++ ffmpeg`
    - Packages
      > ℹ️**Note**
      > 
      > Ensure the virtual environment is activated before you run the following command
      - `pip3.12 install -r requirements.txt` _(install the project dependencies)_

## Usage
> [!NOTE]
> Ensure the virtual environment is activated before you run the following commands
> 
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

## APIs Documentation

Check [Swagger APIs Doc](https://fady2019.github.io/SubtitleGeneratorAPIsDoc)

**Note:** You can't try the endpoints out in this swagger APIs doc. It's not connected to the project endpoints.

If you want to try them out, you have to use the swagger docs connected with the project endpoints. to do so:

1. host the project locally ([how?](#installation))
2. visit `http://127.0.0.1:5000/api-docs/`

## Project Folders

<details open>

```diff
.
├── README.md
├── app.py
#   >>> the application entry point
├── app_factory.py
#   >>> creates flask and celery apps
├── celery_tasks
│   ├── emails.py
#   │   >>> celery task for sending emails
│   ├── subtitle_media_file.py
#   │   >>> celery task for cleaning/optimizing audio
│   ├── subtitles.py
#   │   >>> celery task for generating the subtitle
│   └── temporary_tokens.py
#       >>> celery task for removing expired temporary tokens from db
├── db
│   ├── db_config.py
#   │   >>> setup the db config
│   ├── entities
│   │   ├── segment.py
#   │   │   >>> the "segment" db schema
│   │   ├── subtitle.py
#   │   │   >>> the "subtitle" db schema
│   │   ├── temporary_token.py
#   │   │   >>> the "temporary token" db schema
│   │   └── user.py
#   │       >>> the "user" db schema
│   ├── repositories
│   │   ├── repository
│   │   │   ├── repository.py
#   │   │   │   >>> db repository base class
#   │   │   │   >>> the main goal behind db repository is reducing code duplication when executing queries
│   │   │   ├── repository_typing.py
#   │   │   │   >>> contains type for the db repository
│   │   │   ├── create_repository.py
#   │   │   │   >>> db repository that handles the "create" query
│   │   │   ├── delete_repository.py
#   │   │   │   >>> db repository that handles the "delete" query
│   │   │   ├── find_repository.py
#   │   │   │   >>> db repository that handles the "find" query
│   │   │   ├── update_repository.py
#   │   │   │   >>> db repository that handles the "update" query
│   │   │   └── crud_repository.py
#   │   │       >>> db repository that inherits all repositories create, find, update, delete
│   │   ├── segment.py
#   │   │   >>> db repository for the "segment" schema
│   │   ├── subtitle.py
#   │   │   >>> db repository for the "subtitle" schema
│   │   ├── temporary_token.py
#   │   │   >>> db repository for the "temporary token" schema
│   │   └── user.py
#   │       >>> db repository for the "user" schema
│   ├── utils
│   │   └── entity_to_dict.py
#   │       >>> generates typed dict (interface) for db schema repository methods (dynamically)
#   │       >>> for example, the create repository method requires data (to create a row in the db),
#   │       >>> the interface of this data is generated dynamically by this file's functions
│   └── entity_dicts
│       ├── entity_dict.py
#       │   >>> contains the base typed dicts (interfaces) for the db schema dynamically generated interfaces
│       ├── segment_entity_dict.py
#       │   >>> contains the dynamically generated interfaces for the "segment" schema
│       ├── subtitle_entity_dict.py
#       │   >>> contains the dynamically generated interfaces for the "subtitle" schema
│       ├── temporary_token_entity_dict.py
#       │   >>> contains the dynamically generated interfaces for the "temporary token" schema
│       └── user_entity_dict.py
#           >>> contains the dynamically generated interfaces for the "user" schema
├── decorators
│   ├── errors
│   │   └── app_error_handler.py
#   │       >>> a decorator for catching the error and sending error response to the client
│   ├── input_validator
│   │   ├── __init__.py
#   │   │   >>> a decorator that takes input source and validator
#   │   │   >>> it executes the given validator on the data comes from the given input source
│   │   └── input_source.py
#   │       >>> classes for the user's input sources. where does the input come from? request json, args, files and so on
│   ├── restrictions
│   │   └── rate_limit.py
#   |       >>> a decorator that prevents the user from accessing an endpoint in quick succession
│   └── security
│       ├── auth_token.py
#       │   >>> decorators for handling the request auth token. sign, clear and validate it
│       └── user_subtitle.py
#           >>> a decorator for checking that the target user has a specific subtitle
├── dtos
│   ├── dto.py
#   │   >>> the base interface for app's dtos
#   │   >>> note: the main benefit of dtos is encapsulating the db query result
#   │             to pass it through functions or return it as a response to the client
│   ├── segment.py
#   │   >>> the segment schema dto(s)
│   ├── subtitle.py
#   │   >>> the subtitle schema dto(s)
│   └── user.py
#       >>> the user schema dto(s)
├── dtos_mappers
│   ├── mapper.py
#   │   >>> the base class for the dto mapper
#   │   >>> the dto mapper converts db query result (db row) to dto object
│   ├── segment.py
#   │   >>> coverts segment db row to segment dto
│   ├── subtitle.py
#   │   >>> coverts subtitle db row to subtitle dto
│   └── user.py
#       >>> coverts user db row to user dto
├── helpers
│   ├── __init__.py
│   ├── audio.py
#   │   >>> it contains some helper functions for audio
#   │   >>> extract_vocals: takes an audio path and generates an audio that contains vocals only
#   │   >>> get_audio_duration: calculates the duration of an audio
│   ├── celery.py
#   │   >>> it contains some helper functions for celery
#   │   >>> revoke_task: terminal celery task
#   │   >>> mark_task_as_revoked: marks task as terminated (in redis)
#   │   >>> remove_revoked_task: deletes marked-terminated task (from redis)
#   │   >>> is_revoked: checks whether a task marked a terminated or not
│   ├── cookies.py
#   │   >>> it contains some helper functions for response cookies
#   │   >>> set_cookie: stores a cookie in the response
#   │   >>> delete_cookie: removes a cookie from the response
│   ├── date.py
#   │   >>> it contains some helper functions for dates
#   │   >>> to_datetime: converts value to datetime if possible
#   │   >>> format_date: changes the date format to the target format
#   │   >>> add_to_datetime: increases a date by some milliseconds, seconds, minutes, ... so on
#   │   >>> is_in_future: checks whether a date is in the future or not
#   │   >>> get_duration: shows how many seconds, minutes, hours and days are in a date
│   ├── file.py
#   │   >>> it contains some helper functions for files
#   │   >>> delete_file: removes a file if exists
#   │   >>> delete_dir: removes a dir if exists
#   │   >>> create_file: creates a file if not exists
│   └── jwt.py
#       >>> it contains some helper functions for jwt tokens
#       >>> generate_token_from_payload: takes a payload and generates a jwt token for it
#       >>> extract_payload_from_token: takes a jwt token and extracts the payload from it
├── requirements.txt
#   >>> the project dependencies
├── response
│   ├── response.py
#   │   >>> a class that represents the endpoints' response
#   │   >>> it inherits the FlaskResponse and add some extra detail to it. like, adding message to each response
│   └── response_messages.py
#       >>> an enum that contains all response messages and their status code
├── routes
│   ├── api.py
#   │   >>> the root route for the app's api
│   ├── auth.py
#   │   >>> contains the auth endpoints (for more detail, check swagger: /api-docs/?urls.primaryName=Authentication)
│   └── subtitles
#       >>> contains the subtile & segment endpoints (for more detail, check swagger: /api-docs/?urls.primaryName=Subtitles)
│       ├── segments
│       │   ├── segment.py
│       │   └── segments.py
│       ├── subtitle.py
│       └── subtitles.py
├── services
│   ├── auth.py
#   │   >>> contains the business logic for the auth endpoints
│   ├── segments.py
#   │   >>> contains the business logic for the segment endpoints
│   ├── subtitles.py
#   │   >>> contains the business logic for the subtitle endpoints
│   └── subtitle_file
│       ├── __init__.py
#       │   >>> contains different classes for different subtitle file creators. like txt, srt and vtt
#       │   >>> each creator creates the file in its own format
│       └── subtitle_file_creator.py
#           >>> creates a file from a subtitle segments (the factory)
│  
├── swagger
│   ├── __init__.py
#   │   >>> configures swagger for the api's endpoints
│   ├── docs
#   │   >>> contains swagger yml files
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
#       >>> contains metadata and shared components for swagger
├── templates
│   └── emails
#       >>> contains all html templates for email
│       ├── base.html
│       ├── reset_password.html
│       ├── subtitle_generation_completed.html
│       ├── subtitle_generation_failed.html
│       └── verify_email.html
└── validation
    ├── auth.py
#   │   >>> contains validators for the auth endpoints
    ├── pagination.py
#   │   >>> contains the pagination validators
    ├── shared.py
#   │   >>> contains the validator executor, a function the executes a validator schema
    ├── subtitles.py
#   │   >>> contains validators for the subtitle endpoints
    ├── transformers.py
#   │   >>> contains input transformers for validation. like trim strings
    └── validators.py
#       >>> contains shared/general validators
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
