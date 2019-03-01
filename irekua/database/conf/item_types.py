types = [
    {
        "name": "Audio",
        "description": "Grabacion de audio en un archivo de formato WAV\n",
        "schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "description": "JSON schema for WAV file media info",
            "properties": {
                "bitspersample": {
                    "default": 16,
                    "description": "Number of bits used for every audio sample in recording\n",
                    "examples": [
                        8,
                        16
                    ],
                    "type": "integer"
                },
                "numchannels": {
                    "default": 1,
                    "description": "Number of audio channels in recording\n",
                    "examples": [
                        1,
                        2
                    ],
                    "type": "integer"
                },
                "samplerate": {
                    "description": "Number of samples per minute taken by the recorder\n",
                    "examples": [
                        44100,
                        96000
                    ],
                    "type": "integer"
                },
                "timeexp": {
                    "default": 1,
                    "description": "Time expansion factor used in recording\n",
                    "examples": [
                        1,
                        10,
                        15
                    ],
                    "type": "integer"
                }
            },
            "required": [
                "samplerate",
                "numchannels",
                "timeexp"
            ],
            "title": "WAV media info",
            "type": "object"
        }
    }
]
