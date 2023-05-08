# SuperBIG

SuperBIG is a virtual prompt/context management system. It can take long prompts that wouldn't otherwise fit into the context size limit of your model and optimally search for information and snippets that are relevant to a search string. The search results can then be injected back into the prompt, cutting down on token length and giving the model just enough information to produce a solid generation.

ELI5: 
> SuperBIG wraps your prompt in a searchable environment to simulate a virtual context of unlimited size - think of it like a swapfile or pagefile with a search engine on top

More info: [https://github.com/oobabooga/text-generation-webui/pull/1548](https://github.com/oobabooga/text-generation-webui/pull/1548)

A simplified version of this exists (superbooga) in the [Text-Generation-WebUI](https://github.com/oobabooga/text-generation-webui), but this repo contains the full WIP project.

Note that SuperBIG is an experimental project, with the goal of giving local models the ability to give accurate answers using massive data sources.

## Installation
```
pip install superbig
```

## Usage

Import the `PseudocontextProvider`, and use it in your projects like so:

```
from superbig.provider import PseudocontextProvider

provider = PseudocontextProvider()
tokenizer = AutoTokenizer.from_pretrained(...)
model = AutoModelForCausalLM.from_pretrained(...)

...

new_prompt = provider.with_pseudocontext(prompt)

input_ids = tokenizer.tokenize(new_prompt)
model.generate(input_ids, **kwargs)
```

## Adding Sources

Sources can be automatically inferred from the prompt by passing `auto_infer_sources={}` to the provider:

```
new_prompt = provider.with_pseudocontext(prompt, auto_infer_sources={UrlSource: true})
```

You can also manually add sources using the `add_source` function:

```
provider.add_source('mysource', UrlSource('https://github.com/kaiokendev/superbig'))
```

Manually added sources need to be explicitly referenced in the prompt, surrounded by triple square brackets:

```
Hello World, this is my prompt, and this is my source: [[[mysource]]]
```

## Milestones
- [x] PyPI package
- [x] Bugs fixed for general usage
- [x] Manually-added sources
- [ ] More sources
    - [ ] PDF
    - [ ] Filepath
- [ ] More chunkers
    - [ ] Multitext 
    - [ ] Paragraph
    - [ ] Forum
- [ ] Allow each source to use separate chunkers
- [ ] Search result metadata
- [ ] Dynamically shrinking search result pages
- [ ] Custom search logic that incorporates model output (Focus system)