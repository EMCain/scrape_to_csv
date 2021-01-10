# Setup

To get things running and test the example script, follow these steps.

Clone the repo. 

Set up and start the virtual environment.

```
$ virtualenv -p "$(which python3)" venv
$ source venv/bin/activate
```

(If you only have python3 on your computer, use which python instead.)

Then install the requirements:

```
$ (venv) pip install -r requirements.txt
```

Copy the absolute path to the src file and do this, pasting it into the first argument after "echo", to set up your module paths correctly. 

```bash
cd $(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
echo /absolute/path/to/src > src-path.pth
```

(If someone can help me figure out how to not have to do this, or better yet, how to turn this repo into a pip package people can easily use, that would be very helpful.)

## Run example

```
(venv) python src/examples/medications.py
```

Results will be in results/meds_example. Run as many times as you like -- a unique timestamp means a new file will be created each time. 


## Customization

Use `src/examples/medications.py` as an example. 

You will need to define the following: 

* an iterable of URLs. This can be a list like `["https://example.com/abc", "https://example.com/123"]`, but since many websites follow a predictable URL pattern it is often faster to create a generator function that yields each URL. 
* a parser callback that takes an HTML string as input, and returns a dict in the form `{"column header name":"cell value"}`. This dict will make up one row of the spreadsheet. 
* a list of column headers -- these should be the same as the dict keys in the callback function, and should be in the order you want to see them in the final spreadsheet. 
* a project name (should be a string, avoid spaces and other characters that don't play well with file paths).

It is recommended to use BeautifulSoup for the parser callback (although you could use any libary that can handle the DOM). [Chapter 12 of Automate the Boring Stuff with Python](https://automatetheboringstuff.com/2e/chapter12/) explains this library very well. 

I haven't tried this with a dynamic web page yet but you would probably use Selenium in the parser callback.