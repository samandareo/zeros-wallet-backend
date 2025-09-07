from flask import Flask,render_template,url_for,request,redirect,flash,current_app,session,jsonify
#from flask_mysqldb import MySQL
import mysql.connector

import os
import secrets
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import math
import uuid
from werkzeug.security import check_password_hash,generate_password_hash
import cryptocode

import jwt
from datetime import datetime, timedelta, timezone
import json
import blocksmith
import random
import requests
from web3 import Web3
from hexbytes import HexBytes
from flask_cors import CORS
import re
import uuid
from solathon import Client, Keypair

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)



from dotenv import load_dotenv
load_dotenv()

client = Client(os.getenv('SOLANA_API_URL', "https://api.mainnet-beta.solana.com"))

privatepass = os.getenv('PRIVATE_PASS_KEY', '')
signing_key = os.getenv('JWT_SIGNING_KEY', '')

from apps.route import user,dcoin,coin,bannar,info,wallet,settings,swap,task,stakecoin,staketrx,airdrop,airdropparticipate,withdrew,admin
from apps.route import deposit,referral,quiz,badge