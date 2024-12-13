## License
**The Frontend / Web Client code is Licensed Under** [Mozilla Public License Version 2.0](https://choosealicense.com/licenses/)

**The Server / Backend code is Licensed Under** [GNU General Public License Version 3.0](https://choosealicense.com/licenses/)

## Installation
```shell
git clone https://github.com/kisenaa/Web-RSBP.git
# client / frontend
cd <cloned_directory/client>
npm install -g pnpm
pnpm install

# server / backend
cd <cloned_directory/server>
python -m venv venv
./venv/scripts/activate
pip install -r requirements.txt
```

## Running Backend
```shell
cd <cloned_directory/server>
./venv/scripts/activate
uvicorn server:app --reload

# Open http://127.0.0.1:8000/docs
```

## Running Frontend
```shell
cd <cloned_directory/client>
pnpm run dev

# Open http://localhost:5173/
```

