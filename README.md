# Alfred-espanso

This workflow converts **simple** snippets from Alfred to espanso and vice-versa.
It allows also to append a bit of text (for instance from the clipboard history) to an existing snippet file in your espanso repository.


## Installation

Install the workflow and add ~/Library/Application Support/espanso to Features > Default Results > Search Scopes in Alfred's preferences.


## Usage

The workflow consists in three Universal Actions:

**1. Convert snippets → espanso**

Apply to an .alfredsnippet file (exported from Features > Snippets). 
This converts it to an espanso .yml file.
You can then put this .yml file in ~/Library/Application Support/espanso.

**2. Convert espanso → Alfred**

Apply to an .yml espanso file
This converts it to an .alfredsnippets file.
You can then install it by double-cliking.
If you hit command ⌘ before selecting this action, you will have the possibility to add an icon to this .alfredsnippet set.

Both these action work for **simple** (*static, one-to-one*) snippets

**3. Append to an espanso file**

Activate on a text (e.g. from the clipboard history). Activate this action and select a file from your ~/Library/Application Support/espanso/match folder. This will append the text at the end of the file, and open it (in your default app for .yml files, or with an app that you can choose), so that you can define the trigger.


## Command-line usage

The two python scripts alf_to_esp.py and esp_to_alf.py can be used directly in command line:

<code>python3 esp_to_alf.py [-h] [--icon ICON] espanso_file.yml</code>

<code>python3 alf_to_esp.py [-h] alfredsnippet_file.alfredsnippets</code>


## Acknowledgement

This workflow was deeply inspired by:

- @davidoc's [convert_alfredsnippets_to_espanso_package.py](https://gist.github.com/davidoc)
- @alfredapp's [snippet-transformer-workflow](https://github.com/alfredapp/snippet-transformer-workflow/)


