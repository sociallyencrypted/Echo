# Echo

## Running Instructions
- Make a folder called `files` in the root directory of the project.
- Make a file called `.env` in the root directory of the project.
- Add the following line to the `.env` file:
```
CHATGPT_API_KEY=<YOUR_API_KEY>
```
- Run the following commands:
```
python3 echo.py
```
- Open a browser and go to `http://localhost:31337/`
- Voila!

## Notes
- Currently uses `gpt-3.5-turbo-instruct`. Can look into porting to `gpt-4-turbo`, but that will require moving from Completions API to Chat Completions API.
