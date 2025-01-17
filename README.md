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
- Code alls the AI Verde LLM delivery platform of Uofa datascience institute. Contact edwin for getting the ssh keys. Hardcoded now for "gpt-4-turbo" but a list of all models available can be found using ``(after you have exported the right OPENAI keys).
- Uses a core divide and conquer approach.
- 
  
- Core of the code was written in couple of hours, - But Works. Also in combination to this, I used tools like sed, awk, regex on sublime text, and even chatgpt at times to do various cleaning up + sub parts- especially the nasty irritating ones like alphabetic merge sorting and cleaning up replies from the AI model. Basically my philosophy is use whatever it takes/whatever tools are available out there, as long as you get shit done.
