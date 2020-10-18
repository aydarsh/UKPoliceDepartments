# A client for DATA.POLICE.UK API usage

[`UKPoliceDepartments.ipynb`](UKPoliceDepartments.ipynb) - this file can be opened with Jupyter Notebook. Use [Anaconda](https://www.anaconda.com/products/individual) to launch Jupyter Notebook and then open the file.  

To run scripts place cursor in a cell and press CTRL+Enter.  

1. The first cell is to import libraries and declare methods;  
2. The second cell shows how to retrieve all police forces 
3. In the third cell one can get social engagement methods of a specified police force
  - Specify the value in variable like shown here: `police_force = 'cheshire'`
4. Here one can check if a police force has specified social engagement method
  - Specify values like shown here:
    - `police_force = 'bedfordshire'`
    - `social_engagement_method = 'facebook'`
5. With the code from the fifth cell one can retrieve police forces that have the specified social engagement method
  - Required variable value is `social_engagement_method = 'facebook'`