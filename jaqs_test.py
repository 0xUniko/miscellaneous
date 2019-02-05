#%%
from jaqs.data.dataapi import DataApi
api = DataApi(addr='tcp://data.quantos.org:8910')
api.login(17888842604, 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1NDgwNTU4OTg3NDAiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTc4ODg4NDI2MDQifQ.FH8qKKb014_J7l9TZbPKijKIzrCpZOj2YiKGZSas7n4')

#%%
api.quote('000001.SH', fields='last')