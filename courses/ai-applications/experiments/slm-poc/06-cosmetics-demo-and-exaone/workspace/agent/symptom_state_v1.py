"""Isolated prototype: represent present, explicitly absent, and unknown symptoms.

This does not change the existing agent, stored sessions, or model tools.
"""
from copy import deepcopy
from jsonschema import Draft202012Validator

SYMPTOMS=('dryness','breakout','redness','stinging','itching')
VALUES=('present','absent','unknown')
PATCH_SCHEMA={'type':'object','properties':{name:{'type':'string','enum':list(VALUES)} for name in SYMPTOMS},
              'additionalProperties':False,'minProperties':1}

def empty_state():return {name:'unknown' for name in SYMPTOMS}

def from_legacy_present_list(present):
    """Only presence can be recovered. Missing entries are NOT proof of absence."""
    if not isinstance(present,list) or any(x not in SYMPTOMS for x in present) or len(set(present))!=len(present):
        raise ValueError('Invalid legacy present-symptom list')
    return {name:'present' if name in present else 'unknown' for name in SYMPTOMS}

class SymptomSession:
    def __init__(self):
        self._state=empty_state();self.version=0

    @property
    def state(self):return deepcopy(self._state)

    def update(self,patch):
        errors=list(Draft202012Validator(PATCH_SCHEMA).iter_errors(patch))
        if errors:raise ValueError('; '.join(e.message for e in errors))
        self._state={**self._state,**deepcopy(patch)}
        self.version+=1
        return {'ok':True,'version':self.version,'state':self.state}
