
# Create-Wiki-Corpus

Research code to convert Wikipedia dump files into raw text files with each article in a new line. 
No markup-language, or HTML tags. Real sentences only.

## Running the script

The corpus-creation is computationally expensive and is designed to be run in parallel across multiple machines.
To do so, [ludwig](https://github.com/phueb/Ludwig) is used. 
Jobs are submitted by invoking the its command line interface:

```
ludwig -r 1 -c data/ wikiExtractor/
```

The ```-r``` flag indicates how many times to run a job on each ```ludwig``` machine. This should always be set to 1. 

The ```-c``` flag ensures that all folders required for execution are uploaded to each machine. 
By default, ```ludwig``` automatically uploads source code if it is in a folder the name of which is equivalent to the name of the root folder.
Third-party code for Wikipedia template expansion, available [here](https://github.com/attardi/wikiextractor/wiki), is not part of the source code folder, and therefore must be uploaded explicitly. 
Note that folders specified by the ```-c``` flag are not uploaded to each machine, but are uploaded to the remote root folder (on the shared drive), which is accessible by each machine.
Modules inside such folders are nonetheless importable because ```ludwig``` automatically appends the remote root folder to ```sys.path```.

Note that ```-c data/ wikiExtractor/``` must only be specified once, and can be omitted subsequently to save time. 
Don't forget add ```-c data/ wikiExtractor/``` whenever changes to the files in either folder have been made.



### Verifying output

A simple way to verify the output is to count the number of articles:

```
cd /media/research_data/CreateWikiCorpus
find runs/ -name titles.txt | xargs wc -l
```

Verify that the total number of lines is close to the total number of articles in the Wikipedia dump file.

If there are multiple corpora in `runs/`, you need to specify a subset of folder corresponding to the corpus of interest.
For example, say the parameter configuration 15-21 are associated with a corpus, the total number of articles can be calculated by:

```bash
cd /media/research_data/CreateWikiCorpus/runs
find param_15 param_16 param_17 param_18 param_19 param_20 param_21 -name titles.txt | xargs wc -l
```

## Technical Notes

Tested on Ubuntu 16.04 and MacOs using Python=>3.6.
