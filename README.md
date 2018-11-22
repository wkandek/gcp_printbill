gcp_printbill.py - summarizes GCP bills, understands both the downlaod and interactive format

Call: gcp_printbill.py filename mincost project

  - filename: default gcpbill.csv
  - mincost: only print costs that are higher than this number, helps focus on larger values
  - project: only include project that match the pattern

  example: gcp_printbill.py apr_2018.csv 1000 -qe

  will analyze file apr_2018, only print cost items higher than 1000 and include projects that have a"-qe" in name
  
