# final-year-project


"builds": [

    {

    "src": "core/wsgi.py",

    "use": "@vercel/python"

    }

    ],

    "routes": [

    {

    "src": "/(.*)",

    "dest": "core/wsgi.py"

    }

    ]
