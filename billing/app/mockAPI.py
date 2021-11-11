from flask import json


mocked_json = json.dumps(
{
    "id": 77777,
    "sessions": [
        [
            1
        ],
        [
            4
        ]
    ],
    "tara": [
        800.0
    ]
})




mocked_sessions= json.dumps(

{
    "id": 1,
    "direction": "out",
    "bruto":800,
    "neto": 750, 
    "produce": 3,
    "containers": [1]
})
