# VirtualPatch data

Here you can find the data we collected for VirtualPatch. A brief description of
the files follows.

- **traces**: folder containing the raw trace data collected using systrace
- **notebooks**: contains the Jupyter notebooks used to collect and analyze the
data
- **parse_traces**: source code of the program used to parse the raw trace data
and extract the delay timings
- **patch_apis**: source code of the library that can be used to write patches for
VirtualPatch, including API documentation
- **evaluation**: source code of the exploits and security patches used for the
evaluation of VirtualPatch
- **container_generator**: code that can be used to generate the secure containers
for android apps
- **aggregated-severity-cat-google-play.csv**: contains the data we collected for
all the CVEs, used to compute the delays in patch delivery
- **bulletin_dates.csv**: contains the date in which each monthly bulletin was
published
- **launch.csv**: contains the launch timings extracted from the traces
- **patches-valid.csv**: data about Samsung security patches
- **traces.csv**: timings of different delays extracted from the traces
- **apps.csv**: list of apps used for the evaluation
- **container**: source code for the container template
