#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import requests
import progressbar as pb

from utilities.hdx_format import item
from utilities.store_records import StoreRecords


#
# Collecting package activity data.
#
def CollectPackageActivityData(limit=None):
  '''Collect packacge activity data from HDX.'''

  print '%s Querying HDX for package activity stream. Limit is %s.' % (item('prompt_bullet'), str(limit))
  
  #
  # Building URL.
  #
  u = 'https://data.hdx.rwlabs.org/api/action/recently_changed_packages_activity_list?limit=' + str(limit)
  r = requests.get(u)  
  
  #
  # Checking the status code.
  #
  if r.status_code != requests.codes.ok:
    print '%s HDX did not responde with a positive HTTP code.' % item('prompt_error')
    if verbose:
      print r.status_code
    return False

  else:

    #
    # Iterating over results.
    #
    records = []
    results = r.json()['result']

    i = 0
    widgets = [item('prompt_bullet'), ' Collecting country data:', pb.Percentage(), ' ', pb.Bar('-'), ' ', pb.ETA(), ' ']
    pbar = pb.ProgressBar(widgets=widgets, maxval=len(results)).start()

    for result in results:
      revision_data = {
        'user_id': result['user_id'],
        'timestamp': result['timestamp'],
        'revision_id': result['revision_id'],
        'dataset_id': result['data']['package']['name'],
        'owner_org': result['data']['package']['owner_org'],
        'activity_type': result['activity_type']
      }
      records.append(revision_data)

    i += 1
    pbar.update(i)

    #
    # Store records in database.
    #
    pbar.finish()
    StoreRecords(data=records, table='package_activity_data')



#
# Collect packages shared by countries.
#
def CollectCountryActivityData():
  '''Collecting country activity data from HDX.'''

  print '%s Querying HDX for country activity stream.' % item('prompt_bullet')
  
  #
  # Building URL.
  #
  u = 'https://data.hdx.rwlabs.org/api/action/group_list'
  r = requests.get(u)
  
  #
  # Checking the status code.
  # 
  if r.status_code != requests.codes.ok:
    print '%s HDX did not responde with a positive HTTP code.' % item('prompt_error')
    if verbose:
      print r.status_code
    return False

  else:

    #
    # Iterating over each country.
    #
    country_activity = []
    countries = r.json()['result']

    i = 0
    widgets = [item('prompt_bullet'), ' Parsing country list:', pb.Percentage(), ' ', pb.Bar('-'), ' ', pb.ETA(), ' ']
    pbar = pb.ProgressBar(widgets=widgets, maxval=len(countries)).start()
    for country in countries:

      u = 'https://data.hdx.rwlabs.org/api/action/group_show?id=' + country
      r = requests.get(u)

      #
      # Checking the status code.
      # 
      if r.status_code != requests.codes.ok:
        print '%s HDX did not responde with a positive HTTP code.' % item('prompt_error')
        if verbose:
          print r.status_code
        return False

      else:
        country_data = r.json()['result']
        
        #
        # Iterating for every dataset.
        #
        for dataset in country_data['packages']:
          country_select = {
            'country_id': country_data['id'],
            'country_name': country_data['display_name'],
            'dataset_id': dataset['id'],
            'dataset_owner_org': dataset['organization']['name'],
            'dataset_date_created': dataset['metadata_created']
          }
          country_activity.append(country_select)
      
      #
      # Updating progess bar.
      #
      i += 1
      pbar.update(i)

    #
    # Store records in database.
    #
    pbar.finish()
    StoreRecords(data=country_activity, table='organization_activity_data', verbose=False)



def CollectDatasetData():
  '''Collect data about all the datasets.'''

  u = 'https://data.hdx.rwlabs.org/api/action/package_list'

  print '%s Querying HDX for country activity stream.' % item('prompt_bullet')
  
  #
  # Building URL.
  #
  u = 'https://data.hdx.rwlabs.org/api/action/group_list'
  r = requests.get(u)
  
  #
  # Checking the status code.
  # 
  if r.status_code != requests.codes.ok:
    print '%s HDX did not responde with a positive HTTP code.' % item('prompt_error')
    if verbose:
      print r.status_code
    return False
