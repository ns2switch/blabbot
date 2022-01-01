#!/usr/bin/env python3

#Copyright 2021 Anibal Cañada


#Blab is a telegram bot that recovers data leaks and allows users to search it is affected

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.


import os
import logging
import yaml
from include.telclient import telclient
from include.dynamo import blabdynamo

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#variables - conf
with open("conf/config.yml") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

SHORT_TIME_FORMAT = cfg['date']['short_format']
DAY_NAMES = cfg['date']['names']



if __name__ == '__main__':
    telclient()