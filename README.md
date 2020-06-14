# TFE EPL : Attack simulation for post mortem forensic training networks security

## Contributors
- Thomas Beckers
- Maxime Beugoms

## Abstract
When a network attack occurred it leaves some data in the packets emitted we can identify as suspect activity. It is then interesting to have some samples of packet captures of a network making traffic from classic users considered as white traffic and traffic from an attacker considered as malicious one. Theses captures are very useful when learning or designing a software to recognize the white traffic or/and the traffic provided by the attacker(s). Some tools are available to generate captures like .pcap files from a simulated network but it required a lot of installations and configurations that can result to a lot of time lost. Thus we develop a solution in Python that can be used like a library to create a simulated network with white traffic and attacks and perform packet captures on links. 

## Analysis of scientific articles
In order to organize our search and some notes are taken in an Excel file online [here](https://docs.google.com/spreadsheets/d/1pjoRHB0Wb5Mv2xuWurcemfUP_-nbiGaixM4Al2_lBsQ/edit?usp=sharing) to gather relevant data and save time by avoiding whole document reading next time.

## User guide sphinx
1. Install sphinx.
  ```
   pip install sphinx
  ```
2. Launch update of html pages.
  ```
    cd docs
    sphinx-apidoc -o . ..
    make html
  ```
3. Go and click on the index.html.<br>
  _Normally you are in the docs repository if not got to it._
  ```
   cd _build/html
  ```

### Web version available on https://mbeug.github.io/TFE_EPL_Attack-simulation-for-post-mortem-forensic-training-networks-security-/

## Meetings

### Meeting 30/10/2019

[Slide about progress and next sprint](https://docs.google.com/presentation/d/1TF-R83bfQwIfP4yjjg3j5dNAj4_xVH5JBpKgPbtTnAw/edit?usp=sharing)

### Meeting 13/11/2019
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1iTj7UDr42ZixHeJ2uBt1HXY3HtuGePntUOUttiBkKn8/edit?usp=sharing)

#### GNS3 API
We use the GNS3 API to create and connect dynamically virtual PCs. A first example is available with **simple_remote.py** in the **src** folder. You need to open the simpleRemote project in GNS3 then if you run the script you can create VPCs and start a capture. The capture can be found in the **capture** folder of the project.

### Meeting 27/11/2019
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1ijfUzu_D8m0oozuhHm4BKrXnJkHV_Q7o4oZF85fqEYM/edit?usp=sharing)

### Meeting 11/12/2019
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1HpBXY_eCdO258v2WNbibWgOJpp7rcxIZV2CrmX2HkDA/edit?usp=sharing)

### Meeting 14/02/2020
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1c_ba--s0l68Kj_VPVOd4CuT3MeOIyCkRIMlRl4m_IyQ/edit?usp=sharing)

### Meeting 28/02/2020
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1wl4QBeMIYbJrJR9LtY0AGm5KPFKpm_CWkACqQUZD_eg/edit?usp=sharing)

### Meeting 16/03/2020
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1zv0CAfBlcHPC_GzlQR-SX_XIXyVJKFHDvfZJD66JvFw/edit?usp=sharing)

### Meeting 31/03/2020
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1Y-5Z3Qmt6zwJHZz1rH1GJGQ2Dgv7KUslT1HYVnheXO4/edit?usp=sharing)

### Meeting 14/04/2020
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1jrOd_rnwWmrYi5ZgKnXkMNQZVh3xqfNYlRZO3YWYcXU/edit?usp=sharing)

### Meeting 28/04/2020
[Slide about progress and next sprint](https://docs.google.com/presentation/d/14TLEmYQ1V5d6NXI9s79MeNo5eY8DxXOE-aiguU4WIQE/edit?usp=sharing)

### Meeting 12/05/2020
[Slide about progress and next sprint](https://docs.google.com/presentation/d/1LMt46wIDFHNxUFqmKIWm0rZr8GxMX0AZ7sjldfIwuWA/edit?usp=sharing)
