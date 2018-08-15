# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:46:27 2018

@author: anburiyan
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

""" Make conversation flow between dutch and with associated human """
import requests
import sqlite3
import config
import numpy as np
import logging
import utils.util as u
import os

# from self_info_config import SelfInfoConfiguration as sic

self_info_about_human = ["you are my sweety",
                         "you are $aliasname",
                         "you are my heartfull person",
                         "I am calling you as $aliasname"]
self_info_about_brain = ["myself is $aliasname",
                         "I am your fauvorite person",
                         "you have been calling me as $aliasname"]

logger = logging.getLogger(__name__)


def find_on_memory(human_request_text, who_connected, associated_brain):
    """ Find response for the human request """
    output = ""
    try:
        keep_conversation_in_memory(who_connected, human_request_text, 'human')
        response = requests.get("http://localhost:5000/parse", params={
                                "q": human_request_text, "project": "dutch", "model": "model_20180708-174450"})
        findings = response.json()
        output = process_findings(findings, output)
        keep_conversation_in_memory(associated_brain, output, 'brain')
    except Exception as exp:
        logger.error(
            "Error is occured while finding on memeory {0}".format(exp))
    return output


def keep_conversation_in_memory(convuniqueid, conversation, conversationby):
    ''' Store conversation in memory to remember it at next time '''
    try:
        with sqlite3.connect(config.sqlite_file) as con:
            cur = con.cursor()
            sql = 'INSERT INTO memory(convuniqueid,conversations,conversationby) VALUES("'"{}"'","'"{}"'","'"{}"'")'
            sql = sql.format(convuniqueid, conversation, conversationby)
            cur.execute(sql)
            con.commit()
    except Exception as exp:
        logger.error(
            "Error is occured while keep conversation in memeory {0}".format(exp))


def process_findings(findings, output):
    try:
        intent = findings["intent"]

        if 'intent' in findings:
            if intent['name'] == 'self':
                # change unique with actual connected between brain and human
                output = handle_self_info(findings, 'abcd12345')
            elif intent['name'] == 'information_about':
                output = handle_information_about(findings, 'abcd12345')
            elif intent['name'] == 'electronic_devices':
                output = handle_electronic_devices(findings, 'abcd12345')
        if not output:
            output = "Sorry! I could not find for you"
        keep_conversation_in_memory('abcd123456789', output, 'brain')
    except Exception as exp:
        logger.error(
            "An error is occured while processing findings {0}".format(exp))
    return output


def handle_self_info(resp, unique_human):
    ''' Handle self information between associated brain and human '''
    results = ''
    try:
        with sqlite3.connect(config.sqlite_file) as con:
            cur = con.cursor()
            # imagine as of now only one entity will be for self information
            sql = 'SELECT DISTINCT aliasname, description, createdon FROM ' + \
                resp['entities'][0]['entity']
            fields = []
            where = []
            params = {}
            where.append("uniquehuman = :uniquehuman")
            params['uniquehuman'] = unique_human

            if where:
                sql = '{} WHERE {}'.format(sql, ' AND '.join(where))                
            try:
                cur.execute(sql, params)
            except sqlite3.Error as e:
                logger.error("Error is occured while execute handle self info {0}".format(exp))                
                return
            output = ''
            results = cur.fetchall()
            if results and len(results) > 0:
                if resp['entities'][0]['entity'] == 'humans':
                    output = "{}. {} {}".format(np.random.choice(self_info_about_human)
                                                .replace("$aliasname", results[0][0]), results[0][1], results[0][2])
                else:
                    output = "{}. {} {}".format(np.random.choice(self_info_about_brain)
                                                .replace("$aliasname", results[0][0]), results[0][1], results[0][2])
    except Exception as exp:        
        logger.error(
            "Error is occured while handle self infor {0}".format(exp))    
    return output


def handle_electronic_devices(resp, unique_human):
    """ Handle electronic devices to perform on/off the devices """
    output = ''
    try:
        with sqlite3.connect(config.sqlite_file) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            fields = []
            where = []
            params = {}
            where_relationship = []
            params_relationship = {}
            sql = ''
            table = ''
            sql = 'SELECT DISTINCT {fields} FROM '
            for entity in resp['entities']:
                # if entity['value'].lower() == 'switch on':
                #     # switch on the device
                # elif entity['value'].lower() == 'switch off':
                #     # switch off the device
                if entity['entity'].lower() == 'electronic_devices':
                    fields = ['Name', 'state', 'CreatedOn',
                              'CreatedBy', 'MappedTo', 'DigitPin']
                    sql = sql + "electronic_devices"
                    if entity['value'].lower() == 'my computer':
                        # On which computer should perform the operation
                        # read the device details
                        where.append("MappedTo = :MappedTo")
                        params['MappedTo'] = entity['value'].lower()

            if fields:
                sql = sql.format(fields=', '.join(fields))
            else:
                sql = sql.format(fields='*')
            sql_ = sql

            if where:
                sql_ = '{} WHERE {}'.format(sql, ' AND '.join(where))
            try:
                cur.execute(sql_, params)
            except sqlite3.Error as e:
                logger.exception(
                    msg="Error is occured while excute {0}".format(e))
                return
            results = cur.fetchall()

            if results and len(results) > 0:
                if len(results) > 1:
                    output = 'I could remember so many but i can able to tell you only one now'
                else:
                    # trigger raspi to switch on/off the devices
                    if (connect_raspi(results[0][5])):
                        output = 'Switched on the machine'
            else:
                output = 'I could not find any devices for you'
    except Exception as exp:
        logger.error(
            "An error is occured when performing device handler {0}".format(exp))        
    return output


def connect_raspi(pin):
    """ Connect the raspi controller to trigger the event """
    triggered = False
    # connect raspi and trigger the given pin to switch on/off the machine

    return triggered


def handle_information_about(resp, unique_human):
    ''' Handle information about persons, relationships, educations, etc'''
    output = ''
    try:
        with sqlite3.connect(config.sqlite_file) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            fields = []
            where = []
            params = {}
            where_relationship = []
            params_relationship = {}
            fields.append("rowid")
            sql = ''
            for entity in resp['entities']:
                if entity['value'].lower() == 'name':
                    fields.append("Firstname")
                    fields.append("Lastname")
                elif entity['value'].lower() == 'aliasname':
                    fields.append("Aliasname")
                elif entity['value'].lower() == 'dob':
                    fields.append("DOB")
                elif entity['value'].lower() == 'bornplace':
                    fields.append("bornplace")
                elif entity['value'].lower() == 'dod':
                    fields.append("DOD")
                elif entity['value'].lower() == 'diedplace':
                    fields.append("diedplace")
                else:
                    fields = ['rowid', 'Firstname', 'Lastname',
                              'Aliasname', 'DOB', 'DOD', 'bornplace', 'diedplace']
                # Keep the same index order. Set will change the order of list since it is unstructed datastructure
                fields = sorted(set(fields), key=fields.index)

                sql = 'SELECT DISTINCT {fields} FROM people'
                if entity['entity'].lower() == 'people':
                    if entity['value'].lower():
                        # include row_id in where clause in case if the people already taken and continuing conversation about his/her
                        # As of now consider aliasname to filer records
                        where.append("Aliasname = :Aliasname")
                        params['Aliasname'] = entity['value'].lower()
                if entity['entity'].lower() == 'relationship':
                    if entity['value'].lower():
                        # include row_id in where clause in case if the people already taken and continuing conversation about his/her
                        # As of now consider aliasname to filer records
                        where_relationship.append("name = :name")
                        params_relationship['name'] = entity['value'].lower()
            if fields:
                sql = sql.format(fields=', '.join(fields))
            else:
                sql = sql.format(fields='*')
            sql_ = sql

            if where:
                sql_ = '{} WHERE {}'.format(sql, ' AND '.join(where))

            try:
                cur.execute(sql_, params)
            except sqlite3.Error as e:
                logger.exception(
                    msg="Error is occured while excute {0}".format(e))
                return
    except Exception as exp:
        logger.error(
            "An error is occured while handling information about {0}".format(exp))
    return output


def process_relationships(cur, resp, where_relationship, params_relationship, sql):
    """ Process relationships to get know about which person information """
    try:
        results = cur.fetchall()
        retrived_people_count = len(results)

        if results and len(results) > 0 and u.response_has_attribute_and_value(resp['entities'], 'entity', 'relationship'):
            # get relationship records. Take top 1 even if there are multiple records retrived
            peopleid = 0
            columnindex = 0
            for key in results[0].keys():
                if key in 'rowid':
                    peopleid = results[0][columnindex]
                    break
                columnindex += 1

            sql_rel = 'select relatedto from relationship rs inner join relationshiptypes rst \
                        on rs.relationshiptype = rst.rowid \
                        where rs.peopleid = {}'.format(peopleid)

            if where_relationship and len(where_relationship) > 0:
                sql_rel += ' AND rst.name = "'"{}"'"'.format(
                    params_relationship['name'])
            try:
                cur.execute(sql_rel)
            except sqlite3.Error as e:
                logger.exception(
                    msg="Error is occured while excute {0}".format(e))
                return
            results = cur.fetchall()
            peopleids = []
            if results and len(results) > 0:
                for result in results:
                    columnindex = 0
                    for key in result.keys():
                        if key in 'relatedto':
                            peopleids.append(result[columnindex])
                            break
                        columnindex += 1

                # convert list into comma separated if the list has int, float, then use map(str, [])
                # Else just pass []
                sql += ' where rowid in ({})'.format(
                    ", ".join(map(str, peopleids)))
                try:
                    cur.execute(sql)
                except sqlite3.Error as e:
                    logger.exception(
                        msg="Error is occured while excute {0}".format(e))
                    return
                results = cur.fetchall()

        if results and len(results) > 0:
            if retrived_people_count > 1:
                output = 'I could remember so many but i can able to tell you only one now'

            for res in results:
                column_index = 0
                fullname = ''
                for col in res.keys():
                    if col == 'Firstname' and res[column_index]:
                        fullname += '{} '.format(res[column_index])
                    elif col == 'Lastname' and res[column_index]:
                        fullname += '{} '.format(res[column_index])
                    elif col == 'aliasname' and res[column_index]:
                        output += 'people will call as {} '.format(
                            res[column_index])
                    elif col == 'DOB' and res[column_index]:
                        output += 'Born on {} '.format(res[column_index])
                    elif col == 'bornplace' and res[column_index]:
                        output += 'Born at {} '.format(res[column_index])
                    elif col == 'DOD' and res[column_index]:
                        output += 'Died on {} '.format(res[column_index])
                    elif col == 'diedplace' and res[column_index]:
                        output += 'Died at {} '.format(res[column_index])
                    column_index += 1
                if fullname:
                    output += "full name is {}".format(fullname)
                if retrived_people_count > 1:
                    break
    except Exception as exp:        
        logger.error(
            "An error is occured while process person's relationship information {0}".format(exp))
