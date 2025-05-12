# General Idea of the Backend

The api is organized as follows:

In `main.py` is the main application which is started.
The file itself is relatively small and only contains the different routers and the app setup.

In the `api` directory lie the routers for specific conformance checking methods.

The overview that chatGPT gave.

```
backend/
├── app/
│   ├── main.py               # create_app(), include routers
│   ├── api/
│   │   ├── logs.py           # /api/logs: upload & metadata
│   │   └── modules/
│   │       ├── __init__.py
│   │       ├── log_skeleton.py      # router for log skeleton
│   │       ├── temporal.py  # router for temportal cc
│   │       └── ...
│   ├── conformance_checking/
│   │   ├── fuzzy.py          # pure-python implementation
│   │   ├── heuristic.py
│   │   └── ...
│   └── models/
│       └── schemas.py        # Pydantic models: LogUpload, ModuleResult, etc.
├── tests/
│   └── test_modules/
├── Dockerfile
└── requirements.txt
```
