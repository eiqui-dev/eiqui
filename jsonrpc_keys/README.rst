.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

JSON-RPC Keys
===========

Allow keys in json-rpc calls.


Parameters
=====
Key - The key
User - The user identified by the key
Actived - Check if the key can be used
urls - List of URL's separated by line affected by the key (empty for all)
       

Usage
=====

To use this module, you need to:

1. Create new key in configuration panel
2. Now the client need send the atribute 'key' in 'params':
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "call",
  "params": {
    "key": "The Key",
    [...]
  }
}
3. Add to your controller:
   key_user_id = request.env['jsonrpc.keys'].sudo().check_key(THE_KEY, request.httprequest.path)
   if not key_user_id:
   	raise Exception('Permission denied!')



Credits
=======

Creator
------------

* Alexandre Díaz <alex@aloxa.eu>
