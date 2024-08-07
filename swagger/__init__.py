from flask import Flask
from flasgger import Swagger
import os


def config_swagger(app: Flask):
    swagger_config = Swagger.DEFAULT_CONFIG

    swagger_config["openapi"] = "3.0.3"
    swagger_config["title"] = "CS50x Subtitle Generator Docs"
    swagger_config["doc_dir"] = os.path.join(os.getcwd(), "swagger", "docs")
    swagger_config["specs_route"] = "/api-docs/"

    swagger_config["specs"] = [
        {
            "endpoint": "auth",
            "route": "/auth.json",
            "rule_filter": lambda rule: "api.auth" in rule.endpoint,
            "name": "Authentication",
        }
    ]

    return Swagger(
        app=app,
        config=swagger_config,
        template_file=os.path.join(os.getcwd(), "swagger", "template.yml"),
    )
