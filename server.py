from typing import Type

import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Ad, Session

app = Flask('app')


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code =status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response


def get_ad_by_id(ad_id: int):
    ad = request.session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, "Ad not found")
    return ad


def add_ad(ad: Ad):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "Ad already exists")


class AdView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)


    def post(self):
        ad_data = request.json
        ad = Ad(**ad_data)
        add_ad(ad)
        return jsonify(ad.dict), 201

    def patch(self, ad_id: int):
        ad_data = request.json
        ad = get_ad_by_id(ad_id)
        for field, value in ad_data.items():
            setattr(ad, field, value)
        add_ad(ad)
        return jsonify(ad.dict)

    def delete(self, ad_id: int):
        user = get_ad_by_id(ad_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({'status': 'Ad deleted'})


ad_view = AdView.as_view('ad_view')


app.add_url_rule('/ad/<int:ad_id>', view_func=ad_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ad', view_func=ad_view, methods=['POST'])


if __name__ == '__main__':
    app.run()


