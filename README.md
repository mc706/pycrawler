# Crawler


## Install

### Clone the project
``` 
git clone https://github.com/mc706/pycrawler.git
cd pycrawler
```

### Make a virtualenv
``` 
mkvirtualenv pycrawler -p ~/.pyenv/versions/3.6.0/bin/python
```
### Install Requirements
``` 
pip install -r requirements.txt
```

### Make sure you have `phantomjs` installed.
``` 
brew install phantomjs
```

## Setup Tests
Create a folder inside of `sites` with the name of your site:

```
mkdir sites/test_site
```

Create a config file inside of your site folder: so
`sites/test_site/config.yml`

```yml 
name: Test Site
domain: http://www.test.com
entry_points:
  - http://www.test.com/home/
```
## Run
To run all of the suites
``` 
python crawler.py
```

or to run a specific test:

``` 
python crawler.py test_site```
