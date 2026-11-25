import logging

from fastapi import FastAPI, HTTPException
from flask import Flask

from .services import load_order

logger = logging.getLogger(__name__)
api = FastAPI()
web = Flask(__name__)


@api.get("/orders/{order_id}")
def order(order_id: int):
    try:
        return load_order(order_id)
    except KeyError as exc:
        logger.warning("order lookup failed: %s", exc)
        raise HTTPException(status_code=404, detail="E404") from exc


@web.errorhandler(LookupError)
def handle_error(err):
    logger.warning("lookup error: %s", err)
    return "E404", 404


@web.route("/orders/<int:order_id>")
def order_page(order_id):
    try:
        return load_order(order_id)
    except KeyError as exc:
        logger.warning("order lookup failed: %s", exc)
        return "not found", 404
