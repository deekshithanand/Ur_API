# define api resources
from flask import jsonify
from flask_restful import Resource, request, abort
from src import mongo
from bson import json_util
import json


def flattenList(lis: list) -> list:
    lis = [item.split(",") for item in lis]  # generate list of sub strings
    flatList = []
    for i in lis:
        flatList.extend(i)
    return flatList


class Details(Resource):

    def get(self):
        # get all user details

        fields = request.args.getlist('fields')  # ["1,2"]

        if fields is None:

            details = mongo.db.UserDetails.find_one(
                {"NAME.title": "DEEKSHITH ANAND"}, {"_id": 0})
            return details
        else:
            # return only the requested fields
            fields = flattenList(fields)
            query = dict()
            query["_id"] = 0
            for field in fields:
                query[field] = 1
            details = mongo.db.UserDetails.find_one(
                {"NAME.title": "DEEKSHITH ANAND"}, query)
            return details

    def post(self):
        # create new fields or update existing if field already exists
        # get data from form or raw json
        # whatever the data comes in is dict and that is sent to as update query

        formData = request.form
        jsonData = request.get_json()

        if formData:
            post_data = formData.lists()
            post_dict = dict()
            for k, v in post_data:
                post_dict[k] = v[0] if len(v) is 1 else v

            update_data = {"$set": post_dict}

        elif jsonData:
            update_data = {"$set": jsonData}

        else:
            abort(400)

        mongo.db.UserDetails.update(
            {"NAME.title": "DEEKSHITH ANAND"}, update_data)
        return {"message": "Record updated sucessfully"}, 201

    def delete(self):
        # delete a field from collection
        # user deletion done from user management
        # method accepts only get params in fields

        deleteFields = request.args.getlist('fields')
        delete_all_fields = request.args.get('allfields')
        delete_all_fields = delete_all_fields.upper() if delete_all_fields else None

        if delete_all_fields == 'TRUE':
            # code to delete all fields
            mongo.db.UserDetails.update({"NAME.title": "DEEKSHITH ANAND"},
                                        {"NAME": {"title": "DEEKSHITH ANAND"}}
                                        )
            return {"message": "All fields removed"}, 200

        elif deleteFields:
            deleteFields = flattenList(deleteFields)
            unset_dict = dict()
            for i in deleteFields:
                unset_dict[i] = 1
            unset_dict = {"$unset": unset_dict}

            mongo.db.UserDetails.update(
                {"NAME.title": "DEEKSHITH ANAND"},
                unset_dict
            )
            return {"message": "Specified field removed"}, 200
        else:
            # error for no args
            abort(400)
