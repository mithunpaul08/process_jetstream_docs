# process_jetstream_docs
Takes the 144 .md files in jetstream repo and extract glossary out of it using an AI model

## steps

- `pip install -r requirements.txt`
- extract .md files from this repo:https://gitlab.com/jetstream-cloud/docs
  - use find or something on linux command line
- move it to a folder called `data/jetstream/` in this repo
- `python process_jetstream_docs
/nirav_jetstream.py`


## Caveats
- Code alls the AI Verde LLM delivery platform of Uofa datascience institute. Contact edwin for getting the ssh keys. Hardcoded now for "gpt-4-turbo" but a list of all models available can be found using ` curl -s -L "https://llm1.cyverse.ai/v1/models" -H "Authorization: Bearer $OPENAI_API_KEY" -H 'Content-Type: application/json'`(after you have exported the right OPENAI keys). Talk to edwin if you are from the data science institute.

  
